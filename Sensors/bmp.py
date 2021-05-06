#!/usr/bin/python
#encoding=utf-8
#--------------------------------------
#  Read data from a digital pressure sensor.
#  BMP180/BMP280
#
#  Official datasheet available from :
#  https://www.bosch-sensortec.com/bst/products/all_products/bme280
#
# Original Author : Matt Hawkins
# Date   : 21/01/2018
#
# https://www.raspberrypi-spy.co.uk/
# https://www.raspberrypi-spy.co.uk/2016/07/using-bme280-i2c-temperature-pressure-sensor-in-python/
# https://www.raspberrypi-spy.co.uk/2015/04/bmp180-i2c-digital-barometric-pressure-sensor/
#
#--------------------------------------
#  BMP388
#
# Official datasheet: https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmp388-ds001.pdf
#
# Original Author : Getelectronics
#
# https://github.com/getelectronics/PIBits/blob/master/python/bmp388.py
# http://www.pibits.net/
#
#--------------------------------------

#Examples:
#python3 bm.py (default options)
#python3 bm.py -a 0x76 -s 1013.25


import smbus
import time
import getopt
import sys
from ctypes import c_short


def getShort(data, index):
    # return two bytes from data as a signed 16-bit value
    return c_short((data[index+1] << 8) + data[index]).value


def getShortBmp180(data, index):
    # return two bytes from data as a signed 16-bit value
    return c_short((data[index] << 8) + data[index + 1]).value


def getUShort(data, index):
    # return two bytes from data as an unsigned 16-bit value
    return (data[index+1] << 8) + data[index]


def getUShortBmp180(data, index):
    # return two bytes from data as an unsigned 16-bit value
    return (data[index] << 8) + data[index + 1]


def getChar(data,index):
    # return one byte from data as a signed char
    result = data[index]
    if result > 127:
        result -= 256
    return result


def getUChar(data,index):
    # return one byte from data as an unsigned char
    result =  data[index] & 0xFF
    return result
    

def read_s8(bus, addr, cmd):
    result = bus.read_byte_data(addr, cmd)
    if result > 128:
        result -= 256
    return result


def read_u16(bus, addr, cmd):
    LSB = bus.read_byte_data(addr, cmd)
    MSB = bus.read_byte_data(addr, cmd + 0x01)
    return (MSB << 0x08) + LSB


def read_s16(bus, addr, cmd):
    result = read_u16(bus, addr, cmd)
    if result > 32767:
        result -= 65536
    return result


def readBMID(bus, addr):
    # Chip ID Register Address
    REG_ID     = 0xD0
    REG_ID_388 = 0x00
    try:
        (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID, 2)
        if (chip_id == 0):
            (chip_id, chip_version) = bus.read_i2c_block_data(addr, REG_ID_388, 2)
        return (chip_id, chip_version)
    except:
        print("Is the BMP sensor connected?")
        exit(2)


