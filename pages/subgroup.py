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
            if(not i["result"]["to"] == "link"):
                lI.ids.landingitem_content.remove_widget(lI.ids.buttonct)
            else:
                lI.weblink = i["result"]["data"]
                
                
                
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