import base64
import binascii
import os


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def decode(inpdec, declvl):
    if declvl == 0:
        print(inpdec)
    elif declvl == 1:
        stg0 = inpdec.encode('ascii')
        stgfinal = base64.b64decode(stg0)
        output = stgfinal.decode()
    elif declvl == 2:
        stg0 = inpdec.encode('ascii')
        stg1 = base64.b64decode(stg0)
        stgfinal = base64.b64decode(stg1)
        output = stgfinal.decode()
    elif declvl == 3:
        stg0 = inpdec.encode('ascii')
        stg1 = base64.b64decode(stg0)
        stg2 = base64.b64decode(stg1)
        stg3 = base64.b64decode(stg2)
        output = stg3.decode('ascii')
    elif declvl == 4:
        stg0 = inpdec.encode('ascii')
        stg1 = base64.b64decode(stg0)
        stg2 = base64.b64decode(stg1)
        stg3 = base64.b64decode(stg2)
        stg4 = base64.b64decode(stg3)
        output = stg4.decode('ascii')
    elif declvl == 5:
        stg0 = inpdec.encode('ascii')
        stgfinal = base64.b64decode(stg0)
        stgbin = binascii.a2b_hex(stgfinal)
        stghex = base64.b16decode(stgbin)
        stg4 = base64.b64decode(stghex)
        stg3 = base64.b64decode(stg4)
        stg2 = base64.b64decode(stg3)
        stg1 = base64.b64decode(stg2)
        output = stg1.decode()


def encode(inpenc, enclvl):
    if enclvl == 0:
        print(inpenc)
    elif enclvl == 1:
        stg0 = inpenc.encode('ascii')
        stg1 = base64.b64encode(stg0)
        print(stg1.decode('ascii'))
    elif enclvl == 2:
        stg0 = inpenc.encode('ascii')
        stg1 = base64.b64encode(stg0)
        stg2 = base64.b64encode(stg1)
        print(stg2.decode('ascii'))
    elif enclvl == 3:
        stg0 = inpenc.encode('ascii')
        stg1 = base64.b64encode(stg0)
        stg2 = base64.b64encode(stg1)
        stg3 = base64.b64encode(stg2)
        print(stg3.decode('ascii'))
    elif enclvl == 4:
        stg0 = inpenc.encode('ascii')
        stg1 = base64.b64encode(stg0)
        stg2 = base64.b64encode(stg1)
        stg3 = base64.b64encode(stg2)
        stg4 = base64.b64encode(stg3)
        print(stg4.decode('ascii'))
    elif enclvl == 5:
        stg0 = inpenc.encode('ascii')
        stg1 = base64.b64encode(stg0)
        stg2 = base64.b64encode(stg1)
        stg3 = base64.b64encode(stg2)
        stg4 = base64.b64encode(stg3)
        stghex = base64.b16encode(stg4)
        stgbin = binascii.b2a_hex(stghex)
        stgfinal = base64.b64encode(stgbin)
        output = stgfinal.decode('ascii')
    else:
        print('Especifique um valor válido')
        input('Pressione qualquer tecla para sair...')


def outputfinal():
    print('Aqui está sua string:')
    print(output)
    input('Pressione qualquer tecla para sair...')
