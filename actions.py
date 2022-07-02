from kivy.network.urlrequest import UrlRequest
import requests

class SparkClub():
    def __init__(self):
        self.account = {
            loggedIn: False,
            token: None,
            permissions: None,
            username: None,
            email: None
        }
    def login(self, username, password):
        res = self._sendAPIRequest("POST", "/acc/login", {
            username: username,
            password: password,
            group: "testing-env" # change to the lightning robotics group name later
        })
        if(res.status == 200 and data.successful):
            self.account.loggedIn = True
            self.account.token = data.token
            self.account.permissions = data.permissions
            self.account.username = data.username
            self.account.email = data.email
            print("Logged in!")
            return True
        else:
            return False
    
    def _sendAPIRequest(self, method, endpoint, data=None):
        cookies = {}
        if(self.account.loggedIn):
            cookies["token"] = self.account.token
        res = requests.request(method, "http://localhost:8080" + endpoint, data=data, cookies=cookies)
        data = res.json()
        
        return {status: res.status_code, data: data}
        
    