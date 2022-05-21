from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout


class widget_1(App):
    # override the build method and return the root widget of this App
  
    def build(self):
        # Define a grid layout for this App
        self.layout = GridLayout(cols = 1, padding = 10)
  

        # Add a button
        self.button = Button(text ="Click for pop-up")
        self.button2 = Button(text = "Hi")
        self.layout.add_widget(self.button)
        self.layout.add_widget(self.button2)
  
        # Attach a callback for the button press event
        self.button.bind(on_press = self.onButtonPress)
        
        
        return self.layout
          # On button press - Create a popup dialog with a label and a close button
    def onButtonPress(self, button):
        layout2 = BoxLayout(orientation = "vertical")
        layout = GridLayout(cols = 1, padding = 10)
  
        popupLabel = Label(text = "Click for pop-up")
        closeButton = Button(text = "Close the pop-up")
        popup2button = Button(text = "Test")
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)       
        layout2.add_widget(popup2button)
        # Instantiate the modal popup and display
        popup = Popup(title ='Demo Popup',content = layout)     
        popup2 = Popup(title = 'Test3', content = layout2)
        popup.open()
        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press = popup.dismiss)   

# Main Kivy class
class BoxLayoutApp(App):

   def build(self):
      # Outer vertical box
      outerBox = BoxLayout(orientation='vertical')

      # For widgets next to each other,
      Row1 = BoxLayout(orientation='horizontal')


      # Create buttons for Row 1
      btn1 = Button(text="One",
          background_normal='',
          background_color=(1, 0, 0.25, 0.25),
          font_size=25,
          size_hint=(0.7, 1))
      btn2 = Button(text="Two",
          background_normal='',
          background_color=(1, 1, 0.5, 0.8),
          font_size=25,
          size_hint=(0.7, 1))

      # Add buttons to Row 1
      Row1.add_widget(btn1)
      Row1.add_widget(btn2)

      #Buttons for row 2 and 3
      Row_2_3 = BoxLayout(orientation='vertical')

      btn3 = Button(text="Three",
          background_normal='',
          background_color=(1,0,0,0.75),
          font_size=25,
          size_hint=(1, 10))
      btn4 = Button(text="Four",
          background_normal='',
          background_color=(0,1,0,0.75),
          font_size=25,
          size_hint=(1, 15))

      # Add buttons to Row 2 and 3
      Row_2_3.add_widget(btn3)
      Row_2_3.add_widget(btn4)

      # Add all widgets to outerbox
      outerBox.add_widget(Row1)
      outerBox.add_widget(Row_2_3)
      return outerBox
'''
    def button_press(self, button):
        layout_1 = BoxLayout(orientation = 'Horizontal')
        Brad = Button (text = "why Brad?")
        pop_up = Popup(text = "anything", content = )'''



# creating the object root for BoxLayoutApp() class
main_layout = BoxLayoutApp()
main_layout.run()



if __name__ == '__main__':
    widget_1().run()


