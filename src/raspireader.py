# Kivy files
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.core.window import Window
import os

# Persistent Data
from persistent_data import PersistentData
data = PersistentData()

class LoadDialog(Popup):
    def load(self, path, selection):
        self.choosen_file = [None, ]
        self.choosen_file = selection
        Window.title = selection[0][selection[0].rfind(os.sep) + 1:]
        self.dismiss()

    def cancel(self):
        self.dismiss()

class SaveDialog(Popup):
    def save(self, path, selection):
        _file = codect.open(selection, 'w', encoding='utf8')
        _file.write(self.text)
        Window.title = selection[selection.rfind(os.sep) + 1:]
        _file.close()
        self.dismiss()

    def cancel(self):
        self.dismiss()

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
    loadiso = ObjectProperty(None)
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    def print_to_screen(self, txt):
        data.writeToFile(txt)
        #print(txt)

class PageManager(ScreenManager):
    pass

class StartPage(Screen):
    def print_to_screen(self):
        curdir = dirname(__file__)
        print(curdir)
        print("hello world")
    def file_pick(self):
        self.load_dialog = LoadDialog()
        self.load_dialog.open()


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
