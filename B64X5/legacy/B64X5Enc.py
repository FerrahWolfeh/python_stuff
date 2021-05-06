import base64
import binascii
inp = str(input('Entre os dados: '))
stg0 = inp.encode('ascii')
stg1 = base64.b64encode(stg0)
stg2 = base64.b64encode(stg1)
stg3 = base64.b64encode(stg2)
stg4 = base64.b64encode(stg3)
stghex = base64.b16encode(stg4)
stgbin = binascii.b2a_hex(stghex)
stgfinal = base64.b64encode(stgbin)
print(stgfinal.decode('ascii'))
