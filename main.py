

from kivy.lang import Builder
from datetime import datetime, timedelta
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty, BooleanProperty
# import kivy label
from kivy.uix.label import Label
from kivymd.uix.textfield import MDTextField
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.picker import MDDatePicker, MDTimePicker
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
from kivy.utils import platform

import kivy
from kivy.clock import Clock
from actions import SparkClub
import kivy.uix.screenmanager as t
from kivy.storage.jsonstore import JsonStore
import webbrowser
import threading
#from kivy.utils import platform

from kivy.config import Config
from settings import AppSettings
Config.set('graphics', 'fullscreen', '0')
Config.set("graphics", "resizable", 0)

from plyer import vibrator

if(platform == "ios"):
    from pyobjus import autoclass, objc_dict

window_size = [600,600]
def getDSTOffset():
    return -4

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
            "view-list": ["Home", "landing"],
            "checkbox-marked-circle-outline": ["Meetings", "attendance"],
            "forum": ["Communications", "cable"],
            "account-circle": ["My Account", "account"]
        }
class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))
    def clickItem(self):
        global inPopup
        inPopup = False
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





    
def changeTitleVisibility(show):
    fadeto(MDApp.get_running_app().root.ids.title_card, 1 if show else 0, 0.1)

def changePage(page):
    MDApp.get_running_app().root.ids.window_manager.transition = t.RiseInTransition(duration=.3)
    MDApp.get_running_app().root.ids.window_manager.current = page
    try:
        pageScrollers[MDApp.get_running_app().root.ids.window_manager.current].scroll_y = 1
    except:
        pass
    if(page == "landing"):
        MDApp.get_running_app().root.ids.nav_bar_title.text = "Landing Page"
        x = threading.Thread(target = MDApp.get_running_app().root.ids.landingpage.addItems, args = (), daemon=True)
        x.start()
        
        MDApp.get_running_app().root.ids.nav_bar.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        #Clock.schedule_once(MDApp.get_running_app().root.ids.landingpage.addItems, 0)
        
        MDApp.get_running_app().root.ids.content_drawer.trigger_login()
        
    elif(page == "actions"):
        MDApp.get_running_app().root.ids.nav_bar_title.text = "Actions"
        Clock.schedule_once(MDApp.get_running_app().root.ids.actionspage.addItems, 0)
    elif(page == "subgroup"):
        MDApp.get_running_app().root.ids.nav_bar.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  
        
        x = threading.Thread(target = MDApp.get_running_app().root.ids.subgrouppage.subgroupInfo, args = (), daemon=True)
        x.start()
        MDApp.get_running_app().root.ids.nav_bar_title.text = "Subgroup (" + subgroup + ")"
        
    elif(page == "login"):
        MDApp.get_running_app().root.ids.nav_bar_title.text = "You Shouldn't See This..."
        MDApp.get_running_app().root.ids.nav_bar.pos_hint = {'center_x': 0.5, 'center_y': 10}
        SCI.logout()
    elif(page == "error"):
        MDApp.get_running_app().root.ids.nav_bar_title.text = "You Shouldn't See This..."
        MDApp.get_running_app().root.ids.nav_bar.pos_hint = {'center_x': 0.5, 'center_y': 10}
    elif(page == "account"):
        MDApp.get_running_app().root.ids.nav_bar_title.text = "My Account"
        MDApp.get_running_app().root.ids.accountpage.setup()
    elif(page == "attendance"):
        MDApp.get_running_app().root.ids.nav_bar_title.text = "Meeting Schedule"
        MDApp.get_running_app().root.ids.attendancepage.show()
    elif(page == "meeting"):
        MDApp.get_running_app().root.ids.nav_bar_title.text = "Specific Meeting"
        MDApp.get_running_app().root.ids.meetingpage.init()
    elif(page == "cable"):
        MDApp.get_running_app().root.ids.nav_bar_title.text = "Communications"
        MDApp.get_running_app().root.ids.cablepage.init()

        
    
        
pageScrollers = {}

def checkScroll(b):
    
    try:
        
        changeTitleVisibility(pageScrollers[MDApp.get_running_app().root.ids.window_manager.current].scroll_y > 0.90)
    except:
        if(MDApp.get_running_app().root.ids.window_manager.current == "cable"):
            changeTitleVisibility(True)
        else:
            changeTitleVisibility(False)
        pass

Clock.schedule_interval(checkScroll, 0.1)

def getLandingPageItems():
    Clock.schedule_once(lambda x : toggle_message_box(True), 0)
    i = SCI.get_items("H")
    m = SCI.get_meeting_today()
    p = SCI.get_protons()
    s = SCI.get_subgroups()
    Clock.schedule_once(lambda x : toggle_message_box(False), 0)
    return (i, m, p, s)
 
 
initialPage = "landing"

def handleLogin(token, data={}):
    if(token):
        if(SCI.try_login_with_key()):
            #changePage("landing")
            Clock.schedule_once(lambda x: changePage(initialPage), 0)
            MDApp.get_running_app().setUserId(SCI.account['id'], SCI.account['username'])
            
            
        else:
            Clock.schedule_once(lambda x: changePage("login"), 0)
    else:
        res = SCI.login(data["username"], data["password"])
        if(res):
            Clock.schedule_once(lambda x: changePage(initialPage), 0)
            
            MDApp.get_running_app().setUserId(SCI.account['id'], SCI.account['username'])
            
        else:
            Clock.schedule_once(lambda x: MDApp.get_running_app().root.ids.loginpage.showWrongInformation(), 0)
            
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
        #print(successful)
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


