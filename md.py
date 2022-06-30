from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout

KVContents = open('Login.kv', encoding='utf8').read()


class Login(FloatLayout):
    def rgba255to1(self, rgba):
        return (rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3])

class LoginPage(MDApp):
    def __init__(self):
        super().__init__()
        self.screen = Builder.load_string(KVContents)
        
    def build(self):
        return self.screen
    
    
    

LoginPage().run()
        