# initial set up of imports

import time
import datetime

# imports the modules for the sensor
import bme280
import smbus2
    
# csv to be able to open file
import csv

# calibrate the sensor
port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)
data = bme280.sample(bus, address, calibration_params)

def get_temp():
    temperature = "{:.2f}".format(data.temperature)
    temperature = str(temperature)
    return(temperature)

def get_pressure():
    pressure = "{:.5f}".format(data.pressure / 100)
    pressure = str(pressure)
    return(pressure)

def get_humidity():
    humidity = "{:.2f}".format(data.humidity)
    humidity = str(humidity)
    return(humidity)

def time_now():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    now = str(now)
    return(now)

def write_to_csv():
    # the a is for append, if w for write is used then it overwrites the file
    with open('./sensor.csv', mode='a') as sensor_readings:
        sensor_write = csv.writer(sensor_readings, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_to_log = sensor_write.writerow([time_now(),get_temp(),get_pressure(),get_humidity()])
        return(write_to_log)

write_to_csv()

#print(date_now(), time_now(), get_temp(), get_pressure(), get_humidity())
