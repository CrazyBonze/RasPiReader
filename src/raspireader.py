# Kivy files
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty

# Persistent Data
from persistent_data import PersistentData
data = PersistentData()

class HeaderButtons(BoxLayout):
    pass

class Header(AnchorLayout):
    pass

class PageLayer(AnchorLayout):
    pass

class FooterButtons(BoxLayout):
    pass

class Footer(AnchorLayout):
    pass

class RootWidget(FloatLayout):
    def print_to_screen(self, txt):
        data.writeToFile(txt)
        #print(txt)

class PageManager(ScreenManager):
    pass

class StartPage(Screen):
    def print_to_screen(self):
        print("hello world")

class OptionsPage(Screen):
    pass

class CommitPage(Screen):
    pass

class BackupPage(Screen):
    pass

class RasPiReaderApp(App):
    def build(self):
        root = RootWidget()
        return root
