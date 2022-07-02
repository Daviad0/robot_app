from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from actions import SparkClub

KVContents = open('Login.kv', encoding='utf8').read()

SCI = SparkClub()


class Login(FloatLayout):
    def rgba255to1(self, rgba):
        return (rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3])
    
    def submitForm(self):
        print("Submitted form!")
        v = True
        res = SCI.login(self.ids.username.text, self.ids.password.text)
        print(res)
        

class LoginPage(MDApp):
    def __init__(self):
        super().__init__()
        self.screen = Builder.load_string(KVContents)
        
    def build(self):
        return self.screen
    
    
    
    

LoginPage().run()
        