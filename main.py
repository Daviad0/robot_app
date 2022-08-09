from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.popup import Popup






class BoxLayoutExample(BoxLayout):
    def btn(self):
        show_popup1()


class BoxLayoutExample2(BoxLayout):
    def btn(self):
        show_popup2()

class BoxLayoutExample3(BoxLayout):
    def btn(self):
        show_popup3()

'''class Function1(App):
    def build(self):
        Ort = BoxLayout(orientation ='vertical')
        VO = BoxLayout(orientation ='vertical')
        btn1 = Button(text = "What is your name?")
        VO.add_widget(btn1)
        Ort.add_widget(VO)
        return Ort

fcn = Function1()
fcn.run()'''



class P1(BoxLayout):
    pass
class P2(BoxLayout):
    pass
class P3(BoxLayout):
    pass

class LoginPage(BoxLayout):
    pass


class Login(App):
    pass

class AppBuild(App):
    pass
class AppBuild2(App):
    pass
class AppBuild3(App):
    pass





def show_popup1():
    give1 = P1()

    popupWindow1 = Popup(title="Popup Window1", content=give1, size_hint=(None,None), size=(400,400))

    popupWindow1.open()

def show_popup2():
    give2 = P2()

    popupWindow2 = Popup(title="Popup Window2", content=give2, size_hint=(None,None), size=(400,400))

    popupWindow2.open()

def show_popup3():
    give3 = P3()

    popupWindow3 = Popup(title="Popup Window3", content=give3, size_hint=(None,None), size=(400,400))

    popupWindow3.open()


Login().run()