thisMeeting = ""
class Meeting(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    def getItems(self):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        u = SCI.get_users()
        s = SCI.get_subgroups()
        m = SCI.get_meetings()
        me = SCI.get_this_user()
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : self.addItems(u, s, m, me), 0)
    def addItems(self, u, s, m, me):
        print(thisMeeting)
        tM = next(x for x in m if x["_id"] == thisMeeting)
        
        
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        dout = datetime.strptime(tM["datetime"], f)
        dout = dout + timedelta(hours=getDSTOffset())
        
        
        attending = []
        managingSubgroups = []
        for subgroup in s:
            if(me["id"] in subgroup["managers"]):
                managingSubgroups.append(subgroup)
            if(subgroup["name"] in tM["subgroups"]):
                attending.append(subgroup["name"])
        
        fs = ""
        sgAttending = False
        for i in range(0, len(attending)):
            
            fs += attending[i]
            if(i != len(attending) - 1):
                fs += ", "
        fs += " are attending this meeting!"
        
        if(len(attending) < 1):
            fs = "No one is attending this meeting!"
            
        useUsers = []
        for user in u:
            doesManage = False
            for subgroup in managingSubgroups:
                if(subgroup["name"] in user['access']['groups']):
                    doesManage = True
                    break
            if(doesManage or SCI.permissionCheck(["ADMIN_SCHEDULE_ATTENDENCE_CONFIRM"]) or SCI.permissionCheck(["ADMIN_SCHEDULE_ATTENDENCE"])):
                useUsers.append(user)
        
        useUsers.sort(key=lambda x: x["name"])
        self.ids.meeting_title_datetime.text = tM['title'] + " on " + str(dout.month) + "/" + str(dout.day) + " @ " + str(dout.hour - 12 if dout.hour > 12 else dout.hour) + ":" + str(dout.minute).zfill(2) + ("PM" if dout.hour >= 12 else "AM")
        self.ids.meeting_description.text = tM['description']
        self.ids.meeting_attending.text = fs
        self.ids.statuses.clear_widgets()
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        now = datetime.now()
        dout = datetime.strptime(tM["datetime"], f)
        dout = dout + timedelta(hours=getDSTOffset())
        for user in useUsers:
            
            attendanceItem = None
            for aI in user['attendance']:
                if(aI['event'] == thisMeeting):
                    attendanceItem = aI
                    break
            
            
            
            
            mS = MemberStatus()
            mS.uid = user["id"]
            
            request = None
            
            if("requests" in tM):
                for r in tM["requests"]:
                    try:
                        if(r["requester"] == user["id"]):
                            request = r
                            break
                    except:
                        pass
            
            if(not attendanceItem == None):
                
                
                
                
                mS.init(attendanceItem["overriddenstatus"], request["final"] if request != None else "", dout > now)
                
                if(request != None):
                    mS.ids.status_request.text = "Requesting " + request["final"]
                    mS.ids.status_request.color = self.getColor("red")
                else:
                    mS.ids.content.remove_widget(mS.ids.status_request)
                
                if(attendanceItem["status"] != ""):
                    mS.ids.status_current.text = "Currently " + attendanceItem["status"]
                else:
                    mS.ids.status_current.text = "Currently *" + attendanceItem["overriddenstatus"]
            else:
                
                mS.ids.status_current.text = "No Record..."
                mS.init("", request["final"] if request != None else "", dout > now)
            
            mS.ids.status_member.text = user['username'] + " (" + user["fullname"] + ")"
            
            self.ids.statuses.add_widget(mS)
        
            
    def init(self):
        x = threading.Thread(target = self.getItems, args = (), daemon=True)
        x.start()
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
        
    def actualHide(self):
        global inPopup
        self.pos_hint = {'center_x': 0.5, 'center_y': 10}
        inPopup = False
        
    def hide(self):
        #print("HIDE")
        fadeto(self, 0, .2)
        Clock.schedule_once(lambda x : self.actualHide(), .2)
        
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
        #print("Action Performed: " + str(buttonId))
        if(buttonId == -1):
            self.hide()
        else:
            self.callback(buttonId)
            self.hide()
        
        
    
    pass

