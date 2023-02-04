class Custom(Screen):
    def getColor(self, name):
        return COLORS[name.lower()]
    pass