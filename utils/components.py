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
        #vibrate(0.4)
        if(platform == "android" or platform == "ios"):
            vibrator.vibrate(0.2)
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
            self.ids.buttons.add_widget(IDButton(text=name, md_bg_color=self.getColor(color), color=self.getColor('white'), on_release=self.performAction, buttonid=n, font_size="12sp", padding="12dp"))
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

class IDInput(MDTextField):
    inputid = NumericProperty(0)
    def getColor(self, name):
        return COLORS[name.lower()]
    pass
class InputBox(FloatLayout):
    def getColor(self, name):
        return COLORS[name.lower()]
    def show(self):
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        #vibrate(0.4)
        if(platform == "android" or platform == "ios"):
            vibrator.vibrate(0.1)
    def hide(self):
        self.pos_hint = {'center_x': 0.5, 'center_y': 10}
    def addData(self, title, contents, inputs, callback=None):
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
            i = IDInput(inputid=n,multiline=multiline, password=protected, line_color_focus= self.getColor('primary'), active_line=True, hint_text=hint, font_name= 'Roboto', border=(2,2,2,2), spacing=(20,20,20,20), padding=(20,20,20,20),border_color= (0,0,0,1))
            i.bind(text=self.changeText)
            self.ids.inputs.add_widget(i)
            n+=1
            self.data.append("")
    def changeText(self, *args):
        inputId = args[0].inputid
        print("changed text: " + str(inputId))
        self.data[inputId] = args[0].text
    def performAction(self, *args):
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
    def getColor(self, name):
        return COLORS[name.lower()]
    def openLink(self):
        print(self.weblink)
        webbrowser.open(self.weblink)
        print("A")
    pass

class SubgroupItem(FloatLayout):
    togoto = StringProperty()
    def getColor(self, name):
        return COLORS[name.lower()]
    def toSubgroup(self):
        global subgroup
        subgroup = self.togoto
        changePage("subgroup")
    pass