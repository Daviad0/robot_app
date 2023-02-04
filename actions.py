import re
from kivy.network.urlrequest import UrlRequest
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
import requests
import os

path = ""
group = "lightning-robotics"

class SparkClub():
    def __init__(self):
	
        
        self.account = {
            "loggedIn": False,
            "token": "",
            "permissions": [],
            "username": "",
            "email": "",
            "subgroups": [],
            "role": "",
            "id": ""
        }
    def permissionCheck(self,allowed):
        if("*" in self.account["permissions"]):
            return True
    
        for permission in allowed:
            if(permission in self.account["permissions"]):
                return True
        return False
    def initialize(self):
        global path
        path = os.path.join(MDApp.get_running_app().user_data_dir, "account.json")
        self.storage = JsonStore(path)
        print(self.storage.exists("account"))
    def try_login_with_key(self):
        if(self.storage.exists("prev")):
            self.account = self.storage.get("prev")["account"]
            if(self.account["loggedIn"]):
                res = self._sendAPIRequest("GET", "/acc/verify")
                data = res["data"]
                if not data["successful"]:
                    self.account["loggedIn"] = False
                    self.storage.put("prev", account=self.account)
                    return False
                else:
                    self.account["subgroups"] = data["user"]["access"]["groups"]
                    self.account["role"] = data["user"]["access"]["role"]
                    self.account["permissions"] = data["user"]["permissions"]
                    return True
        return False
    #def get_permissions_of_role(self):
    def logout(self):
        self.account = {
            "loggedIn": False,
            "token": "",
            "permissions": [],
            "username": "",
            "email": "", 
            "subgroups": [],
            "role": "",
            "id": ""
        }
        self.storage.put("prev", account=self.account)
    def login(self, username, password):
        res = self._sendAPIRequest("POST", "/acc/login", {
            "username": username,
            "password": password,
            "group": group # change to the lightning robotics group name later
        })
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            self.account["loggedIn"] = True
            self.account["token"] = data["token"]
            self.account["permissions"] = data["user"]["permissions"]
            self.account["username"] = data["user"]["username"]
            self.account["email"] = data["user"]["email"]
            self.account["subgroups"] = data["user"]["access"]["groups"]
            self.account["role"] = data["user"]["access"]["role"]
            self.account["id"] = data["user"]["id"]
            self.storage.put("prev", account=self.account)
            print("Logged in!")
            return True
        else:
            return False
    def get_subgroup(self, subgroup):
        if not self.account["loggedIn"]:
            return []
        res = self._sendAPIRequest("GET", "/group/subgroup?name=" + subgroup)
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return (data["subgroup"], data['admin'])
        else:
            return []
    def get_users(self):
        if not self.account["loggedIn"]:
            return []
        res = self._sendAPIRequest("GET", "/group/users")
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return data["items"]
        else:
            return []
    def get_this_user(self):
        if not self.account["loggedIn"]:
            return None
        res = self._sendAPIRequest("GET", "/acc/verify")
        if(res["status"] == 200):
            return res["data"]["user"]
        else:
            return None
    def get_roles(self):
        if not self.account["loggedIn"]:
            return None
        res = self._sendAPIRequest("GET", "/group/roles")
        data = res["data"]
        if(res["status"] == 200):
            return data["items"]
        else:
            return None
    def send_attendance_request(self, finalResult, useMeeting):
        if not self.account["loggedIn"]:
            return None
        res = self._sendAPIRequest("POST", "/group/attendance/request", data={"final": finalResult, "meetingId" : useMeeting, "uid": self.account["id"]})
        if(res["status"] == 200):
            return res["data"]
        else:
            return None
    def send_override(self, meetingId, userId, override):
        if not self.account["loggedIn"]:
            return None
        res = self._sendAPIRequest("POST", "/group/attendance/override", data={"meetingId": meetingId, "uid": userId, "override": override})
        if(res["status"] == 200):
            return res["data"]
        else:
            return None
    def get_meetings(self):
        if not self.account["loggedIn"]:
            return []
        res = self._sendAPIRequest("GET", "/group/meetings")
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return data["items"]
        else:
            return []
    def get_items(self, context):
        if not self.account["loggedIn"]:
            return []
        res = self._sendAPIRequest("GET", "/group/items", headers={"subgroup": context})
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return data["items"]
        else:
            return []
    def reset_code_request(self, email, studentId):
        if self.account["loggedIn"]:
            return None
        res = self._sendAPIRequest("POST", "/acc/requestcode", data={"email": email, "studentid": studentId})
        if(res["status"] == 200):
            return res["data"]
        else:
            return None
    def reset_password_code(self, code, password, userId):
        if self.account["loggedIn"]:
            return None
        
        res = self._sendAPIRequest("POST", "/acc/reset", data={"code": code, "newPw": password, "uid": userId})
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return True
        else:
            return False
    def get_protons(self):
        if not self.account["loggedIn"]:
            return None
        
        res = self._sendAPIRequest("GET", "/group/protons")
        if(res["status"] == 200):
            return res["data"]
        else:
            return None
    def get_my_attendance(self):
        if not self.account["loggedIn"]:
            return None
        
        res = self._sendAPIRequest("GET", "/group/report/attendance/you")
        data = res["data"]
        if(res["status"] == 200):
            return data
        else:
            return None
    def get_subgroups(self):
        if not self.account["loggedIn"]:
            return None
        res = self._sendAPIRequest("GET", "/group/subgroups")
        if(res["status"] == 200):
            return res["data"]["items"]
        
        else:
            return None
    def remove_subgroup_member(self, subgroup, admin, member):
        if not self.account["loggedIn"]:
            return None
        if not admin and not self.account["id"] == member:
            return None
        
        res = self._sendAPIRequest("POST", "/group/subgroup/remove", data={"uid": member, "group": subgroup["name"]})
        if(res["status"] == 200):
            return res["data"]
        else:
            return None
    def remove_item(self, id):
        if not self.account["loggedIn"]:
            return False

        res = self._sendAPIRequest("POST", "/group/item", data={"_id": id, "action": "delete"})
        
        if(res["status"] == 200):
            return True
        else:
            return False
    
    def change_subgroup_attendance(self, subgroup, admin, meeting, action):
        if not self.account["loggedIn"]:
            return None
        if not admin:
            return None
        
        res = self._sendAPIRequest("POST", "/group/subgroup/schedule", data={"meetingId": meeting['_id'], "group": subgroup["name"], "action": action})
        if(res["status"] == 200):
            return res["data"]
        else:
            return None
    def edit_item(self, id, title, contents, linkto):
        if not self.account["loggedIn"]:
            return False
        
        action = "link" if linkto else "static"
        
        res = self._sendAPIRequest("POST", "/group/item", data={"_id": id, "action": "edit", "title": title, "contents": contents, "resultdata": [action, linkto]})
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return True
        else:
            return False
    def create_new_item(self, title, contents, linkto, subgroup=None, icon="star"):
        if not self.account["loggedIn"]:
            return False
        
        action = "link" if linkto else "static"
        res = {
            "to": action,
            "data": linkto
        }
        
        show = 1
        subgroups = [] if subgroup == None else [subgroup]
        
        
        res = self._sendAPIRequest("POST", "/group/item", data={"title": title, "contents": contents, "resultdata": [action, linkto], "icon": icon, "show": show, "subgroups": subgroups, "action": "create"})
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return True
        else:
            return False
    def new_meeting(self, title, description, length, datetime):
        if not self.account["loggedIn"]:
            return False
        
        res = self._sendAPIRequest('POST', '/group/meeting', data={"title": title, "description": description, "length": length, "datetime": datetime, "action": "create", "subgroups": []})
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return True
        else:
            return False
    def add_user_to_subgroup(self, uid, subgroup):
        if not self.account["loggedIn"]:
            return False
        
        res = self._sendAPIRequest('POST', '/group/subgroup/add', data={"uid": uid, "group": subgroup})
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return True
        else:
            return False
    def try_create_account(self, username, fullname, email, externalId, password):
        if self.account["loggedIn"]:
            return False
        res = self._sendAPIRequest('POST', '/acc/create', data={"username": username, "fullname": fullname, "email": email, "externalId": externalId, "password": password, "group": group})
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            
            self.account["loggedIn"] = True
            self.account["token"] = data["token"]
            self.account["permissions"] = data["user"]["permissions"]
            self.account["username"] = data["user"]["username"]
            self.account["email"] = data["user"]["email"]
            self.account["subgroups"] = data["user"]["access"]["groups"]
            self.account["role"] = data["user"]["access"]["role"]
            self.account["id"] = data["user"]["id"]
            self.storage.put("prev", account=self.account)
            
            
            return (True, data)
        else:
            return (False, data)
    def try_external_login(self, externalId):
        if self.account["loggedIn"]:
            return False
        
        res = self._sendAPIRequest('POST', '/group/today/anon', data={"externalId": externalId, "group": group})
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return True
        else:
            return False
    def get_meeting_today(self):
        if not self.account["loggedIn"]:
            return {}
        
        res = self._sendAPIRequest("GET", "/group/today")
        data = res["data"]
        if(res["status"] == 200 and data["successful"] and "today" in data):
            return data["today"]
        else:
            return None
    def sign_in_meeting(self):
        if not self.account["loggedIn"]:
            return False
        
        res = self._sendAPIRequest("POST", "/group/today")
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return True
    def get_messages(self, group_wide, subgroup):
        if not self.account["loggedIn"]:
            return False
        res = self._sendAPIRequest("GET", "/group/subgroup/messages" if not group_wide else "/group/announcements", headers={"group": subgroup})
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return data["messages"]
    def send_message(self, group_wide, subgroup, message):
        if not self.account["loggedIn"]:
            return False
        res = self._sendAPIRequest("POST", "/group/subgroup/message" if not group_wide else "/group/announcement", data={"message": message, "group": subgroup})
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return True
        else:
            return False
    def reset_password(self, current, new):
        if not self.account["loggedIn"]:
            return False
        res = self._sendAPIRequest("POST", "/acc/reset", data={"oldPw": current, "newPw": new, "id": self.account["id"]})
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return True
        else:
            return False
    
    def _sendAPIRequest(self, method, endpoint, data=None, headers=None):
        try:
            cookies = {}
            if(self.account["loggedIn"]):
                cookies["session"] = self.account["token"]
                print(self.account["token"])
            res = requests.request(method, "https://lr.robosmrt.com" + endpoint, data=data, cookies=cookies, headers=headers)
            
            if(res.status_code != 200):
                print("ERROR RECIEVED FOR " + endpoint + ": " + str(res.status_code))
                MDApp.get_running_app().root.show_error("Error Code: " + str(res.status_code))
            data = res.json()
            return {"status": res.status_code, "data": data}
        except:
            MDApp.get_running_app().root.show_error("Error Code: " + str(res.status_code))
            return {}
        
    
