import npyscreen, subprocess
from test import getfolders
from libfilmer import processo

class baseform(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm('TYPING')

    def create(self):
       self.myDepartment = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name='Folders', values = getfolders(False, True))

class deftype(npyscreen.Form):                                   
        
    def create(self):
        self.tyl = self.add(npyscreen.TitleSelectOne, max_height=2, name="Tipo", values = ["Filme", "Série"], scroll_exit=True)

    def afterEditing(self):
        if self.tyl.get_selected_objects() == ['Filme']:
#            self.parentApp.getForm('Result').resoot.value = self.tyl.get_selected_objects()      #Planejo não usar isso, mas vou deixar pq vou por em outro lugar
            self.parentApp.setNextForm('Result')
        else:
#            self.parentApp.getForm('Result2').resoot2.value = self.tyl.get_selected_objects()
            self.parentApp.setNextForm('Result2')       

class moviemode(npyscreen.ActionFormV2):                                   
        
    def create(self):
#        self.resoot = self.add(npyscreen.TitleText, max_height=2, name="result", scroll_exit=True)
        self.url = self.add(npyscreen.TitleText, name = "URL:")
        self.name = self.add(npyscreen.TitleText, name = "Nome do Filme", rely=4)
        self.folders = self.add(npyscreen.TitleSelectOne, name="Pastas", max_height=12, values = getfolders(False, True), rely=6, scroll_exit=True)
#        self.run = self.add(npyscreen.BoxBasic, values = subprocess.call('wget https://google.com', shell=True))

#    def run_process(self, url, name, folders):

    def on_ok(self):

        self.parentApp.switchForm(None)

    def afterEditing(self):
        self.parentApp.setNextForm(None)
        self.run = self.add(npyscreen.BoxBasic, values = subprocess.call('yes no', shell=True))

class seriemode(npyscreen.Form):                                   

    def afterEditing(self):
        self.parentApp.setNextForm(None)
        
    def create(self):
        self.resoot2 = self.add(npyscreen.TitleText, max_height=2, name="result2", scroll_exit=True)

class MyApplication(npyscreen.NPSAppManaged):
    typ, url, name, season, epis, direct = None, None, None, None, None, None
    def onStart(self):
        self.addForm('MAIN', baseform, name='folderselect')
        self.addForm('TYPING', deftype, name='Tipo')
        self.addForm('Result', moviemode, name='Modo Filmes')
        self.addForm('Result2', seriemode, name='Modo Séries')

if __name__ == '__main__':
   TestApp = MyApplication().run()