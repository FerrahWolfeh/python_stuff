import base64
import binascii
import os
from SL import *


def mainfunc():
    chc = input('Deseja: Criptografar ou Descriptografar (C/D):').lower()
    if chc == 'c':
        p1 = input('Entre o que deseja ser criptografado: ')
        p2 = int(input('Entre o grau do programa [1-5]: '))
        cls()
        encode(p1, p2)
        outputfinal()
    if chc == 'd':
        p1 = input('Entre o que deseja ser descriptografado: ')
        p2 = int(input('Entre o grau da criptografia [1-5]: '))
        cls()
        decode(p1, p2)
        outputfinal()


mainfunc()