def readBME280(bus, addr):
    # Register Addresses
    REG_DATA = 0xF7
    REG_CONTROL = 0xF4

    REG_CONTROL_HUM = 0xF2

    # Oversample setting - page 27
    OVERSAMPLE_TEMP = 2
    OVERSAMPLE_PRES = 2
    MODE = 1

    # Oversample setting for humidity register - page 26
    OVERSAMPLE_HUM = 2
    bus.write_byte_data(addr, REG_CONTROL_HUM, OVERSAMPLE_HUM)

    control = OVERSAMPLE_TEMP<<5 | OVERSAMPLE_PRES<<2 | MODE
    bus.write_byte_data(addr, REG_CONTROL, control)

    # Read blocks of calibration data from EEPROM
    # See Page 22 data sheet
    cal1 = bus.read_i2c_block_data(addr, 0x88, 24)
    cal2 = bus.read_i2c_block_data(addr, 0xA1, 1)
    cal3 = bus.read_i2c_block_data(addr, 0xE1, 7)

    # Convert byte data to word values
    dig_T1 = getUShort(cal1, 0)
    dig_T2 = getShort(cal1, 2)
    dig_T3 = getShort(cal1, 4)

    dig_P1 = getUShort(cal1, 6)
    dig_P2 = getShort(cal1, 8)
    dig_P3 = getShort(cal1, 10)
    dig_P4 = getShort(cal1, 12)
    dig_P5 = getShort(cal1, 14)
    dig_P6 = getShort(cal1, 16)
    dig_P7 = getShort(cal1, 18)
    dig_P8 = getShort(cal1, 20)
    dig_P9 = getShort(cal1, 22)

    dig_H1 = getUChar(cal2, 0)
    dig_H2 = getShort(cal3, 0)
    dig_H3 = getUChar(cal3, 2)

    dig_H4 = getChar(cal3, 3)
    dig_H4 = (dig_H4 << 24) >> 20
    dig_H4 = dig_H4 | (getChar(cal3, 4) & 0x0F)

    dig_H5 = getChar(cal3, 5)
    dig_H5 = (dig_H5 << 24) >> 20
    dig_H5 = dig_H5 | (getUChar(cal3, 4) >> 4 & 0x0F)

    dig_H6 = getChar(cal3, 6)

    # Wait in ms (Datasheet Appendix B: Measurement time and current calculation)
    wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM)+0.575)
    time.sleep(wait_time/1000)  # Wait the required time  

    # Read temperature/pressure/humidity
    data = bus.read_i2c_block_data(addr, REG_DATA, 8)
    pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    hum_raw = (data[6] << 8) | data[7]

    #Refine temperature
    var1 = ((((temp_raw>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
    var2 = (((((temp_raw>>4) - (dig_T1)) * ((temp_raw>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
    t_fine = var1+var2
    temperature = float(((t_fine * 5) + 128) >> 8);

    # Refine pressure and adjust for temperature
    var1 = t_fine / 2.0 - 64000.0
    var2 = var1 * var1 * dig_P6 / 32768.0
    var2 = var2 + var1 * dig_P5 * 2.0
    var2 = var2 / 4.0 + dig_P4 * 65536.0
    var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * dig_P1
    if var1 == 0:
        pressure=0
    else:
        pressure = 1048576.0 - pres_raw
        pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
        var1 = dig_P9 * pressure * pressure / 2147483648.0
        var2 = pressure * dig_P8 / 32768.0
        pressure = pressure + (var1 + var2 + dig_P7) / 16.0

    # Refine humidity
    humidity = t_fine - 76800.0
    humidity = (hum_raw - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
    humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
    if humidity > 100:
        humidity = 100
    elif humidity < 0:
        humidity = 0

    return temperature/100.0,pressure/100.0,humidity


def readBMP180(bus, addr):
    # Register Addresses
    REG_CALIB  = 0xAA
    REG_MEAS   = 0xF4
    REG_MSB    = 0xF6
    # Control Register Address
    CRV_TEMP   = 0x2E
    CRV_PRES   = 0x34 
    # Oversample setting
    OVERSAMPLE = 3    # 0 - 3

    # Read calibration data
    # Read calibration data from EEPROM
    cal = bus.read_i2c_block_data(addr, REG_CALIB, 22)

    # Convert byte data to word values
    AC1 = getShortBmp180(cal, 0)
    AC2 = getShortBmp180(cal, 2)
    AC3 = getShortBmp180(cal, 4)
    AC4 = getUShortBmp180(cal, 6)
    AC5 = getUShortBmp180(cal, 8)
    AC6 = getUShortBmp180(cal, 10)
    B1  = getShortBmp180(cal, 12)
    B2  = getShortBmp180(cal, 14)
    MC  = getShortBmp180(cal, 18)
    MD  = getShortBmp180(cal, 20)

    # Read temperature
    bus.write_byte_data(addr, REG_MEAS, CRV_TEMP)
    time.sleep(0.005)
    (msb, lsb) = bus.read_i2c_block_data(addr, REG_MSB, 2)
    UT = (msb << 8) + lsb

    # Read pressure
    bus.write_byte_data(addr, REG_MEAS, CRV_PRES + (OVERSAMPLE << 6))
    time.sleep(0.04)
    (msb, lsb, xsb) = bus.read_i2c_block_data(addr, REG_MSB, 3)
    UP = ((msb << 16) + (lsb << 8) + xsb) >> (8 - OVERSAMPLE)

    # Refine temperature
    X1 = ((UT - AC6) * AC5) >> 15
    X2 = (MC << 11) / (X1 + MD)
    B5 = X1 + X2
    temperature = int(B5 + 8) >> 4

    # Refine pressure
    B6  = B5 - 4000
    B62 = int(B6 * B6) >> 12
    X1  = (B2 * B62) >> 11
    X2  = int(AC2 * B6) >> 11
    X3  = X1 + X2
    B3  = (((AC1 * 4 + X3) << OVERSAMPLE) + 2) >> 2

    X1 = int(AC3 * B6) >> 13
    X2 = (B1 * B62) >> 16
    X3 = ((X1 + X2) + 2) >> 2
    B4 = (AC4 * (X3 + 32768)) >> 15
    B7 = (UP - B3) * (50000 >> OVERSAMPLE)

    P = (B7 * 2) / B4

    X1 = (int(P) >> 8) * (int(P) >> 8)
    X1 = (X1 * 3038) >> 16
    X2 = int(-7357 * P) >> 16
    pressure = int(P + ((X1 + X2 + 3791) >> 4))

    return (temperature/10.0,pressure/100.0)
    
    
def readBMP388(bus, addr):
    BMP388_REG_ADD_WIA = 0x00
    BMP388_REG_VAL_WIA = 0x50

    BMP388_REG_ADD_ERR = 0x02
    BMP388_REG_VAL_FATAL_ERR = 0x01
    BMP388_REG_VAL_CMD_ERR = 0x02
    BMP388_REG_VAL_CONF_ERR = 0x04

    BMP388_REG_ADD_STATUS = 0x03
    BMP388_REG_VAL_CMD_RDY = 0x10
    BMP388_REG_VAL_DRDY_PRESS = 0x20
    BMP388_REG_VAL_DRDY_TEMP = 0x40

    BMP388_REG_ADD_CMD = 0x7E
    BMP388_REG_VAL_EXTMODE_EN = 0x34
    BMP388_REG_VAL_FIFI_FLUSH = 0xB0
    BMP388_REG_VAL_SOFT_RESET = 0xB6

    BMP388_REG_ADD_PWR_CTRL = 0x1B
    BMP388_REG_VAL_PRESS_EN = 0x01
    BMP388_REG_VAL_TEMP_EN = 0x02
    BMP388_REG_VAL_NORMAL_MODE = 0x30

    BMP388_REG_ADD_PRESS_XLSB = 0x04
    BMP388_REG_ADD_PRESS_LSB = 0x05
    BMP388_REG_ADD_PRESS_MSB = 0x06
    BMP388_REG_ADD_TEMP_XLSB = 0x07
    BMP388_REG_ADD_TEMP_LSB = 0x08
    BMP388_REG_ADD_TEMP_MSB = 0x09

    BMP388_REG_ADD_T1_LSB = 0x31
    BMP388_REG_ADD_T1_MSB = 0x32
    BMP388_REG_ADD_T2_LSB = 0x33
    BMP388_REG_ADD_T2_MSB = 0x34
    BMP388_REG_ADD_T3 = 0x35
    BMP388_REG_ADD_P1_LSB = 0x36
    BMP388_REG_ADD_P1_MSB = 0x37
    BMP388_REG_ADD_P2_LSB = 0x38
    BMP388_REG_ADD_P2_MSB = 0x39
    BMP388_REG_ADD_P3 = 0x3A
    BMP388_REG_ADD_P4 = 0x3B
    BMP388_REG_ADD_P5_LSB = 0x3C
    BMP388_REG_ADD_P5_MSB = 0x3D
    BMP388_REG_ADD_P6_LSB = 0x3E
    BMP388_REG_ADD_P6_MSB = 0x3F
    BMP388_REG_ADD_P7 = 0x40
    BMP388_REG_ADD_P8 = 0x41
    BMP388_REG_ADD_P9_LSB = 0x42
    BMP388_REG_ADD_P9_MSB = 0x43
    BMP388_REG_ADD_P10 = 0x44
    BMP388_REG_ADD_P11 = 0x45

    # Load calibration values.
    if bus.read_byte_data(addr, BMP388_REG_ADD_WIA) == BMP388_REG_VAL_WIA:
        u8RegData = bus.read_byte_data(addr, BMP388_REG_ADD_STATUS)
        if u8RegData & BMP388_REG_VAL_CMD_RDY:
            bus.write_byte_data(addr, BMP388_REG_ADD_CMD, BMP388_REG_VAL_SOFT_RESET)
            time.sleep(0.01)
    else:
        print ("Pressure sersor NULL!\r\n")
        exit(4)
    bus.write_byte_data(addr, BMP388_REG_ADD_PWR_CTRL,BMP388_REG_VAL_PRESS_EN | BMP388_REG_VAL_TEMP_EN | BMP388_REG_VAL_NORMAL_MODE)
    
    # Load calibration
    T1 = read_u16(bus, addr, BMP388_REG_ADD_T1_LSB)
    T2 = read_u16(bus, addr, BMP388_REG_ADD_T2_LSB)
    T3 = read_s8(bus, addr, BMP388_REG_ADD_T3)
    P1 = read_s16(bus, addr, BMP388_REG_ADD_P1_LSB)
    P2 = read_s16(bus, addr, BMP388_REG_ADD_P2_LSB)
    P3 = read_s8(bus, addr, BMP388_REG_ADD_P3)
    P4 = read_s8(bus, addr, BMP388_REG_ADD_P4)
    P5 = read_u16(bus, addr, BMP388_REG_ADD_P5_LSB)
    P6 = read_u16(bus, addr, BMP388_REG_ADD_P6_LSB)
    P7 = read_s8(bus, addr, BMP388_REG_ADD_P7)
    P8 = read_s8(bus, addr, BMP388_REG_ADD_P8)
    P9 = read_s16(bus, addr, BMP388_REG_ADD_P9_LSB)
    P10 = read_s8(bus, addr, BMP388_REG_ADD_P10)
    P11 = read_s8(bus, addr, BMP388_REG_ADD_P11)
    
    # Read temperature
    xlsb = bus.read_byte_data(addr, BMP388_REG_ADD_TEMP_XLSB)
    lsb = bus.read_byte_data(addr, BMP388_REG_ADD_TEMP_LSB)
    msb = bus.read_byte_data(addr, BMP388_REG_ADD_TEMP_MSB)
    adc_T = (msb << 0x10) + (lsb << 0x08) + xlsb
    
    # Compensate temperature
    partial_data1 = adc_T - 256 * T1
    partial_data2 = T2 * partial_data1
    partial_data3 = partial_data1 * partial_data1
    partial_data4 = partial_data3 * T3
    partial_data5 = partial_data2 * 262144 + partial_data4
    partial_data6 = partial_data5 / 4294967296
    T_fine = partial_data6
    temperature = partial_data6 * 25 / 16384
    
    
    # Read pressure
    xlsb = bus.read_byte_data(addr, BMP388_REG_ADD_PRESS_XLSB)
    lsb = bus.read_byte_data(addr, BMP388_REG_ADD_PRESS_LSB)
    msb = bus.read_byte_data(addr, BMP388_REG_ADD_PRESS_MSB)
    adc_P = (msb << 0x10) + (lsb << 0x08) + xlsb
    
    # Compensate pressure
    partial_data1 = T_fine * T_fine
    partial_data2 = partial_data1 / 0x40
    partial_data3 = partial_data2 * T_fine / 256
    partial_data4 = P8 * partial_data3 / 0x20
    partial_data5 = P7 * partial_data1 * 0x10
    partial_data6 = P6 * T_fine * 4194304
    offset = P5 * 140737488355328 + partial_data4 \
        + partial_data5 + partial_data6

    partial_data2 = P4 * partial_data3 / 0x20
    partial_data4 = P3 * partial_data1 * 0x04
    partial_data5 = (P2 - 16384) * T_fine * 2097152
    sensitivity = (P1 - 16384) * 70368744177664 \
        + partial_data2 + partial_data4 + partial_data5

    partial_data1 = sensitivity / 16777216 * adc_P
    partial_data2 = P10 * T_fine
    partial_data3 = partial_data2 + 65536 * P9
    partial_data4 = partial_data3 * adc_P / 8192
    partial_data5 = partial_data4 * adc_P / 512
    partial_data6 = adc_P * adc_P
    partial_data2 = P11 * partial_data6 / 65536
    partial_data3 = partial_data2 * adc_P / 128
    partial_data4 = offset / 0x04 + partial_data1 + partial_data5 \
        + partial_data3
    pressure = partial_data4 * 25 / 1099511627776
    altitude = 4433000 * (0x01 - pow(pressure / 100.0 / 101325.0, 0.1903))
    
    return (temperature/100.0, pressure/10000.0)
    


def getAltitude(pressure, slp):
    if(slp > 0):
        altitude = 44330 * (1.0 - pow(pressure / slp, 0.1903))
        if(altitude >= 0):
            return altitude
        else:
            return 0
    else:
        return 0


def getSensorName(chip_id):
    if(chip_id in [86, 87, 88]):
        return "BMP280"
    elif(chip_id == 96):
        return "BME280"
    elif(chip_id == 85):
        return "BMP180"
    elif(chip_id == 80):
        return "BMP388"
    else:
        print("Chip ID {} not handled by this script".format(chip_id))
        exit(1)
        
        
def getBus():
    try:
        return smbus.SMBus(1) # Rev 2 Pi, Pi 2 & Pi 3 uses bus 1
    except:
        try:
            return smbus.SMBus(0)  # Rev 1 Pi uses bus 0
        except:
            print("Is I2C interface enabled?")
            exit(2)
        

def main():
    address = 0x77 # Default device I2C address
    sea_level_pressure = 1013.25
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"ha:s:")
    except getopt.GetoptError:
        print ('bm.py -a <address> -s <seaLevelhPa>1')
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print ('bm.py -a <address> -s <seaLevelhPa>2')
            sys.exit()
        elif opt == "-a":
            address = int(arg, 0)
        elif opt == "-s":
            sea_level_pressure = float(arg)
            
    bus = getBus()

    (chip_id, chip_version) = readBMID(bus, address)
    sensor_name = getSensorName(chip_id)
    print ("Chip ID: {}".format(chip_id))
    print ("Version: {}".format(chip_version))
    print ("Name: {}".format(sensor_name))
    print ("")

    temperature = 0
    pressure = 0
    humidity = 0
    
    if(chip_id == 85):
        temperature,pressure = readBMP180(bus, address)
    elif(chip_id in [86, 87, 88, 96]):
        temperature,pressure,humidity = readBME280(bus, address)
    elif(chip_id == 80):
        temperature,pressure = readBMP388(bus, address)
    else:
        print("Chip ID {} not handled by this script".format(chip_id))
        exit(3)

    altitude = getAltitude(pressure, sea_level_pressure)

    print ("Temperatura: {0:0.2f} C".format(temperature))
    print ("Pressão: {0:0.2f} hPa".format(pressure))
    print ("Altitude: {0:0.2f} m".format(altitude))


if __name__=="__main__":
    main()
