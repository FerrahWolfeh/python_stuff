# coding: utf-8
import subprocess, socket, os, sys, requests, re
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
            inter = '/home/MVS/'
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
            inter = '/home/SRS/'
            return inter
        else:                                                    #Fecha instantaneamente se não for nenhum dos dois
            print('Não foi possível identificar a máquina')
            print('Terminando execução')
            exit(1)


            
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
        download = 'wget ' + aspas(url)
        subprocess.call(download, shell=True)
        subprocess.call(rename, shell=True)
        subprocess.call(catpasta, shell=True)
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
        download = 'wget ' + aspas(url)
        subprocess.call(download, shell=True)
        subprocess.call(rename, shell=True)
        subprocess.call(catpasta, shell=True)
        print
        print('Concluído')
        print
        exit(0)

def usuario():
    p1 = str(input('Insira a URL de download (fim da url deve terminar com ".mkv", ".mp4", ".avi" ou ".srt"): '))
    checkurl(p1)
    ex = '.' + p1.split(".")[-1]
    if ex == '.mp4'.lower() or ex == '.mkv'.lower() or ex == '.avi'.lower() or ex == '.srt'.lower():
        pass
    else:
        print('URL Inválida')
        exit(1)
    print()
    print()
    perg = str(input('O download é uma série ou um filme? (S/F): ').upper())
    print()
    print()
    if perg == 'F':
        p4 = 0
        p5 = 0
        fs = True
        p2 = str(input('Insira o nome do filme igual ao do TMDB: '))
        print()
        print()
        p3 = str(input('Insira a categoria principal do filme: '))
        print()
        print()
        verificarpasta(p3, fs)
        processo(p1, p2, p3, p4, p5, fs)
    elif perg == 'S':
        fs = False
        p2 = str(input('Insira o nome da série igual ao do TMDB: '))
        print()
        print()
        p3 = str(input('Insira a categoria principal da série: '))
        print()
        print()
        p4 = str(input('Insira a temporada do episódio: ').zfill(2))
        p5 = str(input('Insira o número do episódio:').zfill(2))
        verificarpasta(p3, fs)
        processo(p1, p2, p3, p4, p5, fs)

usuario()
