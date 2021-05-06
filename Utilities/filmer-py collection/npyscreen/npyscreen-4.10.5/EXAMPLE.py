#!/usr/bin/env python
# encoding: utf-8

import npyscreen
#npyscreen.disableColor()

name = False

class TestApp(npyscreen.NPSApp):
    def main(self):
        # These lines create the form and populate it with widgets.
        # A fairly complex screen in only 8 or so lines of code - a line for each control.
        F  = npyscreen.Form(name = "Baixar Filme/Série")
        t  = F.add(npyscreen.TitleText, name = "URL:", )
        global name 
        name = t.value
        fn = F.add(npyscreen.TitleFilename, name = "Nome:",)
 #       fn2 = F.add(npyscreen.TitleFilenameCombo, name="Filename2:")
        ms = F.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Categorias", 
                values = ["Option1","Option2","Option3"], scroll_exit=True)
        ms2= F.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Tipo", 
                values = ["Filme", "Série"], scroll_exit=True)
        
        # This lets the user play with the Form.
        F.edit()


print(name)
        
if __name__ == "__main__":
    App = TestApp()
    App.run()   
