from re import I
from kivy.lang import Builder
from datetime import datetime
from kivy.properties import StringProperty, ListProperty
# import kivy label
from kivy.uix.label import Label

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDToolbar

from kivymd.uix.list import OneLineIconListItem, MDList
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
import threading

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
            "list-status": ["Actions", "landing"],
            "account-circle": ["My Account", "account"]
        }
class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))
    def clickItem(self):
        changePage(icons_item[self.icon][1])


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

def rgba255to1(rgba):
    return (rgba[0]/255, rgba[1]/255, rgba[2]/255, rgba[3])

def fadeto(widget, opacity, duration):
    a = Animation(opacity=opacity, duration=duration)
    a.start(widget)
    

def toggle_message_box(show):
    MDApp.get_running_app().root.ids.message_box.pos_hint = {'center_x': 0.5, 'center_y': 0.5 if show else 10}


def changePage(page):
    MDApp.get_running_app().root.ids.window_manager.transition = t.RiseInTransition(duration=.3)
    MDApp.get_running_app().root.ids.window_manager.current = page
    if(page == "landing"):
        MDApp.get_running_app().root.ids.nav_bar_title.title = "Landing Page"
        x = threading.Thread(target = MDApp.get_running_app().root.ids.landingpage.addItems, args = (), daemon=True)
        x.start()
        
        MDApp.get_running_app().root.ids.nav_bar.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        #Clock.schedule_once(MDApp.get_running_app().root.ids.landingpage.addItems, 0)
        
        MDApp.get_running_app().root.ids.content_drawer.trigger_login()
        
    elif(page == "actions"):
        Clock.schedule_once(MDApp.get_running_app().root.ids.actionspage.addItems, 0)
    elif(page == "subgroup"):
        MDApp.get_running_app().root.ids.nav_bar.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  
        
        x = threading.Thread(target = MDApp.get_running_app().root.ids.subgrouppage.subgroupInfo, args = (), daemon=True)
        x.start()
        MDApp.get_running_app().root.ids.nav_bar_title.title = "Subgroup (" + subgroup + ")"
        
    elif(page == "login"):
        MDApp.get_running_app().root.ids.nav_bar_title.title = "You Shouldn't See This..."
        MDApp.get_running_app().root.ids.nav_bar.pos_hint = {'center_x': 0.5, 'center_y': 10}
        SCI.logout()
    elif(page == "account"):
        MDApp.get_running_app().root.ids.nav_bar_title.title = "My Account"
        MDApp.get_running_app().root.ids.accountpage.setup()
    
    MDApp.get_running_app().root.ids.nav_drawer.set_state("closed")
        

def getLandingPageItems():
    Clock.schedule_once(lambda x : toggle_message_box(True), 0)
    i = SCI.get_items("H")
    m = SCI.get_meeting_today()
    p = SCI.get_protons()
    Clock.schedule_once(lambda x : toggle_message_box(False), 0)
    return (i, m, p)
 
 
initialPage = "landing"

def handleLogin(token, data={}):
    if(token):
        if(SCI.try_login_with_key()):
            #changePage("landing")
            Clock.schedule_once(lambda x: changePage(initialPage), 0)
            
            
        else:
            Clock.schedule_once(lambda x: changePage("login"), 0)
    else:
        res = SCI.login(data["username"], data["password"])
        if(res):
            Clock.schedule_once(lambda x: changePage(initialPage), 0)
            
            
            # add a bad response here?
        
    
    

COLORS = {
    "primary": rgba255to1((19, 3, 252,1)),
    "secondary": rgba255to1((7, 0, 105,1)),
    "light": rgba255to1((130, 207, 255,1)),
    "white": rgba255to1((255, 255, 255,1)),
    "gray" : rgba255to1((100, 100, 100,1)),
    "black": rgba255to1((0, 0, 0,1)),
    "success": rgba255to1((0, 200, 0,1)),
    "red": rgba255to1((255, 0, 0,1))
}


