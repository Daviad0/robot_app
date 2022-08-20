
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
from settings import AppSettings
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

inPopup = False

icons_item = {
            "exit-to-app": ["Sign out", "login"],
            "view-list": ["Landing Page", "landing"],
            "checkbox-marked-circle-outline": ["Meetings", "attendance"],
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
SETTINGS = AppSettings()

def rgba255to1(rgba):
    if(len(rgba) == 3):
        return (rgba[0]/255, rgba[1]/255, rgba[2]/255, 1)
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
        MDApp.get_running_app().root.ids.nav_bar_title.title = "Actions"
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
    elif(page == "attendance"):
        MDApp.get_running_app().root.ids.nav_bar_title.title = "Meeting Schedule"
        MDApp.get_running_app().root.ids.attendancepage.show()
    
    
        

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
        
    
    

COLORS = {}

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

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

class Meeting(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class IDButton(MDFillRoundFlatButton):
    buttonid = NumericProperty(0)

class ActionBox(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    def show(self):
        
        
        
        global inPopup
        if(inPopup):
            
            return
        inPopup = True
        self.opacity = 0
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        fadeto(self, 1, .2)
        #vibrate(0.4)
        if(platform == "android" or platform == "ios"):
            vibrator.vibrate(0.2)
    def actualHide(self):
        global inPopup
        self.pos_hint = {'center_x': 0.5, 'center_y': 10}
        
    def hide(self):
        print("HIDE")
        self.pos_hint = {'center_x': 0.5, 'center_y': 10}
        
    def addData(self, title, contents, buttons, callback=None):
        if(inPopup):
            return
        # Each callback should have an argument for the buttonid
        self.ids.title.text = title
        self.ids.contents.text = contents
        
        self.ids.buttons.clear_widgets()
        self.callback = callback
        n = 0
        for b in buttons:
            name = b["name"]
            color = b["color"]
            self.ids.buttons.add_widget(IDButton(text=name, md_bg_color=self.getColor(color), color=self.getColor('white'), on_release=self.performAction, buttonid=n, font_size="12sp", padding="12dp"))
            n+=1
    def performAction(self, *args):
        global inPopup
        buttonId = args[0].buttonid
        print("Action Performed: " + str(buttonId))
        if(buttonId == -1):
            self.hide()
        else:
            self.callback(buttonId)
            self.hide()
        inPopup = False
        
    
    pass

class IDInput(MDTextField):
    inputid = NumericProperty(0)
    def getColor(self, name):
        return COLORS[name.lower()]
    pass
class InputBox(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    def show(self):
        global inPopup
        if(inPopup):
            return
        self.opacity = 0
        inPopup = True
        
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        fadeto(self, 1, .2)
        #vibrate(0.4)
        if(platform == "android" or platform == "ios"):
            vibrator.vibrate(0.1)
    def actualHide(self):
        global inPopup
        
        inPopup = False
    def hide(self):
        
        self.pos_hint = {'center_x': 0.5, 'center_y': 10}
    def addData(self, title, contents, inputs, callback=None):
        if(inPopup):
            return
        # Each callback should have an argument for the buttonid
        self.ids.title.text = title
        self.ids.contents.text = contents
        
        self.ids.inputs.clear_widgets()
        self.callback = callback
        self.data = []
        n = 0
        for b in inputs:
            hint = b["hint"]
            multiline = b["multiline"]
            protected = b["protected"]
            id = "form" + str(n)
            i = IDInput(inputid=n,multiline=multiline, password=protected, line_color_focus= self.getColor('primary'),line_color_normal= self.getColor('primary'), color_mode= 'custom', active_line=True, hint_text=hint, font_name= 'Roboto', border=(2,2,2,2), spacing=(20,20,20,20), padding=(20,20,20,20),border_color= (0,0,0,1))
            i.bind(text=self.changeText)
            i.line_color_focus = self.getColor('primary')
            self.ids.inputs.add_widget(i)
            n+=1
            self.data.append("")
    def changeText(self, *args):
        inputId = args[0].inputid
        print("changed text: " + str(inputId))
        self.data[inputId] = args[0].text
    def performAction(self, *args):
        global inPopup
        buttonId = args[0].buttonid
        if(buttonId == -1):
            self.hide()
        else:
            self.callback(self.data)
            self.hide()
        inPopup = False
            
    
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
    weblink = StringProperty("")
    moduleitemid = StringProperty("")
    def getColor(self, name):
        return COLORS[name.lower()]
    def openLink(self):
        print(self.weblink)
        webbrowser.open(self.weblink)
        print("A")
        
    def handleConfirmation(self, buttonId):
        if(buttonId == 0):
            x = threading.Thread(target = self.bgDeleteItem, args = (self.moduleitemid,), daemon=True)
            x.start()
    def deleteItem(self):
        MDApp.get_running_app().root.ids.action_box.addData("Are You Sure?", "This will delete the Landing Item for EVERYONE, not just you seeing it!", [{"name" : "Delete", "color": "red"}], self.handleConfirmation)
        MDApp.get_running_app().root.ids.action_box.show()
    def bgDeleteItem(self, id):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.remove_item(id)
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : changePage("landing"), 0)
        
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

class SmallMeetingItem(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]

class Attendance(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    
    def getItems(self):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        a = SCI.get_meetings()
        s = SCI.get_subgroups()
        u = SCI.get_this_user()
        Clock.schedule_once(lambda x : self.addItems(a, s, u), 0)
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
    
    def show(self):
        
        x = threading.Thread(target = self.getItems, args = (), daemon=True)
        x.start()
    
    def triggerOverlay(self, *args):
        card = args[0]
        touch = args[1]
        if(not card.collide_point(touch.x, touch.y)):
            return
        
        if(not type(card) is ClickableMDCard):
            return
        
        link = card.link
        
        if(link == "upcoming"):
            self.showUpcomingOverlay(card)
        elif(link == "past"):
            self.showPastOverlay(card)
    
    def showUpcomingOverlay(self, card):
        
        id = card.identifier
        m = next(x for x in self.meetings if x["_id"] == id)
        
        
        attending = []
        for sg in self.subgroups:
            if(sg['name'] in m['subgroups']):
                attending.append(sg['name'])
        
        fs = ""
        sgAttending = False
        for i in range(0, len(attending)):
            
            bold = attending[i] in self.user['access']['groups']
            if(bold):
                sgAttending = True
            fs += ("[b]"+attending[i]+"[/b]") if bold else attending[i]
            if(i != len(attending) - 1):
                fs += ", "
        fs += " are attending this meeting!"
        
        if(len(attending) < 1):
            fs = "No one is attending this meeting yet!"
        
        buttons = []
        if(sgAttending):
            buttons.append({"name": "Request 'EXCUSED' Status", "color": "primary"})
        
        MDApp.get_running_app().root.ids.action_box.addData(m['title'], m['description'] + "\n\n" + str(m['length']) + " hours\n\n" + fs, buttons, self.handleUpcomingOverlay)
        MDApp.get_running_app().root.ids.action_box.show()
        
        
        pass
    
    def showPastOverlay(self, card):
        id = card.identifier
        m = next(x for x in self.meetings if x["_id"] == id)
        
        
        attending = []
        for sg in self.subgroups:
            if(sg['name'] in m['subgroups']):
                attending.append(sg['name'])
        
        fs = ""
        sgAttending = False
        for i in range(0, len(attending)):
            
            bold = attending[i] in self.user['access']['groups']
            if(bold):
                sgAttending = True
            
            fs += ("[b]"+attending[i]+"[/b]") if bold else attending[i]
            if(i != len(attending) - 1):
                fs += ", "
        fs += " attended this meeting!"
        
        if(len(attending) < 1):
            fs = "No one attended this meeting!"

        buttons = []
        if(not m['_id'] in self.userAttended and sgAttending):
            buttons.append({"name": "Request 'ATTENDED' Status", "color": "success"})
            buttons.append({"name": "Request 'EXCUSED' Status", "color": "primary"})
        
        MDApp.get_running_app().root.ids.action_box.addData(m['title'] + " (Past)", m['description'] + "\n\n" + str(m['length']) + " hours\n\n" + fs, buttons, self.handlePastOverlay)
        MDApp.get_running_app().root.ids.action_box.show()
        
        
        pass
    
    def sendRequest(self, finalRes):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.send_attendance_request(finalRes)
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : changePage("attendance"), 0)
    def handleUpcomingOverlay(self, buttonId):
        print("Handle this overlay")
        if(buttonId == 0):
            x = threading.Thread(target = self.sendRequest, args = ("EXCUSED",), daemon=True)
            x.start()
    def handlePastOverlay(self, buttonId):
        print("Handle this overlay")
        if(buttonId == 0):
            x = threading.Thread(target = self.sendRequest, args = ("ATTEND",), daemon=True)
            x.start()
        elif(buttonId == 1):
            x = threading.Thread(target = self.sendRequest, args = ("EXCUSED",), daemon=True)
            x.start()
    def addItems(self, mtgs, sgs, me):
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        now = datetime.now()
        self.ids.upcomingmeetings.clear_widgets()
        self.ids.pastmeetings.clear_widgets()
        self.user = me
        self.subgroups = sgs
        self.meetings = mtgs
        
        attended = []
        for a in me['attendance']:
            attended.append(a["event"])
        self.userAttended = attended
        for m in mtgs:
            dout = datetime.strptime(m["datetime"], f)
            
            if(dout > now):
                inMeeting = False
                for a in m["subgroups"]:
                    if(a in me['access']['groups']):
                        inMeeting = True
                        break
                
                
                sMI = SmallMeetingItem()
                sMI.ids.card.identifier = m['_id']
                sMI.ids.card.link = "upcoming"
                sMI.ids.card.bind(on_touch_down = self.triggerOverlay)
                sMI.ids.meeting_title.text = m['title']
                sMI.ids.meeting_datetime.text = str(dout.month) + "/" + str(dout.day) + " @ " + str(dout.hour - 12 if dout.hour > 12 else dout.hour) + ":" + str(dout.minute).zfill(2) + ("PM" if dout.hour >= 12 else "AM")
                if(inMeeting):
                    sMI.ids.meeting_status.icon = "calendar-check"
                    sMI.ids.meeting_status.text_color = self.getColor('success')
                else:
                    sMI.ids.meeting_status.icon = "calendar-remove"
                    sMI.ids.meeting_status.text_color = self.getColor('gray')
                
                self.ids.upcomingmeetings.add_widget(sMI)
            else:
                inMeeting = False
                for a in m["subgroups"]:
                    if(a in me['access']['groups']):
                        inMeeting = True
                        break
                
                attendedMeeting = m['_id'] in attended
                    
                
                sMI = SmallMeetingItem()
                sMI.ids.card.identifier = m['_id']
                sMI.ids.card.link = "past"
                sMI.ids.card.bind(on_touch_down = self.triggerOverlay)
                sMI.ids.meeting_title.text = m['title']
                sMI.ids.meeting_datetime.text = str(dout.month) + "/" + str(dout.day) + " @ " + str(dout.hour - 12 if dout.hour > 12 else dout.hour) + ":" + str(dout.minute).zfill(2) + ("PM" if dout.hour >= 12 else "AM")
                if(attendedMeeting):
                    sMI.ids.meeting_status.icon = "account-check"
                    sMI.ids.meeting_status.text_color = self.getColor('success')
                else:
                    if(inMeeting):
                        sMI.ids.meeting_status.icon = "alert-circle"
                        sMI.ids.meeting_status.text_color = self.getColor('red')
                    else:
                        sMI.ids.meeting_status.icon = "minus"
                        sMI.ids.meeting_status.text_color = self.getColor('gray')
                
                self.ids.pastmeetings.add_widget(sMI)
        
        
        pass
        
        
    
class Landing(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    def removeAllElements(self):
        rows = [i for i in self.ids.all_items.children]
        for r in rows:
            self.ids.all_items.remove_widget(r)
    # def showNewMember(self,d):
    #     MDApp.get_running_app().root.ids.input_box.addData("New Landing Item", "Create a new landing item to be visible to all members of the team!", [
    #         {"hint":"Username","multiline":False,"protected":False}
    #     ], self.handleNewMember)
    #     MDApp.get_running_app().root.ids.input_box.show()
    # def handleNewMember(self, data):
    #     print(data)
    #     x = threading.Thread(target = self.createItem, args = (data,), daemon=True)
    #     x.start()
    # def addMember(self, data):
    #     Clock.schedule_once(lambda x : toggle_message_box(True), 0)
    #     SCI.create_new_item(data[0], data[1], data[2])
    #     Clock.schedule_once(lambda x : toggle_message_box(False), 0)
    #     Clock.schedule_once(lambda x : changePage("landing"), 0)
    def showNewItem(self,d):
        MDApp.get_running_app().root.ids.input_box.addData("New Landing Item", "Create a new landing item to be visible to all members of the team!", [
            {"hint":"Title","multiline":False,"protected":False},
            {"hint":"Contents","multiline":True,"protected":False},
            {"hint":"Link To (optional)","multiline":False,"protected":False},
        ], self.handleNewItem)
        MDApp.get_running_app().root.ids.input_box.show()
    def handleNewItem(self, data):
        print(data)
        x = threading.Thread(target = self.createItem, args = (data,), daemon=True)
        x.start()
    def createItem(self, data):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.create_new_item(data[0], data[1], data[2])
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : changePage("landing"), 0)
    def showItems(self, r):
        self.removeAllElements()
        #self.ids.all_items.rows = 9
        self.ids.all_items.add_widget(EmptySpace())
        self.ids.all_items.add_widget(EmptySpace())
        
        
        admin = True
        
        
        
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
        if(admin):
            fL = FloatLayout(size_hint_y= None)
            b = IDButton(text="Add New Item", md_bg_color=self.getColor("primary"), color=self.getColor('white'), font_size="12sp", padding="12dp", pos_hint={"center_x":.5, "center_y":.5}, on_release=self.showNewItem)
            fL.add_widget(b)
            self.ids.all_items.add_widget(fL)
        for lpi in r[0]:
            #self.ids.all_items.rows += 4
            
            
            nW = LandingItem()
            
            
            nW.ids.title.text = lpi["title"]
            nW.ids.icon.icon = lpi["icon"]
            
            nW.ids.description.text = lpi["contents"]
            buttonsGone = 0

            if(not lpi["result"]["to"] == "link"):
                nW.ids.buttonspan.remove_widget(nW.ids.button)
                buttonsGone += 1
            else:
                nW.weblink = lpi["result"]["data"]
            
            if(not admin):
                nW.ids.buttonspan.remove_widget(nW.ids.deletebutton)
                buttonsGone += 1
            else:
                nW.moduleitemid = lpi["_id"]
                
            if(buttonsGone == 2):
                nW.ids.landingitem_content.remove_widget(nW.ids.buttonct)
            if("color" in lpi):
                try:
                    if("#" in lpi["color"]):
                        nW.ids.button.mg_bg_color = rgba255to1(hex_to_rgb(lpi["color"]))
                        nW.ids.icon.text_color = rgba255to1(hex_to_rgb(lpi["color"]))
                        print(rgba255to1(hex_to_rgb(lpi["color"])))
                    else:
                        nW.ids.button.mg_bg_color = self.getColor(lpi["color"])
                        nW.ids.icon.text_color = self.getColor(lpi["color"])
                    
                except:
                    pass
                
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
    def showResetPassword(self,d):
        MDApp.get_running_app().root.ids.input_box.addData("Reset Your Password", "You will need your old password to change your password to a new one. Please note that this will not sign out your other accounts!", [
            {"hint":"Current Password","multiline":False,"protected":True},
            {"hint":"New Password","multiline":False,"protected":True},
            {"hint":"Confirm New Password","multiline":False,"protected":True},
        ], self.handleResetPassword)
        MDApp.get_running_app().root.ids.input_box.show()
    def handleResetPassword(self, data):
        print(data)
        x = threading.Thread(target = self.resetPassword, args = (data,), daemon=True)
        x.start()
    def showError(self, title, error):
        MDApp.get_running_app().root.ids.action_box.addData(title, error, [])
        MDApp.get_running_app().root.ids.action_box.show()
    def resetPassword(self, data):
        
        if(not data[1] == data[2]):
            # show error   
            Clock.schedule_once(lambda x: self.showError("New Password Mismatch", "The new password you entered doesn't match the confirmation password."))
            return
        
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        result = SCI.reset_password(data[0], data[1])
        
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        if(not result):
            # show error
            Clock.schedule_once(lambda x: self.showError("Incorrect Password", "You can't change your password to something new if you don't know your previous one!"))
            return
        
    pass

class Splash(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass
class ClickableMDCard(MDCard):
    identifier = StringProperty()
    link = StringProperty()
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class Subgroup(Screen):
    def showNewItem(self):
        MDApp.get_running_app().root.ids.input_box.addData("New Subgroup Item", "Create a item that will only be visible to the " + self.subgroup["name"] + " subgroup", [
            {"hint":"Title","multiline":False,"protected":False},
            {"hint":"Contents","multiline":True,"protected":False},
            {"hint":"Link To (optional)","multiline":False,"protected":False},
        ], self.handleNewItem)
        MDApp.get_running_app().root.ids.input_box.show()
    def handleNewItem(self, data):
        print(data)
        x = threading.Thread(target = self.createItem, args = (data,), daemon=True)
        x.start()
    def createItem(self, data):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.create_new_item(data[0], data[1], data[2], self.subgroup["tag"])
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : changePage("subgroup"), 0)
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
        self.admin = sgD[1]
        self.users = users
        self.subgroup = sg
        self.meetings = meetings
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
        
        show = 10 if not self.admin else 20
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        now = datetime.now()
        
        self.ids.members.clear_widgets()
        self.ids.meetings.clear_widgets()
        self.ids.groupitems.clear_widgets()
        # if(show >= 10):
        #     l = Label(text="No upcoming meetings scheduled", italic=True, font_size="12dp", font_name="Roboto", color=self.getColor("secondary"))
        #     self.ids.meetings.add_widget(l)
        for u in users:
            if(sg["name"] in u["access"]["groups"]):
                mI = MemberItem()
                mI.ids.card.identifier = u["id"]
                mI.ids.card.link = "member"
                mI.ids.card.bind(on_touch_down=self.triggerOverlay)
                if(u["id"] in sg["managers"]):
                    mI.ids.username.text = "• " + u["username"]
                else:
                    mI.ids.username.text = u["username"]
                self.ids.members.add_widget(mI)
        print(items)
        for m in meetings:
            if(show > 0 and (sg["name"] in m["subgroups"] or self.admin)):
                dout = datetime.strptime(m["datetime"], f)
                if(dout > now):
                    mI = MeetingItem()
                    mI.ids.card.identifier = m["_id"]
                    mI.ids.card.link = "meeting"
                    mI.ids.card.opacity = 1 if (sg["name"] in m["subgroups"]) else 0.5
                    mI.ids.card.bind(on_touch_down=self.triggerOverlay)
                    mI.ids.title.text = m["title"]
                    
                    mI.ids.date.text = str(dout.month) + "/" + str(dout.day) + " @ " + str(dout.hour - 12 if dout.hour > 12 else dout.hour) + ":" + str(dout.minute).zfill(2) + ("PM" if dout.hour >= 12 else "AM")
                    self.ids.meetings.add_widget(mI)
                    show -= 1
        for i in items:
            lI = LandingItem()
            lI.ids.title.text = i["title"]
            lI.ids.icon.icon = i["icon"]
            lI.ids.description.text = i["contents"]
            if("color" in i):
                try:
                    if("#" in i["color"]):
                        lI.ids.button.mg_bg_color = rgba255to1(hex_to_rgb(i["color"]))
                        lI.ids.icon.text_color = rgba255to1(hex_to_rgb(i["color"]))
                        print(rgba255to1(hex_to_rgb(i["color"])))
                    else:
                        lI.ids.button.mg_bg_color = self.getColor(i["color"])
                        lI.ids.icon.text_color = self.getColor(i["color"])
                except:
                    pass
            buttonsGone = 0

            if(not i["result"]["to"] == "link"):
                lI.ids.buttonspan.remove_widget(lI.ids.button)
                buttonsGone += 1
            else:
                lI.weblink = i["result"]["data"]
            
            if(not self.admin):
                lI.ids.buttonspan.remove_widget(lI.ids.deletebutton)
                buttonsGone += 1
            else:
                lI.moduleitemid = i["_id"]
                
            if(buttonsGone == 2):
                lI.ids.landingitem_content.remove_widget(lI.ids.buttonct)
                
                
                
            if(i["contents"] == ""):
                lI.ids.landingitem_content.remove_widget(lI.ids.description)
            self.ids.groupitems.add_widget(lI)
    def triggerOverlay(self, *args):
        card = args[0]
        touch = args[1]
        if(not card.collide_point(touch.x, touch.y)):
            return
        
        if(not type(card) is ClickableMDCard):
            return
        
        link = card.link
        
        if(link == "member"):
            self.showMemberOverlay(card)
        elif(link == "meeting"):
            self.showMeetingOverlay(card)
    def showMemberOverlay(self, *args):
        
        card = args[0]
        
        buttons = [{"name" : "Account", "color": "primary"}]
        
        u = next(x for x in self.users if x["id"] == card.identifier)
        self.member = u
        if(self.admin and not u["id"] in self.subgroup["managers"]):
            buttons.append({"name" : "Kick", "color": "red"})
        
        username = ("• " if u["id"] in self.subgroup['managers'] else "") + u["username"]
        
        MDApp.get_running_app().root.ids.action_box.addData(username, u["fullname"] + "\nThis user is in " + str(len(u['access']['groups'])) + " subgroups\nThey have 400 protons", buttons, self.handleMemberOverlay)
        MDApp.get_running_app().root.ids.action_box.show()
    def handleMemberOverlay(self, buttonId):
        print(buttonId)
        if(buttonId == 0):
            changePage("account")
            # TODO, show account page of actual user selected
        elif(buttonId == 1):
            x = threading.Thread(target = self.removeMember, args = (self.member["id"],), daemon=True)
            x.start()
            pass
    def showLeaveOverlay(self):
        MDApp.get_running_app().root.ids.action_box.addData("Are You Sure?", "You won't be able to join back unless the subgroup is public, or a Subgroup Leader invites you back!", [{"name" : "Leave", "color": "red"}], self.handleLeaveOverlay)
        MDApp.get_running_app().root.ids.action_box.show()
    def handleLeaveOverlay(self, buttonId):
        if(buttonId == 0):
            pass
            x = threading.Thread(target = self.removeMember, args = (SCI.account["id"],), daemon=True)
            x.start()
            print("Leave subgroup here")
    def showMeetingOverlay(self, *args):
        card = args[0]
        buttons = []
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        
        print(self.meetings)
        m = next(x for x in self.meetings if x["_id"] == card.identifier)
        dout = datetime.strptime(m["datetime"], f)
        self.selectedMeeting = m
        if(self.admin):
            if not self.subgroup['name'] in self.selectedMeeting['subgroups']:
                buttons.append({"name" : "We Are Attending", "color": "primary"})
            else:
                buttons.append({"name" : "We Aren't Attending", "color" : "red"})
        
        MDApp.get_running_app().root.ids.action_box.addData(m['title'], "on " + str(dout.month) + "/" + str(dout.day) + "/" + str(dout.year) + " @ " + str(dout.hour - 12 if dout.hour > 12 else dout.hour) + ":" + str(dout.minute).zfill(2) + ("PM" if dout.hour >= 12 else "AM") + "\n\n" + m["description"] + "\n\n" + str(len(m["subgroups"])) + " subgroups attending", buttons, self.handleMeetingOverlay)
        MDApp.get_running_app().root.ids.action_box.show()
    def handleMeetingOverlay(self, buttonId):
        if(buttonId == 0):
            pass
            action = "remove"
            if not self.subgroup['name'] in self.selectedMeeting['subgroups']:
                action = "add"
            x = threading.Thread(target = self.changeAttendance, args = (action,), daemon=True)
            x.start()
            
    def changeAttendance(self, action):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.change_subgroup_attendance(self.subgroup, self.admin, self.selectedMeeting, action)
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : changePage("subgroup"), 0)
    def removeMember(self, memberId):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.remove_subgroup_member(self.subgroup, self.admin, memberId)
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : changePage("subgroup"), 0)
        
    pass

class WindowManager(ScreenManager):
    
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)


