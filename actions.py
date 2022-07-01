from kivy.network.urlrequest import UrlRequest

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
        pass
    
    def _sendAPIRequest(self, method, endpoint, data=None):
        pass
        
    