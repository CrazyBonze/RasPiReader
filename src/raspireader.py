# Kivy files
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.selectableview import SelectableView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.adapters.listadapter import ListAdapter
import os, threading
from threading import Thread
from download_img import *

# Persistent Data
from persistent_data import PersistentData
data = PersistentData()

class DownloadISODialog(Popup):
    def getdownloadlist(self):
        download_list = data.getDownloadImg()
        if not download_list:
            print("Fetching download list")
            self.ids.scroll_view.add_widget(Label(text='Loading'))
            Thread(target=self.worker).start()
        else:
            print("already fetched download list")
            self.layout = GridLayout(cols=1, size_hint_y=None)
            self.layout.bind(minimum_height=self.layout.setter('height'))
            for i in download_list:
                #print(i)
                btn = Button(text=i, size_hint_y=None, height=30)
                self.layout.add_widget(btn)
            self.ids.scroll_view.add_widget(self.layout)


    def worker(self):
        images = image_list()
        data.setDownloadImg(images)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        for i in images:
            #print(i)
            btn = Button(text=i, size_hint_y=None, height=30)
            self.layout.add_widget(btn)
        self.ids.scroll_view.clear_widgets()
        self.ids.scroll_view.add_widget(self.layout)


    def cancel(self):
        self.dismiss()

class LoadISODialog(Popup):
    def load(self, path, selection):
        if not selection:
            return
        self.choosen_file = selection[0]
        Window.title = selection[0][selection[0].rfind(os.sep) + 1:]
        data.setISOFile(selection[0])
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
    stop = threading.Event()
    def print_to_screen(self):
        data.print_to_screen()

class PageManager(ScreenManager):
    pass

class StartPage(Screen):
    iso_file = StringProperty(data.getISOFile())
    def get_iso_file(self):
        return data.getISOFile()

    def file_pick(self):
        self.load_dialog = LoadISODialog()
        self.load_dialog.open()
        self.load_dialog.bind(choosen_file=self.setter('iso_file'))

    def download_pick(self):
        self.download_dialog = DownloadISODialog()
        self.download_dialog.open()
        self.download_dialog.getdownloadlist()



class OptionsPage(Screen):
    pass

class CommitPage(Screen):
    pass

class BackupPage(Screen):
    pass

class RasPiReaderApp(App):
    def build(self):
        img_dir_exists()
        root = RootWidget()
        return root
