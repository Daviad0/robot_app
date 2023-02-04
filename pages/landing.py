class Landing(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    def removeAllElements(self):
        rows = [i for i in self.ids.all_items.children]
        for r in rows:
            self.ids.all_items.remove_widget(r)
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