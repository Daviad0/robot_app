from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

KVContents = open('Login.kv', encoding='utf8').read()


class Login(FloatLayout):
    def rgba255to1(self, rgba):
        return (rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3])
    
    def submitForm(self):
        print("Submitted form!")
        v = True
        if(self.ids.username.text == ""):
            v = False
            
            self.ids.username.md_bg_color = self.rgba255to1((50, 0, 0, 1))
        if(self.ids.password.text == ""):
            v = False
            self.ids.password.md_bg_color = self.rgba255to1((50, 0, 0, 1))
        

class LoginPage(MDApp):
    def __init__(self):
        super().__init__()
        self.screen = Builder.load_string(KVContents)
        
    def build(self):
        return self.screen
    
    
    
    

LoginPage().run()
        