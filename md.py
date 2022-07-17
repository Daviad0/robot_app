from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.animation import Animation
from kivy.properties import DictProperty
import json
from kivy.clock import Clock
from actions import SparkClub
import kivy.uix.screenmanager as t
from kivy.storage.jsonstore import JsonStore
import webbrowser

# from pushyy import Pushyy
# from pushyy import RemoteMessage

KVContents = open('App.kv', encoding='utf8').read()

SCI = SparkClub()

def rgba255to1(rgba):
    return (rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3])

def fadeto(widget, opacity, duration):
    a = Animation(opacity=opacity, duration=duration)
    a.start(widget)
    
def changePage(page):
    MDApp.get_running_app().root.transition = t.RiseInTransition(duration=.3)
    MDApp.get_running_app().root.current = page
    if(page == "landing"):
        Clock.schedule_once(MDApp.get_running_app().root.ids.landingpage.addItems, .5)
        

def getLandingPageItems():
    i = SCI.get_items()
    m = SCI.get_meeting_today()
    return (i, m)
 

def authenticate(dt):
    # look for token here
    if(SCI.try_login_with_key()):
        changePage("landing")
    else:
        changePage("login")
    

COLORS = {
    "primary": rgba255to1((19, 3, 252,1)),
    "secondary": rgba255to1((7, 0, 105,1)),
    "white": rgba255to1((255, 255, 255,1)),
    "gray" : rgba255to1((100, 100, 100,1)),
    "black": rgba255to1((0, 0, 0,1)),
    "success": rgba255to1((0, 255, 0,1))
}


class EmptySpace(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass
class AttendanceItemEx(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class LandingItem(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    
    pass


def openLink(link):
    webbrowser.open(link)
    print("A")

class Login(Screen):
   
    
    def submitForm(self):
        print("Submitted form!")
        v = True
        res = SCI.login(self.ids.username.text, self.ids.password.text)
        if(res):
            changePage("landing")
            getLandingPageItems()
        else:
            self.ids.username.text = ""
            self.ids.password.text = ""
    def getColor(self, name):
        return COLORS[name.lower()]
    def goToTempLogin(self):
        print("Go to temp login")
        self.ids.login_page.pos_hint = {'center_x': 0.5, 'center_y': 10}
        self.ids.temp_page.pos_hint = {'center_x': 0.5, 'center_y': 0.75}
    def usernameChange(self):
        self.ids.username.icon_right = ""
        if(self.ids.username.text == ""):
            # keep password disabled
            self.ids.password.disabled = True
            
            fadeto(self.ids.password, 0.3, 0.25)
            self.ids.login_button.disabled = True
            fadeto(self.ids.login_button, 0.3, 0.25)
        else:
            self.ids.password.disabled = False
            fadeto(self.ids.password, 1, 0.25)
    def passwordChange(self):
        self.ids.password.icon_right = ""
        if(self.ids.username.text == "" or self.ids.password.text == ""):
            # disable login button
            self.ids.login_button.disabled = True
            fadeto(self.ids.login_button, 0.3, 0.25)
        else:
            self.ids.login_button.disabled = False
            fadeto(self.ids.login_button, 1, 0.25)
    def emailChange(self):
        if(self.ids.temp_email.text == "" or not "@" in self.ids.temp_email.text):    
            self.ids.temp_send_code.disabled = True
            fadeto(self.ids.temp_send_code, 0.3, 0.25)
        else:
            self.ids.temp_send_code.disabled = False
            fadeto(self.ids.temp_send_code, 1, 0.25)
    def sendCode(self):
        # do the temp code passing here
        if(self.ids.temp_email.text == ""):
            return
        self.ids.temp_code.disabled = False
        fadeto(self.ids.temp_code, 1, 0.25)
        
            
class Landing(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    
    def addItems(self, dt):
        
        r = getLandingPageItems()
        
        self.ids.all_items.rows = 5
        self.ids.all_items.add_widget(AttendanceItemEx())
        for i in range(4):
            self.ids.all_items.add_widget(EmptySpace())
        
        for lpi in r[0]:
            self.ids.all_items.rows += 4
            
            
            nW = LandingItem()
            
            nW.ids.title.text = lpi["title"]
            nW.ids.icon.icon = lpi["icon"]
            nW.ids.description.text = lpi["contents"]
            if(not lpi["result"]["to"] == "link"):
                nW.ids.landingitem_content.remove_widget(nW.ids.buttonct)
            else:
                print("A")
                nW.ids.buttonct.bind(on_release=lambda x: openLink(lpi["result"]["to"]))
                
            if(lpi["contents"] == ""):
                nW.ids.landingitem_content.remove_widget(nW.ids.description)
            
            self.ids.all_items.add_widget(nW)
            for i in range(3):
                self.ids.all_items.add_widget(EmptySpace())
                
                
        
        
    pass

class Custom(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class Account(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class Splash(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class WindowManager(ScreenManager):
    
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
    

# def my_token(token):
#     print(token)
    
# def foreground_notif(message):
#     print(message)
#     MDApp.get_running_app().recent_notif = message.as_dict()

# def click_notif(message):
#     print(message)
#     MDApp.get_running_app().recent_notif = message.as_dict()
    


class LoginPage(MDApp):
    recent_notif = DictProperty(rebind=True)
    
    # def get_token(self):
    #     Pushyy().get_device_token(my_token)
        
    def on_start(self):
        #Pushyy().token_change_listener(my_token)
        Clock.schedule_once(authenticate, 5)
        
        
        
    def build(self):
        
        return Builder.load_string(KVContents)
    
    
    
    
    

LoginPage().run()
        