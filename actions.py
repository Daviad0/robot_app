from kivy.network.urlrequest import UrlRequest
from kivy.storage.jsonstore import JsonStore
import requests

class SparkClub():
    def __init__(self):
        self.storage = JsonStore("account.json")
        print(self.storage.exists("account"))
        self.account = {
            "loggedIn": False,
            "token": "",
            "permissions": [],
            "username": "",
            "email": ""
        }
        
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
                    return True
        return False
    
    def login(self, username, password):
        res = self._sendAPIRequest("POST", "/acc/login", {
            "username": username,
            "password": password,
            "group": "testing-env" # change to the lightning robotics group name later
        })
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            self.account["loggedIn"] = True
            self.account["token"] = data["token"]
            self.account["permissions"] = data["user"]["access"]["permissions"]
            self.account["username"] = data["user"]["username"]
            self.account["email"] = data["user"]["email"]
            self.storage.put("prev", account=self.account)
            print("Logged in!")
            return True
        else:
            return False
    def get_items(self):
        if not self.account["loggedIn"]:
            return []
        res = self._sendAPIRequest("GET", "/group/items")
        data = res["data"]
        if(res["status"] == 200 and data["successful"]):
            return data["items"]
        else:
            return []
        
    def get_protons(self):
        if not self.account["loggedIn"]:
            return None
        
        res = self._sendAPIRequest("GET", "/group/protons")
        if(res["status"] == 200):
            return res["data"]
        else:
            return None
        
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
        
        
    
    def _sendAPIRequest(self, method, endpoint, data=None):
        cookies = {}
        if(self.account["loggedIn"]):
            cookies["session"] = self.account["token"]
            print(self.account["token"])
        res = requests.request(method, "http://localhost:8080" + endpoint, data=data, cookies=cookies)
        data = res.json()
        return {"status": res.status_code, "data": data}
        
    
