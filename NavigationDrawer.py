from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from kivymd.app import MDApp

KV = '''
<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: "50dp", "50dp"
            source: "My project-1.png"

    MDLabel:
        text: "test_1"
        font_style: "Button"
        adaptive_height: True

    MDLabel:
        text: "test1@gmail.com"
        font_style: "Caption"
        adaptive_height: True

    ScrollView:

        MDList:

            OneLineListItem:
                text: "Safety Handbook"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "scr 1"

            OneLineListItem:
                text: "Attendance"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "scr 2"
            
            OneLineListItem:
                text: "Log Out"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "scr 3"


Screen:

    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 10
        title: "Lightning Robotics App"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

    MDNavigationLayout:
        x: toolbar.height

        ScreenManager:
            id: screen_manager

            Screen:
                name: "scr 1"

                MDLabel:
                    text: "Safety Handbook File"
                    halign: "center"

            Screen:
                name: "scr 2"

                MDLabel:
                    text: "Attendance File"
                    halign: "center"
            
            Screen:
                name: "scr 3"

                MDLabel:
                    text: "Logging Out..."
                    halign: "center"

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer
'''


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class LightningNavigationDrawer(MDApp):
    def build(self):
        return Builder.load_string(KV)


LightningNavigationDrawer().run()