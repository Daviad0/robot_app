
from os import umask
from kivy.lang import Builder
from datetime import datetime
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty, BooleanProperty
# import kivy label
from kivy.uix.label import Label

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

# import MDFillRoundFlatButton from kivymd
from kivymd.uix.button import MDFillRoundFlatButton


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
    "red": rgba255to1((255, 0, 0,1)),
    "green": rgba255to1((0, 255, 0,1)),
    "blue": rgba255to1((0, 0, 255,1))
}

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

class IDButton(MDFillRoundFlatButton):
    buttonid = NumericProperty(0)

class ActionBox(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    def show(self):
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    def hide(self):
        self.pos_hint = {'center_x': 0.5, 'center_y': 10}
    def addData(self, title, contents, buttons, callback=None):
        # Each callback should have an argument for the buttonid
        self.ids.title.text = title
        self.ids.contents.text = contents
        
        self.ids.buttons.clear_widgets()
        self.callback = callback
        n = 0
        for b in buttons:
            name = b["name"]
            color = b["color"]
            self.ids.buttons.add_widget(IDButton(text=name, md_bg_color=self.getColor(color), color=self.getColor('white'), on_release=self.performAction, buttonid=n))
            n+=1
    def performAction(self, *args):
        buttonId = args[0].buttonid
        print("Action Performed: " + str(buttonId))
        if(buttonId == -1):
            self.hide()
        else:
            self.callback(buttonId)
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
    def getColor(self, name):
        return COLORS[name.lower()]
    def openLink(self):
        print(self.weblink)
        webbrowser.open(self.weblink)
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
            else:
                nW.weblink = lpi["result"]["data"]
                
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
        
        show = 10
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
            if(show > 0 and sg["name"] in m["subgroups"]):
                dout = datetime.strptime(m["datetime"], f)
                if(dout > now):
                    mI = MeetingItem()
                    mI.ids.card.identifier = m["_id"]
                    mI.ids.card.link = "meeting"
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
            if(not i["result"]["to"] == "link"):
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
        if(self.admin):
            buttons.append({"name" : "We Aren't Attending", "color" : "red"})
        print(self.meetings)
        m = next(x for x in self.meetings if x["_id"] == card.identifier)
        self.selectedMeeting = m
        
        MDApp.get_running_app().root.ids.action_box.addData(m['title'], "@ " + str(m["datetime"]) + "\n" + m["description"] + "\n" + str(len(m["subgroups"])) + " subgroups attending", buttons, self.handleMeetingOverlay)
        MDApp.get_running_app().root.ids.action_box.show()
    def handleMeetingOverlay(self, buttonId):
        if(buttonId == 0):
            pass
            x = threading.Thread(target = self.removeAttendance, args = (), daemon=True)
            x.start()
            
    def removeAttendance(self):
        Clock.schedule_once(lambda x : toggle_message_box(True), 0)
        SCI.remove_subgroup_attendance(self.subgroup, self.admin, self.selectedMeeting)
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