from kivy.network.urlrequest import UrlRequest
import requests

class SparkClub():
    def __init__(self):
        self.account = {
            "loggedIn": False,
            "token": "",
            "permissions": [],
            "username": "",
            "email": ""
        }
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
            print("Logged in!")
            return True
        else:
            return False
    
    def _sendAPIRequest(self, method, endpoint, data=None):
        cookies = {}
        if(self.account["loggedIn"]):
            cookies["token"] = self.account["token"]
        res = requests.request(method, "http://localhost:8080" + endpoint, data=data, cookies=cookies)
        data = res.json()
        print(data)
        return {"status": res.status_code, "data": data}
        
    