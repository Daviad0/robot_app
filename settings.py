import re
from kivy.network.urlrequest import UrlRequest
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
import requests
import os

path = ""

class AppSettings():
    def __init__(self):
        self.settings = {
            "color_scheme": "dark",
            "vibrate": True
        }
    def initialize(self):
        global path
        path = os.path.join(MDApp.get_running_app().user_data_dir, "account.json")
        self.storage = JsonStore(path)
        if(self.storage.exists("config")):
            self.settings = self.storage.get("config")["settings"]
        else:
            self.storage.put("config", settings=self.settings)
        
    def save(self):
        self.storage.put("config", settings=self.settings)
        
    def setSetting(self, key, value):
        try:
            self.settings[key] = value
            self.save()
        except:
            pass