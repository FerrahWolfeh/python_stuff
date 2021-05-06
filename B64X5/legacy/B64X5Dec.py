import base64
import binascii
inpdec = str(input('Entre os dados criptografados: '))
stg0 = inpdec.encode('ascii')
stgfinal = base64.b64decode(stg0)
stgbin = binascii.a2b_hex(stgfinal)
stghex = base64.b16decode(stgbin)
stg4 = base64.b64decode(stghex)
stg3 = base64.b64decode(stg4)
stg2 = base64.b64decode(stg3)
stg1 = base64.b64decode(stg2)
output = stg1.decode()
print(output)