class DateTimeBox(FloatLayout):
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
    def actualHide(self):
        global inPopup
        self.pos_hint = {'center_x': 0.5, 'center_y': 10}
        
    def hide(self):
        #print("HIDE")
        fadeto(self, 0, .2)
        Clock.schedule_once(lambda x : self.actualHide(), .2)
        
    def addData(self, title, contents, callback=None):
        if(inPopup):
            return
        # Each callback should have an argument for the buttonid
        self.ids.title.text = title
        self.ids.contents.text = contents
        self.ids.submit_button.disabled = True
        self.date = None
        self.time = None
        self.items = [False, False, False, False, False]
        #self.ids.date_button.text = "Pick Date"
        #self.ids.time_button.text = "Pick Time"
        
        self.callback = callback
    def validateComponent(self, component, l, min, max, i):
        if(len(component.text) > l):
            component.text = component.text[:l]
        try:
            val = int(component.text)
            if(val < min or val > max):
                raise Exception()
            component.text_color = self.getColor('primary')
            self.items[i] = True
            if(len(component.text) == l):
                return True
        except:
            component.text_color = self.getColor('red')
            self.items[i] = False
            pass
        return False
    def checkEntries(self):
        for i in self.items:
            if(not i):
                self.ids.submit_button.disabled = True
                return
        self.ids.submit_button.disabled = False
    def dateChange(self, type):
        if(type == "M"):
            
            n = self.validateComponent(self.ids.m_date,2, 1, 12, 0)
            if(n):
                self.ids.m_date.focus = False
                self.ids.d_date.focus = True
            self.checkEntries()
        elif(type == "D"):
            
            n = self.validateComponent(self.ids.d_date,2, 1, 31, 1)
            if(n):
                self.ids.d_date.focus = False
                self.ids.y_date.focus = True
            self.checkEntries()
        elif(type == "Y"):
            
            n = self.validateComponent(self.ids.y_date, 4, 2020, 2024, 2)
            if(n):
                self.ids.y_date.focus = False
            self.checkEntries()
    def timeChange(self, type):
        if(type == "H"):
            
            n = self.validateComponent(self.ids.h_time,2, 1, 24, 3)
            if(n):
                self.ids.h_time.focus = False
                self.ids.m_time.focus = True
            self.checkEntries()
        elif(type == "M"):
            
            n = self.validateComponent(self.ids.m_time,2, 0, 59, 4)
            if(n):
                self.ids.h_time.focus = False
                self.ids.m_time.focus = True
            else:
                self.items[4] = False
            self.checkEntries()
    def performAction(self, *args):
        global inPopup
        buttonId = args[0].buttonid
        #print("Action Performed: " + str(buttonId))
        if(buttonId == 0):
            date = self.ids.y_date.text + "-" + self.ids.m_date.text + "-" + self.ids.d_date.text
            time = str(int(self.ids.h_time.text)-getDSTOffset()) + ":" + self.ids.m_time.text + ":00"
            self.hide()
            inPopup = False
            self.callback(date, time)
        else:
            inPopup = False
            self.hide()
        
    def showDate(self):
        date_dialog = MDDatePicker(primary_color=self.getColor("secondary"))
        date_dialog.bind(on_save=self.saveDate)
        date_dialog.open()
    def saveDate(self, i, val,r):
        self.date = val
        self.ids.date_button.text = str(val)
        self.ids.date_button.mg_bg_color = self.getColor('success')
        if(self.date != None and self.time != None):
            self.ids.submit_button.disabled = False
    def showTime(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(on_save=self.saveTime)
        time_dialog.open()
    def saveTime(self, i, val):
        self.time = val
        self.ids.time_button.text = str(val)
        self.ids.time_button.mg_bg_color = self.getColor('success')
        if(self.date != None and self.time != None):
            self.ids.submit_button.disabled = False
    
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
        print("SHOW INPUTBOX", inPopup)
        if(inPopup):
            return
        self.opacity = 0
        inPopup = True
        
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        fadeto(self, 1, .2)
        #vibrate(0.4)

    def actualHide(self):
        global inPopup
        self.pos_hint = {'center_x': 0.5, 'center_y': 10}
        inPopup = False
        
    def hide(self):
        #print("HIDE")
        fadeto(self, 0, .2)
        Clock.schedule_once(lambda x : self.actualHide(), .2)
        
    def addData(self, title, contents, inputs, callback=None):
        global inPopup
        if(inPopup):
            return
        
        # Each callback should have an argument for the buttonid
        self.ids.title.text = title
        self.ids.contents.text = contents
        
        self.ids.inputs.clear_widgets()
        self.callback = callback
        self.data = []
        self.dropdowns = {}
        self.items = {}
        n = 0
        for b in inputs:
            if(b["type"] == "input"):
                hint = b["hint"]
                multiline = b["multiline"]
                protected = b["protected"]
                id = "form" + str(n)
                text = "" if not "value" in b else b["value"]
                i = IDInput(inputid=n,multiline=multiline, password=protected, line_color_focus= self.getColor('primary'),line_color_normal= self.getColor('primary'), color_mode= 'custom', active_line=True, hint_text=hint, font_name= 'Roboto', border=(2,2,2,2), spacing=(20,20,20,20), padding=(20,20,20,20),border_color= (0,0,0,1), max_height="100dp", text=text)
                i.bind(text=self.changeText)
                i.line_color_focus = self.getColor('primary')
                self.items[str(n)] = i
                self.ids.inputs.add_widget(i)
            elif(b["type"] == "dropdown"):
                hint = b["hint"]
                color = b["color"]
                options = b["options"]
                icons = b["icons"]
                
                items = []
                
                for o in options:
                    items.append({
                        "text": o,
                        "viewclass": "OneLineListItem",
                        "on_release": lambda x=o, y=n: self.handleDropdown(x, y)
                    })
                
                id = "form" + str(n)
                fL = FloatLayout(size_hint=(1,None))
                
                
                '''
                MDFillRoundFlatButton:
                        text: "Join"
                        id: action_button
                        on_release: root.showLeaveOverlay()
                        md_bg_color: root.getColor('primary')
                        color: root.getColor('white')'''
                b = IDButton(text=hint, buttonid=n, md_bg_color=color, color=self.getColor('white'), on_release=(lambda x=n: self.openDropdown(x)), pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size="12sp", font_name= 'Roboto', padding="12dp")
                fL.height = b.height
                fL.add_widget(b)
                dD = MDDropdownMenu(caller=b, items=items, width_mult=3)
                self.items[str(n)] = b
                self.dropdowns[str(n)] = dD
                
                self.ids.inputs.add_widget(fL)
            n+=1
            text = ""
            try:
                text = "" if not "value" in b else b["value"]
            except:
                pass
            self.data.append(text)
    def openDropdown(self, key):

        self.dropdowns[str(key.buttonid)].open()
    def handleDropdown(self, item, index):
        self.dropdowns[str(index)].dismiss()
        self.items[str(index)].text = "Selected: " + item
        self.data[index] = item
        
    def changeText(self, *args):
        inputId = args[0].inputid
        #print("changed text: " + str(inputId))
        self.data[inputId] = args[0].text
    def performAction(self, *args):
        global inPopup
        buttonId = args[0].buttonid
        if(buttonId == -1):
            self.hide()
        else:
            self.callback(self.data)
            self.hide()
        
            
    
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
    admin = NumericProperty(0)
    moduleitemid = StringProperty("")
    def getColor(self, name):
        return COLORS[name.lower()]
    def openLink(self):
        #print(self.weblink)
        
        webbrowser.open(self.weblink)
        #print("A")
        
    def handleConfirmation(self, buttonId):
        global inPopup
        if(buttonId == 0):
            self.deleteItem()
        elif(buttonId == 1):
            thisLandingItem = next(x for x in allLandingItems if x["_id"] == self.moduleitemid)
            inPopup = False
            MDApp.get_running_app().root.ids.input_box.addData("Edit Landing Item", "Please input the edited values that you want for this landing item!", [
                {"hint":"Title","multiline":False,"protected":False, "type":"input", "value": thisLandingItem["title"]},
                {"hint":"Contents","multiline":True,"protected":False, "type":"input", "value": thisLandingItem["contents"]},
                {"hint":"Link","multiline":False,"protected":False, "type":"input", "value": thisLandingItem["result"]["data"]}
            ], self.handleEdit)
            MDApp.get_running_app().root.ids.input_box.show()
    
    def handleEdit(self, data):
        #print(data)
        self.context = MDApp.get_running_app().root.ids.window_manager.current
        x = threading.Thread(target = self.bgHandleEdit, args = (data[0], data[1], data[2]), daemon=True)
        x.start()
    def bgHandleEdit(self, title, contents, linkto):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.edit_item(self.moduleitemid, title, contents, linkto)
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : changePage(self.context), 0)
    def handleInfo(self, buttonId):
        pass
    def showInfo(self):
        thisLandingItem = next(x for x in allLandingItems if x["_id"] == self.moduleitemid)
        buttons = []
        if(self.admin == 1):
            buttons.append({"name":"Delete", "color":"red"})
            buttons.append({"name":"Edit", "color":"primary"})
            
        
        MDApp.get_running_app().root.ids.action_box.addData(thisLandingItem['title'], thisLandingItem['contents'], buttons, self.handleConfirmation)
        MDApp.get_running_app().root.ids.action_box.show()
    def deleteItem(self):
        self.context = MDApp.get_running_app().root.ids.window_manager.current
        MDApp.get_running_app().root.ids.action_box.addData("Are You Sure?", "This will delete the Landing Item for EVERYONE, not just you seeing it!", [{"name" : "Delete", "color": "red"}], self.handleConfirmDelete)
        MDApp.get_running_app().root.ids.action_box.show()
    def handleConfirmDelete(self):
        x = threading.Thread(target = self.bgDeleteItem, args = (self.moduleitemid,), daemon=True)
        x.start()
    def bgDeleteItem(self, id):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.remove_item(id)
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : changePage(self.context), 0)
        
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