class EmptySpace(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class Action(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class AttendanceItemEx(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    def checkInToMeeting(self):
        successful = SCI.sign_in_meeting()
        print(successful)
        if(successful):
            x = threading.Thread(target = MDApp.get_running_app().root.ids.landingpage.addItems, args = (), daemon=True)
            x.start()
        
    pass

class AttendanceItem(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class MessageBox(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class MeetingItem(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class MemberItem(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class LandingItem(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    def openLink(self):
        webbrowser.open("https://sparkclub.io/")
        print("A")
    pass

subgroup = ""
class SubgroupItem(FloatLayout):
    togoto = StringProperty()
    def getColor(self, name):
        return COLORS[name.lower()]
    def toSubgroup(self):
        global subgroup
        subgroup = self.togoto
        changePage("subgroup")
    pass




class Login(Screen):
   
    
    def submitForm(self):
        print("Submitted form!")
        x = threading.Thread(target = handleLogin, args = (False,{"username": self.ids.username.text, "password" : self.ids.password.text},), daemon=True)
        x.start()
        
        
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
        
class Actions(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    def removeAllElements(self):
        rows = [i for i in self.ids.all_items.children]
        for r in rows:
            self.ids.all_items.remove_widget(r)
                
    def addItems(self, dt):
        self.removeAllElements()
        self.ids.all_items.rows = 2
        self.ids.all_items.add_widget(Action())
        self.ids.all_items.add_widget(EmptySpace())
                
                
        
        
    pass


class MainScreen(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]

class Landing(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    def removeAllElements(self):
        rows = [i for i in self.ids.all_items.children]
        for r in rows:
            self.ids.all_items.remove_widget(r)
    
    
    def showItems(self, r):
        self.removeAllElements()
        #self.ids.all_items.rows = 9
        self.ids.all_items.add_widget(EmptySpace())
        self.ids.all_items.add_widget(EmptySpace())
        
        if(not r[1] == None):
            l = Label(text = "Current Meeting", font_size = "24dp", font_name =  'Roboto', color = self.getColor("secondary"),size_hint_y= None, bold=True)
        
            self.ids.all_items.add_widget(l)
            if(r[1]["logged"]):
                
                
                aI = AttendanceItem()
                
                aI.ids.meeting.text = r[1]["title"] + " at 12:00 PM (" + str(r[1]["length"]) +  "h)"
                
                self.ids.all_items.add_widget(aI)
                self.ids.all_items.add_widget(EmptySpace())
            else:
                print(r[1])
                aW = AttendanceItemEx()
                aW.ids.title.text = r[1]["title"]
                aW.ids.length.text = str(r[1]["length"]) + " hours"
                
                attending = False
                sg = []
                for i in r[1]["subgroups"]:
                    if i in SCI.account["subgroups"]:
                        attending = True
                        sg.append(i)
                            
                    
                if(attending):
                    aW.ids.subgroup.text = ("Lots of subgroups are meeting!" if len(sg) > 1 else "Your subgroup is meeting")
                    aW.ids.signin_subgroup_icon.icon = "check"
                    aW.ids.signin_subgroup_icon.text_color = self.getColor("success")
                    aW.ids.subgroup.color = self.getColor("success")
                else:
                    aW.ids.subgroup.text = "Your subgroup isn't meeting"
                    aW.ids.signin_subgroup_icon.icon = "help"
                    aW.ids.signin_subgroup_icon.text_color = self.getColor("red")
                    aW.ids.subgroup.color = self.getColor("red")
                    
                    
                    
                
                #aW.ids.subgroup.text = r[1]["subgroup"]
                
                self.ids.all_items.add_widget(aW)
                # for i in range(4):
                #     self.ids.all_items.add_widget(EmptySpace())
                self.ids.all_items.add_widget(EmptySpace())
        
        l = Label(text = "Active Items", font_size = "24dp", font_name =  'Roboto', color = self.getColor("secondary"),size_hint_y= None, bold=True)
        
        self.ids.all_items.add_widget(l)
        for lpi in r[0]:
            #self.ids.all_items.rows += 4
            
            
            nW = LandingItem()
            
            nW.ids.title.text = lpi["title"]
            nW.ids.icon.icon = lpi["icon"]
            
            nW.ids.description.text = lpi["contents"]
            if(not lpi["result"]["to"] == "link"):
                nW.ids.landingitem_content.remove_widget(nW.ids.buttonct)
                
                
            if(lpi["contents"] == ""):
                nW.ids.landingitem_content.remove_widget(nW.ids.description)
            
            self.ids.all_items.add_widget(nW)
            # for i in range(3):
            #     self.ids.all_items.add_widget(EmptySpace())
        
        
        self.ids.all_items.add_widget(EmptySpace())
        #self.ids.all_items.rows += 3
        
        l = Label(text = "My Subgroups", font_size = "24dp", font_name =  'Roboto', color = self.getColor("secondary"),size_hint_y= None, bold=True)
        
        
        self.ids.all_items.add_widget(l)
        for s in SCI.account["subgroups"]:
        
            nS = SubgroupItem(togoto = s)
            nS.ids.subgroup_name.text = s
            self.ids.all_items.add_widget(nS)
        self.ids.all_items.add_widget(EmptySpace())
        
    
    def addItems(self):
        
        r = getLandingPageItems()
        Clock.schedule_once(lambda x: self.showItems(r), 0)
        
        
                
                
        
        
    pass

class NavDrawer(MDToolbar):
    pass

class Custom(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class Account(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    def setup(self):
        self.ids.username.text = SCI.account["username"]
        self.ids.account_role.text = SCI.account["role"].upper()
    pass

class Splash(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class Subgroup(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    def subgroupInfo(self):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        r = SCI.get_subgroup(subgroup)
        m = SCI.get_meetings()
        u = SCI.get_users()
        l = SCI.get_items(r[0]["tag"])
        Clock.schedule_once(lambda x: self.setup(r, m, u, l), 0)
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
    def setup(self, sgD, meetings, users, items):
        sg = sgD[0]
        self.ids.tag.text = ("• " if (sgD[1]) else "" ) + sg["tag"]
        self.ids.subgroup_name.text = sg["name"]
        
        inGroup = (sg["name"] in SCI.account["subgroups"])
        if(inGroup):
            self.ids.subgroup_membership.text = "You are a leader of this subgroup" if sgD[1] else "You are a member of this subgroup"
            self.ids.action_button.text = "Leave Subgroup"
            self.ids.action_button.md_bg_color = self.getColor("red")
            self.ids.action_button.disabled = sgD[1]
            self.ids.action_button.opacity = 0.3 if sgD[1] else 1
            
        else:
            self.ids.subgroup_membership.text = "You are not in this subgroup"
            self.ids.action_button.text = "Join Subgroup"
            self.ids.action_button.md_bg_color = self.getColor("primary")
        pass
        
        show = 10
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        now = datetime.now()
        
        for m in meetings:
            if(show > 0 and sg["name"] in m["subgroups"]):
                dout = datetime.strptime(m["datetime"], f)
                if(dout > now):
                    mI = MeetingItem()
                    
                    mI.ids.title.text = m["title"]
                    
                    mI.ids.date.text = str(dout.month) + "/" + str(dout.day) + " @ " + str(dout.hour - 12 if dout.hour > 12 else dout.hour) + ":" + str(dout.minute).zfill(2) + ("PM" if dout.hour >= 12 else "AM")
                    self.ids.meetings.add_widget(mI)
                    show -= 1
        if(show >= 10):
            l = Label(text="No upcoming meetings scheduled", italic=True, font_size="12dp", font_name="Roboto", color=self.getColor("secondary"))
            self.ids.meetings.add_widget(l)
        for u in users:
            if(sg["name"] in u["access"]["groups"]):
                mI = MemberItem()
                if(u["id"] in sg["managers"]):
                    mI.ids.username.text = "• " + u["username"]
                else:
                    mI.ids.username.text = u["username"]
                self.ids.members.add_widget(mI)
        for i in items:
            lI = LandingItem()
            lI.ids.title.text = i["title"]
            lI.ids.icon.icon = i["icon"]
            lI.ids.description.text = i["contents"]
            if(not i["result"]["to"] == "link"):
                lI.ids.landingitem_content.remove_widget(lI.ids.buttonct)
                
                
            if(i["contents"] == ""):
                lI.ids.landingitem_content.remove_widget(lI.ids.description)
            self.ids.groupitems.add_widget(lI)
            
            
    pass

class WindowManager(ScreenManager):
    
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)


class Main(MDApp):
    def getColor(self, name):
        return COLORS[name.lower()]
    
    def build(self):
        self.icon = "assets/applogo.png"
        return Builder.load_string(KVContents)

    def on_start(self):
        
        for icon_name in icons_item.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item[icon_name][0])
            )
        
        x = threading.Thread(target = handleLogin, args = (True,), daemon=True)
        x.start()


Main().run()