class Main(MDApp):
    def getColor(self, name):
        return COLORS[name.lower()]
    
    def build(self):
        global COLORS
        SCI.initialize()
        SETTINGS.initialize()
        
        # if(SETTINGS.settings["color_scheme"] == "light"):
        #     COLORS = {
        #         "primary": rgba255to1((19, 3, 252,1)),
        #         "secondary": rgba255to1((7, 0, 105,1)),
        #         "light": rgba255to1((130, 207, 255,1)),
        #         "white": rgba255to1((255, 255, 255,1)),
        #         "gray" : rgba255to1((100, 100, 100,1)),
        #         "black": rgba255to1((0, 0, 0,1)),
        #         "success": rgba255to1((0, 200, 0,1)),
        #         "red": rgba255to1((255, 0, 0,1)),
        #         "green": rgba255to1((0, 255, 0,1)),
        #         "blue": rgba255to1((0, 0, 255,1))
        #     }
        # elif(SETTINGS.settings["color_scheme"] == "dark"):
        #     COLORS = {
        #         "primary": rgba255to1((19, 3, 252,1)),
        #         "secondary": rgba255to1((7, 0, 105,1)),
        #         "light": rgba255to1((130, 207, 255,1)),
        #         "white": rgba255to1((50, 50, 50,1)),
        #         "gray" : rgba255to1((150, 150, 150,1)),
        #         "black": rgba255to1((255, 255, 255,1)),
        #         "success": rgba255to1((0, 200, 0,1)),
        #         "red": rgba255to1((255, 0, 0,1)),
        #         "green": rgba255to1((0, 255, 0,1)),
        #         "blue": rgba255to1((80, 80, 255,1))
        #     }
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