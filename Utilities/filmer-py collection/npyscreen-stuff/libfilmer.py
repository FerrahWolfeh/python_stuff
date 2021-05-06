# coding: utf-8
import os, re, requests, socket, subprocess, sys
from os import path
from urllib.parse import unquote

def checkurl(url):                                           #Converte e checa se URL é válida
    if not re.match('(?:http|ftp|https)://', url):
        urlfn = 'http://{}'.format(url)
    try:
        response = requests.get(urlfn)
        pass
    except requests.ConnectionError as exception:
        print("URL Inválida ou não existe")
        exit(1)

def aspas(entrada):                                          #Põe aspas na string, nada demais...
    fainal = '"' + entrada + '"'
    return fainal

def getintervalue(fs):                                         #Tenta reconhecer qual servidor o programa está sendo executado.
    server = socket.gethostname()         
    if fs == True:
        if server == 'ns541102':                                 #Paramiko
            inter = '/home/fms/movies/'
            return inter
        elif server == 'Ubuntu-1804-bionic-64-minimal':          #Mobius
            inter = '/home/Movies/'
            return inter
        else:                                                    #Fecha instantaneamente se não for nenhum dos dois
            print('Não foi possível identificar a máquina')
            print('Terminando execução')
            exit(1)
    else:
        if server == 'ns541102':                                 #Paramiko
            inter = '/home/seris/'
            return inter
        elif server == 'Ubuntu-1804-bionic-64-minimal':          #Mobius
            inter = '/home/Series/'
            return inter
        else:                                                    #Fecha instantaneamente se não for nenhum dos dois
            print('Não foi possível identificar a máquina')
            print('Terminando execução')
            exit(1)

def getfolders(fs):
    filenames= os.listdir (getintervalue(fs)) # get all files' and folders' names in the current directory
    result = []
    for filename in filenames: # loop through all the files and folders
        if os.path.isdir(os.path.join(os.path.abspath("."), filename)): # check whether the current object is a folder or not
            result.append(filename)
    result.sort()
    print(result)
            
def verificarpasta(categoria, fs):                               #Verifica as pastas usando o caminho gerado pelo getintervalue() como base.
    pasta = path.exists(getintervalue(fs) + categoria)           #Se caso a pasta não existir ou for digitada errada, o programa fecha.
    if pasta == False:
        print('Essa pasta não existe...')
        print('Verifique se digitou certo ou se está no servidor correto')
        exit(1)
    else:
        pass

def processo(url, nome, categoria, temporada, episodio, fs):                         #Faz mágica
    if fs == True:
        fs = True
        filme = url.split("/")[-1]
        goodfilme = unquote(filme)
        ext = '.' + filme.split(".")[-1]
        nomefinal = aspas(nome + ext)
        rename = 'mv -v' + ' ' + aspas(goodfilme) + ' ' + nomefinal
        catpasta = 'mv -v' + ' ' + nomefinal + ' ' + getintervalue(fs) + categoria
        download = 'wget -P ' + getintervalue(fs) + categoria + ' ' + '-O ' + nomefinal + ' ' + aspas(url)
        subprocess.call(download, shell=True)
        print
        print('Concluído')
        print
        exit(0)
    else:
        fs = False
        filme = url.split("/")[-1]
        goodfilme = unquote(filme)
        ext = '.' + filme.split(".")[-1]
        nomefinal = aspas(nome + ' ' + 'S' + temporada + 'E' + episodio + ext)
        rename = 'mv -v' + ' ' + aspas(goodfilme) + ' ' + nomefinal
        catpasta = 'mv -v' + ' ' + nomefinal + ' ' + getintervalue(fs) + categoria
        download = 'wget -P ' + getintervalue(fs) + categoria + ' ' + '-O ' + nomefinal + ' ' + aspas(url)
        subprocess.call(download, shell=True)
        print
        print('Concluído')
        print
        exit(0)

def connect_server():
    paa = 1