class Message(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass

class MyMessage(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass


class MemberStatus(FloatLayout):
    uid = StringProperty()

    def getColor(self, name):
        return COLORS[name.lower()]
    
    def sendToServer(self, override):
        res = SCI.send_override(thisMeeting, self.uid, override)


    def reAddButtons(self):
        self.ids.status_buttons.clear_widgets()
        
        attend = MDIconButton(icon="account-check", size_hint_x= None,theme_text_color= "Custom",text_color= self.getColor('white'), md_bg_color= self.getColor('success' if self.chosen.lower() == "attend" else ("orange" if self.requested.lower() == "attend" else "lightgray")), on_release=lambda x: self.selectStatus("attend"), font_size="12sp", padding="12dp")
        excused = MDIconButton(icon="minus", size_hint_x= None,theme_text_color= "Custom",text_color= self.getColor('white'), md_bg_color= self.getColor('gray' if self.chosen.lower() == "excused" else ("orange" if self.requested.lower() == "excused" else "lightgray")), on_release=lambda x: self.selectStatus("excused"), font_size="12sp", padding="12dp")
        absent = MDIconButton(icon="alert-circle", size_hint_x= None,theme_text_color= "Custom",text_color= self.getColor('white'), md_bg_color= self.getColor('red' if self.chosen.lower() == "absent" else "lightgray"), on_release=lambda x: self.selectStatus("absent"), font_size="12sp", padding="12dp", disabled= self.future)
        
        self.ids.status_buttons.add_widget(attend)
        self.ids.status_buttons.add_widget(excused)
        self.ids.status_buttons.add_widget(absent)
        

    def init(self, initial, requested, future):
        self.chosen = initial.lower()
        self.future = future
        
        self.requested = requested
        self.reAddButtons()

    


    def selectStatus(self, type):
        if(type == self.chosen):
            self.chosen = ""
        else:
            self.chosen = type
        self.reAddButtons()
            
        x = threading.Thread(target = self.sendToServer, args = (self.chosen,), daemon=True)
        x.start()





class Login(Screen):
   
    
    def submitForm(self):
        #print("Submitted form!")
        x = threading.Thread(target = handleLogin, args = (False,{"username": self.ids.username.text, "password" : self.ids.password.text},), daemon=True)
        x.start()
    def showWrongInformation(self):
        
        try:
            if(platform == "android" or platform == "ios"):
                vibrator.vibrate(0.2)
        except:
            pass
        MDApp.get_running_app().root.ids.action_box.addData("Incorrect Login", "Your username or password is incorrect! Please double check you are entering it in correctly!", [])
        MDApp.get_running_app().root.ids.action_box.show()
        
        pass
    
    def getColor(self, name):
        return COLORS[name.lower()]
    def goToTempLogin(self):
        if(not inPopup):
            #print("Go to temp login")
            self.ids.login_page.pos_hint = {'center_x': 0.5, 'center_y': 10}
            self.ids.temp_page.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    def goToCreate(self):
        if(not inPopup):
            #print("Go to temp login")
            self.ids.login_page.pos_hint = {'center_x': 0.5, 'center_y': 10}
            self.ids.create_page.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    def goToLogin(self):
        if(not inPopup):
            #print("Go to temp login")
            self.ids.login_page.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            self.ids.temp_page.pos_hint = {'center_x': 0.5, 'center_y': 10}
            self.ids.create_page.pos_hint = {'center_x': 0.5, 'center_y': 10}
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
    def createPageInputChange(self):
        if(self.ids.create_username.text != "" and self.ids.create_fullname.text != "" and self.ids.create_email.text != "" and self.ids.create_external_id.text != "" and self.ids.create_password.text != "" and "@" in self.ids.create_email.text):
            self.ids.create_submit.disabled = False
        else:
            self.ids.create_submit.disabled = True
    def externalIDChange(self):
        if(self.ids.external_id.text == ""):
            self.ids.external_submit.disabled = True
        else:
            self.ids.external_submit.disabled = False
    def apiExternalSubmit(self, externalId):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.try_external_login(externalId)
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : self.goToLogin(), 0)
    def externalSubmit(self):
        externalId = self.ids.external_id.text
        x = threading.Thread(target = self.apiExternalSubmit, args = (externalId,), daemon=True)
        x.start()
    def apiCreateAccount(self, u, fn, e, eid, pw):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        res = SCI.try_create_account(u, fn, e, eid, pw)
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : self.handleCreateAccount(res), 0)
    def handleCreateAccount(self, res):
        if(res[0] == True):
            Clock.schedule_once(lambda x: changePage(initialPage), 0)
            MDApp.get_running_app().setUserId(SCI.account['id'], SCI.account['username'])
        else:
            try:
                if(platform == "android" or platform == "ios"):
                    vibrator.vibrate(0.2)
            except:
                pass
            MDApp.get_running_app().root.ids.action_box.addData("Error Creating Account", res[1]["message"], [])
            MDApp.get_running_app().root.ids.action_box.show()
    def createSubmit(self):
        username = self.ids.create_username.text
        fullname = self.ids.create_fullname.text
        email = self.ids.create_email.text
        external_id = self.ids.create_external_id.text
        password = self.ids.create_password.text
        x = threading.Thread(target = self.apiCreateAccount, args = (username, fullname, email, external_id, password,), daemon=True)
        x.start()
        
        
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
    def perform_ui_error(self, details):
        global inPopup
        MDApp.get_running_app().root.ids.errorpage.ids.details.text = details
        changePage("error")
        MDApp.get_running_app().root.ids.input_box.hide()
        MDApp.get_running_app().root.ids.action_box.hide()
        toggle_message_box(False)
        inPopup = False
        
        
    def show_error(self, errorDetails):
        Clock.schedule_once(lambda x : self.perform_ui_error(errorDetails), 0)
        

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
        global pageScrollers
        pageScrollers["attendance"] = self.ids.scroller
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
        if(not inPopup):
            self.use = card.identifier
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
        fs += " are attending this meeting!" + (" You are expected to attend!" if sgAttending else "")
        
        if(len(attending) < 1):
            fs = "No one is attending this meeting yet!"
        
        buttons = [{"name" : "Show Meeting Page", "color": "primary"}]
        if(sgAttending):
            buttons.append({"name": "Request EXCUSED", "color": "primary"})
        
        MDApp.get_running_app().root.ids.action_box.addData(m['title'], m['description'] + "\n\n" + str(m['length']) + " hours\n\n" + fs, buttons, self.handleUpcomingOverlay)
        MDApp.get_running_app().root.ids.action_box.show()
        
        
        pass
    
    def showNewMeeting(self):
        MDApp.get_running_app().root.ids.datetime_box.addData("Select Date/Time", "Every good meeting has to have a date and a time, or else no one will know when to show!", self.handleSelectDateTime)
        MDApp.get_running_app().root.ids.datetime_box.show()
    def handleSelectDateTime(self, date, time):
        
        global inPopup
        
        
        print(date, time)
        if(date == None or time == None):
            return
        self.date = date
        self.time = time
        inPopup = False
        
        MDApp.get_running_app().root.ids.input_box.addData("New Meeting", "Please describe the meeting that you are creating for the datetime below\n" + str(date) + " " + str(time), [
            {"hint":"Name","multiline":False,"protected":False, "type":"input"},
            {"hint":"Purpose","multiline":True,"protected":False, "type":"input"},
            {"hint":"Length (in hours)","multiline":False,"protected":False, "type":"input"}
        ], self.handleMeetingDetails)
        MDApp.get_running_app().root.ids.input_box.show()
    def createMeeting(self, title, description, length, datetime):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.new_meeting(title, description, length, datetime)
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : changePage("attendance"), 0)
    def reShowInput(self):
        MDApp.get_running_app().root.ids.input_box.addData("New Meeting", "Make sure you fill out all fields with appropriate values!\n" + str(self.date) + " " + str(self.time), [
            {"hint":"Name","multiline":False,"protected":False, "type":"input"},
            {"hint":"Purpose","multiline":True,"protected":False, "type":"input"},
            {"hint":"Length (in hours)","multiline":False,"protected":False, "type":"input"}
        ], self.handleMeetingDetails)
        MDApp.get_running_app().root.ids.input_box.show()
    def handleMeetingDetails(self, data):
        global inPopup
        
        try:
            if(data[0] == "" or data[1] == ""):
                raise Exception()
            if(int(data[2]) < 1):
                raise Exception()
            datetimeObject = datetime.strptime(str(self.date) + " " + str(self.time), '%Y-%m-%d %H:%M:%S')
            
            inPopup = False
            x = threading.Thread(target = self.createMeeting, args = (data[0], data[1], int(data[2]), datetimeObject), daemon=True)
            x.start()
        except:
            inPopup = False
            
            Clock.schedule_once(lambda x : self.reShowInput(), 0.2)
            
            
            pass
    def showPastOverlay(self, card):
        if(not inPopup):
            self.use = card.identifier
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

        buttons = [{"name" : "Show Meeting Page", "color": "primary"}]
        if(not m['_id'] in self.userAttended and sgAttending):
            buttons.append({"name": "Request ATTENDED", "color": "success"})
            buttons.append({"name": "Request EXCUSED", "color": "primary"})
        
        MDApp.get_running_app().root.ids.action_box.addData(m['title'] + " (Past)", m['description'] + "\n\n" + str(m['length']) + " hours\n\n" + fs, buttons, self.handlePastOverlay)
        MDApp.get_running_app().root.ids.action_box.show()
        
        
        pass
    
    def sendRequest(self, finalRes, useMeeting):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.send_attendance_request(finalRes, useMeeting)
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : changePage("attendance"), 0)
    def handleUpcomingOverlay(self, buttonId):
        global thisMeeting
        #print("Handle this overlay")
        if(buttonId == 0):
            thisMeeting = self.use
            changePage("meeting")
        elif(buttonId == 1):
            x = threading.Thread(target = self.sendRequest, args = ("EXCUSED",self.use), daemon=True)
            x.start()
    def handlePastOverlay(self, buttonId):
        global thisMeeting
        #print("Handle this overlay")
        if(buttonId == 0):
            thisMeeting = self.use
            changePage("meeting")
        elif(buttonId == 1):
            x = threading.Thread(target = self.sendRequest, args = ("ATTEND",self.use), daemon=True)
            x.start()
        elif(buttonId == 2):
            x = threading.Thread(target = self.sendRequest, args = ("EXCUSED",self.use), daemon=True)
            x.start()
    def addItems(self, mtgs, sgs, me):
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        now = datetime.now()
        self.ids.upcomingmeetings.clear_widgets()
        self.ids.pastmeetings.clear_widgets()
        self.user = me
        self.subgroups = sgs
        self.meetings = mtgs
        
        if(not SCI.permissionCheck(["ADMIN_SCHEDULE"])):
            self.ids.new_meeting.disabled = True
        else:
            self.ids.new_meeting.disabled = False
        
        attended = []
        for a in me['attendance']:
            attended.append(a["event"])
        self.userAttended = attended
        mtgs.sort(key=lambda x: datetime.strptime(x["datetime"], f), reverse=True)
        for m in mtgs:
            dout = datetime.strptime(m["datetime"], f)
            dout = dout + timedelta(hours=getDSTOffset())
            
            if(dout < now):
                inMeeting = False
                for a in m["subgroups"]:
                    if(a in me['access']['groups']):
                        inMeeting = True
                        break
                
                attendanceItem = None
                for a in me['attendance']:
                    if(a['event'] == m['_id']):
                        attendanceItem = a
                        break
                    
                attendedMeeting = False
                if(attendanceItem != None):
                    if(attendanceItem['status'] == "ATTEND"):
                        attendedMeeting = True
                    
                
                sMI = SmallMeetingItem()
                sMI.ids.card.identifier = m['_id']
                sMI.ids.card.link = "past"
                sMI.ids.card.bind(on_touch_down = self.triggerOverlay)
                sMI.ids.meeting_title.text = m['title'] if m["title"] != "" else "A Meeting"
                sMI.ids.meeting_datetime.text = str(dout.month) + "/" + str(dout.day) + " @ " + str(dout.hour - 12 if dout.hour > 12 else dout.hour) + ":" + str(dout.minute).zfill(2) + ("PM" if dout.hour >= 12 else "AM")
                
                if(attendanceItem != None and attendanceItem['overriddenstatus'] != ""):
                    if(attendanceItem['overriddenstatus'] == "ATTEND"):
                        sMI.ids.meeting_status.icon = "account-check"
                        sMI.ids.meeting_status.text_color = self.getColor('success')
                    elif(attendanceItem['overriddenstatus'] == "EXCUSED"):
                        sMI.ids.meeting_status.icon = "minus"
                        sMI.ids.meeting_status.text_color = self.getColor('gray')
                    elif(attendanceItem['overriddenstatus'] == "ABSENT"):
                        sMI.ids.meeting_status.icon = "alert-circle"
                        sMI.ids.meeting_status.text_color = self.getColor('red')
                    else:
                        # any invalid entries for some reason will be EXCUSED
                        sMI.ids.meeting_status.icon = "minus"
                        sMI.ids.meeting_status.text_color = self.getColor('gray')
                else:
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
                
        
        mtgs.sort(key=lambda x: datetime.strptime(x["datetime"], f))
        for m in mtgs:
            dout = datetime.strptime(m["datetime"], f)
            dout = dout + timedelta(hours=getDSTOffset())
            
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
                sMI.ids.meeting_title.text = m['title'] if m["title"] != "" else "A Meeting"
                sMI.ids.meeting_datetime.text = str(dout.month) + "/" + str(dout.day) + " @ " + str(dout.hour - 12 if dout.hour > 12 else dout.hour) + ":" + str(dout.minute).zfill(2) + ("PM" if dout.hour >= 12 else "AM")
                if(inMeeting):
                    sMI.ids.meeting_status.icon = "calendar-check"
                    sMI.ids.meeting_status.text_color = self.getColor('success')
                else:
                    sMI.ids.meeting_status.icon = "calendar-remove"
                    sMI.ids.meeting_status.text_color = self.getColor('gray')
                
                self.ids.upcomingmeetings.add_widget(sMI)
            
        
        
        pass
        pass

