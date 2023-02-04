
from os import umask
from kivy.lang import Builder
from datetime import datetime
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty, BooleanProperty
# import kivy label
from kivy.uix.label import Label
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDToolbar
# import MDCard
from kivymd.uix.card import MDCard

from kivymd.uix.list import OneLineIconListItem, MDList
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.animation import Animation
from kivy.properties import DictProperty
from kivy.core.window import Window

# import MDFillRoundFlatButton from kivymd
from kivymd.uix.button import MDFillRoundFlatButton
#from kivy.utils import platform

import kivy
from kivy.clock import Clock
from actions import SparkClub
import kivy.uix.screenmanager as t
from kivy.storage.jsonstore import JsonStore
import webbrowser
import threading
from kivy.utils import platform

from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
Config.set("graphics", "resizable", 0)

from plyer import vibrator

window_size = [600,600]

class ContentNavigationDrawer(MDBoxLayout):
    def trigger_login(self):
        self.ids.username.text = SCI.account["username"]
        self.ids.email.text = SCI.account["email"]
    def getColor(self, name):
        return COLORS[name.lower()]
    pass


icons_item = {
            "exit-to-app": ["Sign out", "login"],
            "view-list": ["Landing Page", "landing"],
            "checkbox-marked-circle-outline": ["Attendance", "landing"],
            "list-status": ["Actions", "actions"],
            "account-circle": ["My Account", "account"]
        }
class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))
    def clickItem(self):
        if(icons_item[self.icon][1] == "login"):
            MDApp.get_running_app().root.ids.action_box.addData("Are You Sure?", "You will have to re-enter your username and password to access the app again!", [{"name": "Sign Out", "color": "red"}], self.signOut)
            MDApp.get_running_app().root.ids.action_box.show()
        else: 
            changePage(icons_item[self.icon][1])
        MDApp.get_running_app().root.ids.nav_drawer.set_state("closed")
    def signOut(self, buttonId):
        changePage("login")
        


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color
        
KVContents = open('comb.kv', encoding='utf8').read()

SCI = SparkClub()




    
    
        


 
 
initialPage = "landing"


        
    
    

COLORS = {
    "primary": rgba255to1((19, 3, 252,1)),
    "secondary": rgba255to1((7, 0, 105,1)),
    "light": rgba255to1((130, 207, 255,1)),
    "white": rgba255to1((255, 255, 255,1)),
    "gray" : rgba255to1((100, 100, 100,1)),
    "black": rgba255to1((0, 0, 0,1)),
    "success": rgba255to1((0, 200, 0,1)),
    "red": rgba255to1((255, 0, 0,1)),
    "green": rgba255to1((0, 255, 0,1)),
    "blue": rgba255to1((0, 0, 255,1))
}

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))







        



class MainScreen(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]









class ClickableMDCard(MDCard):
    identifier = StringProperty()
    link = StringProperty()
    def getColor(self, name):
        return COLORS[name.lower()]
    pass



class WindowManager(ScreenManager):
    
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)


class Main(MDApp):
    def getColor(self, name):
        return COLORS[name.lower()]
    
    def build(self):
        SCI.initialize()
        
        self.icon = "assets/applogo.png"
        
        print("Hello World")
        return Builder.load_string(KVContents)

    def on_start(self):
        
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name][0])
            )
        
        x = threading.Thread(target = handleLogin, args = (True,), daemon=True)
        x.start()

Window.fullscreen = False
Main().run()