import npyscreen as np
import os, socket

class firststage(np.NPSApp):

    def setopt(self, title, oList):
        self.title = title
        self.options = oList

    def main(self):
        F = np.Form(name = "Baixar Filmes/Séries",)
        ms= F.add(np.TitleSelectOne, max_height=2, value = [], name="Tipo", values = ["Filme", "Série"], scroll_exit=True)
#        t  = F.add(np.TitleText, name = "URL:", use_two_lines=True )
#        t2 = F.add(np.TitleText, name = "Nome do Filme")
#        opt = F.add(np.TitleSelectOne, name="Pastas", max_height=len(self.options), values=self.options, scroll_exit=True)
        F.edit()
        self.type = ms.get_selected_objects()
        
class secstagefilme(np.NPSApp):

    def setopt(self, title, oList):
        self.title = title
        self.options = oList

    def main(self):
        F = np.Form(name = "Baixar Filmes/Séries",)
#        ms= F.add(np.TitleSelectOne, max_height=2, value = [], name="Tipo", values = ["Filme", "Série"], scroll_exit=True)
        t  = F.add(np.TitleText, name = "URL:", )
        t2 = F.add(np.TitleText, name = "Nome do Filme", rely=4)
        opt = F.add(np.TitleSelectOne, name="Pastas", max_height=12, values=self.options, rely=6, scroll_exit=True)
        F.edit()
        self.dir = opt.get_selected_objects()

def getintervalue(fs, dbgflag):                                         #Tenta reconhecer qual servidor o programa está sendo executado.
    server = socket.gethostname()
    if dbgflag == True:
        inter = "./"
        return inter
    if fs == True and dbgflag == False:
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
    elif fs == False and dbgflag == False:
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

def getfolders(fs, dbg):
    filenames= os.listdir (getintervalue(fs, dbg)) # get all files' and folders' names in the current directory
    result = []
    for filename in filenames: # loop through all the files and folders
        if os.path.isdir(os.path.join(os.path.abspath(getintervalue(fs, dbg)), filename)): # check whether the current object is a folder or not
            result.append(filename)
    result.sort()
    return result

def debugtest():
    a = getfolders(True, True)
    return a

def MakeMovie(title, oList):

    a = secstagefilme()
    a.setopt(title, oList)
    a.run()
    return a.return_this

alpha = debugtest()

def DefineType():
    b = firststage()
    b.setopt(title, oList)
    b.run()
    return b.type

print(MakeMovie('Categoria', alpha))
