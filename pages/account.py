class Account(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    def setup(self):
        self.ids.username.text = SCI.account["username"]
        self.ids.account_role.text = SCI.account["role"].upper()
    pass