class Error(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    def back(self):
        changePage("landing")
        
allLandingItems = []
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
    #     #print(data)
    #     x = threading.Thread(target = self.createItem, args = (data,), daemon=True)
    #     x.start()
    # def addMember(self, data):
    #     Clock.schedule_once(lambda x : toggle_message_box(True), 0)
    #     SCI.create_new_item(data[0], data[1], data[2])
    #     Clock.schedule_once(lambda x : toggle_message_box(False), 0)
    #     Clock.schedule_once(lambda x : changePage("landing"), 0)
    def showNewItem(self,d):
        MDApp.get_running_app().root.ids.input_box.addData("New Landing Item", "Create a new landing item to be visible to all members of the team!", [
            {"hint":"Title","multiline":False,"protected":False, "type":"input"},
            {"hint":"Contents","multiline":True,"protected":False, "type":"input"},
            {"hint":"Link To (optional)","multiline":False,"protected":False, "type":"input"},
            {"hint":"Select Special Icon","color":self.getColor("primary"),"options":["star", "bookmark", "basketball", "check", "fire", "information"], "icons":["star", "bookmark", "basketball", "check", "fire", "information"], "type":"dropdown"}
        ], self.handleNewItem)
        MDApp.get_running_app().root.ids.input_box.show()
    def handleNewItem(self, data):
        global inPopup
        
        if(data[0] == "" or data[1] == ""):
            inPopup = False
            MDApp.get_running_app().root.ids.action_box.addData("Error", "Please fill out the Title and Contents field!", [], None)
            MDApp.get_running_app().root.ids.action_box.show()
            return
        
        #print(data)
        x = threading.Thread(target = self.createItem, args = (data,), daemon=True)
        x.start()
    def createItem(self, data):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.create_new_item(data[0], data[1], data[2], icon="star" if data[3] == "" else data[3])
        Clock.schedule_once(lambda x : toggle_message_box(False), 0)
        Clock.schedule_once(lambda x : changePage("landing"), 0)
    def showItems(self, r):
        global pageScrollers
        pageScrollers["landing"] = self.ids.scroller
        
        self.removeAllElements()
        #self.ids.all_items.rows = 9
        
        
        
        admin = SCI.permissionCheck(["ADMIN_LANDING"])
        canCreate = SCI.permissionCheck(["ADMIN_LANDING_CREATE", "ADMIN_LANDING"])
        
        
        
        if(not r[1] == None and SCI.permissionCheck(["VIEW_SCHEDULE_SIGNIN"])):
            l = Label(text = "Current Meeting", font_size = "24dp", font_name =  'Roboto', color = self.getColor("secondary"),size_hint_y= None, bold=True)
        
            self.ids.all_items.add_widget(l)
            if(r[1]["logged"]):
                
                
                aI = AttendanceItem()
                
                aI.ids.meeting.text = r[1]["title"] + " at 12:00 PM (" + str(r[1]["length"]) +  "h)"
                
                self.ids.all_items.add_widget(aI)
                self.ids.all_items.add_widget(EmptySpace())
            else:
                #print(r[1])
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
        if(canCreate):
            fL = FloatLayout(size_hint_y= None)
            b = IDButton(text="Add New Item", md_bg_color=self.getColor("primary"), color=self.getColor('white'), font_size="12sp", padding="12dp", pos_hint={"center_x":.5, "center_y":.5}, on_release=self.showNewItem)
            fL.add_widget(b)
            self.ids.all_items.add_widget(fL)
        global allLandingItems
        allLandingItems = r[0]
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        for lpi in r[0]:
            #self.ids.all_items.rows += 4
            
            if("details" in lpi):
                
                startRes = lpi["details"]["start"] if "start" in lpi["details"] else None
                endRes = lpi["details"]["end"] if "end" in lpi["details"] else None
                now = datetime.now()
                if(startRes != None):
                    start = datetime.strptime(startRes, f)
                    start = start + timedelta(hours=getDSTOffset())
                    if(start > now):
                        continue
                if(endRes != None):
                    end = datetime.strptime(endRes, f)
                    end = end + timedelta(hours=getDSTOffset())
                    if(end < now):
                        continue
                
            
            
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
                nW.admin = 0
                
            else:
                nW.admin = 1
                nW.moduleitemid = lpi["_id"]
                
            if(buttonsGone == 1):
                nW.ids.landingitem_content.remove_widget(nW.ids.buttonct)
            if("color" in lpi):
                try:
                    if("#" in lpi["color"]):
                        nW.ids.button.mg_bg_color = rgba255to1(hex_to_rgb(lpi["color"]))
                        nW.ids.icon.text_color = rgba255to1(hex_to_rgb(lpi["color"]))
                        #print(rgba255to1(hex_to_rgb(lpi["color"])))
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
        if(SCI.permissionCheck(["ADMIN_SUBGROUPS_MANAGER"])):
            for s in r[3]:
            
                nS = SubgroupItem(togoto = s["name"])
                if(s["name"] in SCI.account["subgroups"]):
                    nS.ids.subgroup_name.text = s["name"]
                else:
                    nS.ids.subgroup_name.text = s["name"] + " (Not Apart Of)"
                self.ids.all_items.add_widget(nS)
        else:
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
    
    def getMe(self):
        Clock.schedule_once(lambda x: toggle_message_box(True), 0)
        me = SCI.get_this_user()
        roles = SCI.get_roles()
        Clock.schedule_once(lambda x: toggle_message_box(False), 0)
        Clock.schedule_once(lambda x: self.showMe(me, roles), 0)
    def showMe(self, me, roles):
        self.ids.username.text = me["username"]
        self.ids.details_fullname.text = me["fullname"]
        self.ids.details_email.text = me["email"]
        self.ids.details_subgroups.text = "In " + str(len(me['access']['groups'])) + " subgroups!"
        
        permString = ""
        for p in SCI.account['permissions']:
            permString += p + ", "
        permString = permString[:-2]
        
        self.ids.details_permissions.text = permString
        self.ids.role_card_contents.clear_widgets()
        roleName = me['access']["role"].upper()
        
        
        '''
        MDCard:
                    id: role_card
                    radius: '20dp'
                    elevation: '2dp'
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    size_hint_y: None
                    size_hint_x: None
                    orientation: 'vertical'
                    md_bg_color: root.getColor('gray')
                    width: (len(account_role.text)*40) + 40
                    height: '48dp'
                    Label:
                        id: account_role
                        text: 'STUDENT'
                        bold: True
                        font_size: '20dp'
        '''
        color = ""
        try:
            myrole = next((x for x in roles if x["name"] == me['access']["role"]))
            color = rgba255to1(hex_to_rgb(myrole["color"]))
        except:
            color = self.getColor("gray")
            pass
        
        role_card = MDCard(radius = '20dp', elevation = '2dp', pos_hint = {'center_x': .5, 'center_y': .5}, size_hint_y = None, size_hint_x = None, orientation = 'vertical', md_bg_color = color, width = (len(roleName)*40) + 40, height = '48dp')
        role_text = Label(text = roleName, bold = True, font_size = '20dp')
        role_card.add_widget(role_text)
        self.ids.role_card_contents.add_widget(role_card)
        
    def setup(self):
        global pageScrollers
        pageScrollers["account"] = self.ids.scroller
        x = threading.Thread(target=self.getMe, daemon=True)
        x.start()
    def showResetPassword(self,d):
        MDApp.get_running_app().root.ids.input_box.addData("Reset Your Password", "You will need your old password to change your password to a new one. Please note that this will not sign out your other accounts!", [
            {"hint":"Current Password","multiline":False,"protected":True, "type":"input"},
            {"hint":"New Password","multiline":False,"protected":True, "type":"input"},
            {"hint":"Confirm New Password","multiline":False,"protected":True, "type":"input"},
        ], self.handleResetPassword)
        MDApp.get_running_app().root.ids.input_box.show()
    def handleResetPassword(self, data):
        #print(data)
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

class Cable(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    def getItems(self):
        Clock.schedule_once(lambda x: toggle_message_box(True), 0)
        items = SCI.get_messages(self.chat == "ALL", None if self.chat == "ALL" else self.chat)
        users = SCI.get_users()
        subgroups = SCI.get_subgroups()
        Clock.schedule_once(lambda x: toggle_message_box(False), 0)
        Clock.schedule_once(lambda x: self.showMessages(items, users, subgroups), 0)
    def init(self):
        
        
        if(not "chat" in self.__dict__):
            self.chat = "ALL"
        self.ids.cable_channel.text = "Announcements - " + self.chat
        if(self.chat == "ALL"):
            self.ids.cable_channel.text = "Announcements - Lightning Robotics"
        
        x = threading.Thread(target=self.getItems, daemon=True)
        x.start()
    def selectChannel(self, channel):
        try:
            self.dropdown.dismiss()
        except:
            pass
        self.chat = channel
        self.ids.cable_channel.text = "Announcements - " + channel
        if(channel == "ALL"):
            self.ids.cable_channel.text = "Announcements - Lightning Robotics"
        self.init()
    def showMessages(self, items, users, sgs):
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        thisSg = None if self.chat == "ALL" else next(x for x in sgs if x["name"] == self.chat) 
        if(not SCI.permissionCheck(["ADMIN_ANNOUNCEMENT"]) and not (thisSg != None and SCI.account["id"] in thisSg["managers"])):
            self.ids.send_message.disabled = True
            self.ids.create_message.disabled = True
        
        
        ddItems = []
        
        sgs.append({
            "name": "ALL"
        })
                
        for s in sgs:
            ddItems.append({
                "text": s["name"],
                "viewclass": "OneLineListItem",
                "on_release": lambda x=s["name"]: self.selectChannel(x)
            })
        
        self.dropdown = MDDropdownMenu(caller=self.ids.cable_channel, items=ddItems, width_mult=3,position="bottom")
        
        self.ids.messages.clear_widgets()
        shown = 0
        for mI in range(len(items)-1, -1, -1):
            if(shown < 20):
                m = items[mI]
                dout = datetime.strptime(m["datetime"], f)
                dout = dout + timedelta(hours=getDSTOffset())
                print(dout.tzinfo)
                sender = next(x for x in users if x["id"] == m["sender"])
                nM = MyMessage() if sender["id"] == SCI.account['id'] else Message()
                nM.ids.contents.text = "[b]" + sender["username"] + "[/b] says on [i]" + str(dout.month) + "/" + str(dout.day) + " @ " + str(dout.hour - 12 if dout.hour > 12 else dout.hour) + ":" + str(dout.minute).zfill(2) + ("PM" if dout.hour >= 12 else "AM") + "[/i]\n\n" + '"' + m["message"] + '"'
                
                self.ids.messages.add_widget(nM)
                shown += 1
            
    def showDropdown(self):
        try:
            self.dropdown.open()
        except:
            pass
    def waitSendMessage(self, msg):
        Clock.schedule_once(lambda x: toggle_message_box(True), 0)
        SCI.send_message(self.chat=="ALL", self.chat, msg)
        Clock.schedule_once(lambda x: toggle_message_box(False), 0)
        Clock.schedule_once(lambda x: self.init(), 0)
    def sendMessage(self):
        if(self.ids.create_message.text != ""):
            
            x = threading.Thread(target=self.waitSendMessage, args=(self.ids.create_message.text,), daemon=True)
            self.ids.create_message.text = ""
            x.start()
            
            
        

class Subgroup(Screen):
    def showNewItem(self):
        MDApp.get_running_app().root.ids.input_box.addData("New Subgroup Item", "Create a item that will only be visible to the " + self.subgroup["name"] + " subgroup", [
            {"hint":"Title","multiline":False,"protected":False, "type":"input"},
            {"hint":"Contents","multiline":True,"protected":False, "type":"input"},
            {"hint":"Link To (optional)","multiline":False,"protected":False, "type":"input"},
            {"hint":"Select Special Icon","color":self.getColor("primary"),"options":["star", "bookmark", "basketball", "check", "fire", "information"],"icons":[], "type":"dropdown"}
        ], self.handleNewItem)
        MDApp.get_running_app().root.ids.input_box.show()
    def goToSubgroupChat(self):
        MDApp.get_running_app().root.ids.cablepage.chat = self.subgroup["name"]
        changePage("cable")
    def handleNewItem(self, data):
        global inPopup
        if(data[0] == "" or data[1] == ""):
            inPopup = False
            MDApp.get_running_app().root.ids.action_box.addData("Error", "Please fill out the Title and Contents field!", [], None)
            MDApp.get_running_app().root.ids.action_box.show()
            return
        #print(data)
        x = threading.Thread(target = self.createItem, args = (data,), daemon=True)
        x.start()
    def createItem(self, data):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.create_new_item(data[0], data[1], data[2], self.subgroup["tag"], icon="star" if data[3] == "" else data[3])
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
        global pageScrollers
        pageScrollers["subgroup"] = self.ids.scroller
        sg = sgD[0]
        
        self.ids.tag.text = ("• " if (sgD[1]) else "" ) + sg["tag"]
        self.ids.subgroup_name.text = sg["name"]
        self.admin = sgD[1]
        if(SCI.permissionCheck(["ADMIN_SUBGROUPS_MANAGER"])):
            self.admin = True
        self.users = users
        self.subgroup = sg
        self.meetings = meetings
        inGroup = (sg["name"] in SCI.account["subgroups"])
        if(inGroup):
            self.ids.subgroup_membership.text = "You are a leader of this subgroup" if sgD[1] else "You are a member of this subgroup"
            
        else:
            self.ids.subgroup_membership.text = "You are not in this subgroup"
        pass
        
        if(not self.admin):
            self.ids.new_item.disabled = True
            self.ids.new_member.disabled = True
        else:
            self.ids.new_item.disabled = False
            self.ids.new_member.disabled = False
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
        #print(items)
        for m in meetings:
            if(show > 0 and (sg["name"] in m["subgroups"] or self.admin)):

                dout = datetime.strptime(m["datetime"], f)
                dout = dout + timedelta(hours=getDSTOffset())
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
        global allLandingItems
        allLandingItems = items
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
                        #print(rgba255to1(hex_to_rgb(i["color"])))
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
            
            if(not self.admin or not SCI.permissionCheck(["ADMIN_LANDING"])):

                lI.admin = 0

            else:
                lI.admin = 1
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
        #print(buttonId)
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
            #print("Leave subgroup here")
    def showMeetingOverlay(self, *args):
        
        card = args[0]
        if(not inPopup):
            self.use = card.identifier
        buttons = [{"name" : "Show Meeting Page", "color": "primary"}]
        f = "%Y-%m-%dT%H:%M:%S.%fZ"
        
        #print(self.meetings)
        m = next(x for x in self.meetings if x["_id"] == card.identifier)
        dout = datetime.strptime(m["datetime"], f)
        dout = dout + timedelta(hours=getDSTOffset())
        self.selectedMeeting = m
        
        if(self.admin):
            if not self.subgroup['name'] in self.selectedMeeting['subgroups']:
                buttons.append({"name" : "We Are Attending", "color": "success"})
            else:
                buttons.append({"name" : "We Aren't Attending", "color" : "red"})
        elif(SCI.permissionCheck(["ADMIN_SUBGROUPS_MANAGER","ADMIN_SCHEDULE"])):
            if not self.subgroup['name'] in self.selectedMeeting['subgroups']:
                buttons.append({"name" : "They Are Attending", "color": "success"})
            else:
                buttons.append({"name" : "They Aren't Attending", "color" : "red"})
            
        
        MDApp.get_running_app().root.ids.action_box.addData(m['title'], "on " + str(dout.month) + "/" + str(dout.day) + "/" + str(dout.year) + " @ " + str(dout.hour - 12 if dout.hour > 12 else dout.hour) + ":" + str(dout.minute).zfill(2) + ("PM" if dout.hour >= 12 else "AM") + "\n\n" + m["description"] + "\n\n" + str(len(m["subgroups"])) + " subgroups attending", buttons, self.handleMeetingOverlay)
        MDApp.get_running_app().root.ids.action_box.show()
    def handleMeetingOverlay(self, buttonId):
        global thisMeeting
        thisMeeting = self.use
        if(buttonId == 0):
            changePage("meeting")
        if(buttonId == 1):
            pass
            action = "remove"
            if not self.subgroup['name'] in self.selectedMeeting['subgroups']:
                action = "add"
            x = threading.Thread(target = self.changeAttendance, args = (action,), daemon=True)
            x.start()
    def addMemberAPI(self, uid):
        Clock.schedule_once(lambda dt: toggle_message_box(True), 0)
        SCI.add_user_to_subgroup(uid, self.subgroup["name"])
        Clock.schedule_once(lambda dt: toggle_message_box(False), 0)
        Clock.schedule_once(lambda dt: changePage("subgroup"), 0)
    def handleAddMember(self, data):
        global inPopup
        
        username = data[0]
        user = next(x for x in self.users if x["username"] == username)
        
        x = threading.Thread(target = self.addMemberAPI, args = (user["id"],), daemon=True)
        x.start()
    def showMembersToAdd(self,data):
        global inPopup
        
        username = data[0]
        fullname = data[1]
        
        listUsers = []
        for x in self.users:
            if(not self.subgroup["name"] in x["access"]["groups"]):
                if(username.lower() in x["username"].lower() and username != ""):
                    listUsers.append(x)
                elif(fullname.lower() in x["fullname"].lower() and fullname != ""):
                    
                    listUsers.append(x)
                elif(username == "" and fullname == ""):
                    listUsers.append(x)
        self.listUsers = listUsers
        
        dropdownOptions = []
        for l in listUsers:
            dropdownOptions.append(l["username"] if username != "" else l["fullname"])
        inPopup = False
        print(dropdownOptions)
        
        Clock.schedule_once(lambda dt: self.showAgain(dropdownOptions), 0.5)
    def showAgain(self, dropdownOptions):
        if(len(dropdownOptions) == 0):
            MDApp.get_running_app().root.ids.action_box.addData("No Users Found", "We could not find any users based on your search!", [])
            MDApp.get_running_app().root.ids.action_box.show()
        else:
            MDApp.get_running_app().root.ids.input_box.addData("Find User", "Select one of these users from the dropdown below, or try again and edit your search!", [
                {"hint":"Select Filtered Member","color":self.getColor("primary"),"options":dropdownOptions, "icons":[], "type":"dropdown"}
                ], self.handleAddMember)
            MDApp.get_running_app().root.ids.input_box.show()
         
    def showAddMember(self):
        
        
        MDApp.get_running_app().root.ids.input_box.addData("Search for Member", "Search for a member that you would like to add to the subgroup!", [
            {"hint":"Username (contains)","multiline":False,"protected":False, "type":"input"},
            {"hint":"Full Name (contains)","multiline":False,"protected":False, "type":"input"}
        ], self.showMembersToAdd)
        MDApp.get_running_app().root.ids.input_box.show()
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
    
    
    def finish_ios_init(self, *args):
        self.onesignal_object = autoclass("OneSignal")
        mock_launch_options = objc_dict({})
        print(dir(self.onesignal_object))
        self.onesignal_object.initWithLaunchOptions_(mock_launch_options)
        self.onesignal_object.setAppId_("8ec8f18d-38ef-449b-8e10-69025823a4a5")
        self.onesignal_object.promptForPushNotificationsWithUserResponse_(self.notif_success)
    def setUserId(self, uid, userName):
        if(platform == "ios"):
            self.onesignal_object.setExternalUserId_(uid)
            self.onesignal_object.sendTag_("username", userName)
            
    def notif_success(self, *args):
        print("Prompt Success!")
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
            "light": rgba255to1((110, 167, 230,1)),
            "white": rgba255to1((255, 255, 255,1)),
            "gray" : rgba255to1((100, 100, 100,1)),
            "lightgray": rgba255to1((220, 220, 220,1)),
            "black": rgba255to1((0, 0, 0,1)),
            "success": rgba255to1((0, 200, 0,1)),
            "red": rgba255to1((255, 0, 0,1)),
            "green": rgba255to1((0, 255, 0,1)),
            "blue": rgba255to1((0, 0, 255,1)),
            "orange": rgba255to1((255, 165, 0,1))
        }
        self.icon = "AppIcons/playstore.png"
        
        if platform == "ios":
            Clock.schedule_once(self.finish_ios_init, 0)
        
        #print("Hello World")
        return Builder.load_string(KVContents)

    def on_start(self):
        
        for icon_name in icons_item.keys():
            if(icon_name == "exit-to-app"):
                self.root.ids.content_drawer.ids.md_list2.add_widget(
                    ItemDrawer(icon=icon_name, text=icons_item[icon_name][0])
                )
            else:
                self.root.ids.content_drawer.ids.md_list.add_widget(
                    ItemDrawer(icon=icon_name, text=icons_item[icon_name][0])
                )
        
        x = threading.Thread(target = handleLogin, args = (True,), daemon=True)
        x.start()
    
Window.fullscreen = False
Main().run()