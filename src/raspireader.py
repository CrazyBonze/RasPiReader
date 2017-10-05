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
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window
from kivy.adapters.listadapter import ListAdapter
from kivy.network.urlrequest import UrlRequest
import os, threading, zipfile, re
from threading import Thread
from download_img import *
from list_disk import *

# Persistent Data
from persistent_data import PersistentData
data = PersistentData()

class DownloadButton(Button):
    image = StringProperty()

class DownloadISODialog(Popup):
    stop = threading.Event()
    def getdownloadlist(self):
        download_list = data.getDownloadImg()
        if not download_list:
            print("Fetching download list")
            self.ids.scroll_view.add_widget(Label(text='Loading...'))
            Thread(target=self.worker).start()
        else:
            print("already fetched download list")
            self.layout = GridLayout(cols=1, size_hint_y=None)
            self.layout.bind(minimum_height=self.layout.setter('height'))
            self.ids.scroll_view.add_widget(self.layout)
            for i in download_list:
                btn = DownloadButton()
                btn.image = i
                self.layout.add_widget(btn)

    def worker(self):
        images = image_list()
        self.ids.scroll_view.clear_widgets()
        data.setDownloadImg(images)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.ids.scroll_view.add_widget(self.layout)
        for i in images:
            btn = DownloadButton()
            btn.image = i
            self.layout.add_widget(btn)

    def setDLImage(self, img):
        self.dl_image = img
        self.dismiss()

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

class DownloadProgress(Popup):
    image = StringProperty()
    stop = threading.Event()
    zip_file = ""

    def download_content(self, f):
        file_tuple = download_iso(f)
        self.zip_file = file_tuple[1]
        req = UrlRequest(file_tuple[0], on_progress=self.update_progress,
                chunk_size=32768, on_success=self.finish,
                file_path=file_tuple[1])


    def update_progress(self, request, current_size, total_size):
        progress = current_size / total_size
        self.ids['download_progress_counter'].text = \
            'Downloading {0:.2f}%'.format(progress*100)
        self.ids['download_progress_bar'].value = progress

    def finish(self, request, result):
        threading.Thread(target=self.unzip_content).start()
        self.ids['progress_area'].clear_widgets()
        self.ids['progress_area'].add_widget(Label(text='Unzipping...'))

    def unzip_content(self):
        #TODO update to show that it is unzipping
        print("Unzipping file")
        #unzip file
        fh = open(self.zip_file, 'rb')
        z = zipfile.ZipFile(fh)
        ZIP_EXTRACT_FOLDER = re.sub(r'\.[zZ][iI][pP]', '', self.zip_file)
        if not os.path.exists(ZIP_EXTRACT_FOLDER):
            os.makedirs(ZIP_EXTRACT_FOLDER)
        z.extractall(ZIP_EXTRACT_FOLDER)
        fh.close()
        os.remove(self.zip_file)
        self.dismiss()

    def suspend(self):
        #leave partial file
        self.dismiss()

    def cancel(self):
        #delete partial file
        os.remove(self.zip_file)
        self.dismiss()

class StartPage(Screen):
    iso_file = StringProperty('No Image Chosen')
    download_file = StringProperty('Pick Image')
    def get_iso_file(self):
        return data.getISOFile()

    def file_pick(self):
        self.load_dialog = LoadISODialog()
        self.load_dialog.open()
        self.load_dialog.bind(choosen_file=self.setter('iso_file'))

    def download_pick(self):
        self.download_dialog = DownloadISODialog()
        self.download_dialog.open()
        self.download_dialog.bind(dl_image=self.setter('download_file'))
        self.download_dialog.getdownloadlist()

    def download_image(self, f):
        self.download_progress = DownloadProgress()
        self.download_progress.image = f
        self.download_progress.open()
        self.download_progress.download_content(f)


class OptionsPage(Screen):
    pass

class DropDownButton(Button):
    sd_card = StringProperty("SD card")
    def __init__(self, **kwargs):
        super(DropDownButton, self).__init__(**kwargs)
        self.drop_list = None
        self.drop_list = DropDown()
        self.types = []

    def update(self):
        self.types = list_disks()
        if not self.types:
            self.drop_list.clear_widgets()
            setattr(self, 'text', "SD card")
            return
        self.drop_list.clear_widgets()
        for i in self.types:
            btn = Button(text=i, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: self.drop_list.select(btn.text))
            self.drop_list.add_widget(btn)
        self.bind(on_release=self.drop_list.open)
        self.drop_list.bind(on_select=lambda instance, x: setattr(self, 'text', x))


class CommitPage(Screen):
    sd_dropdown = DropDown()

    def get_list(self):
        print(self.sd_options)

class BackupPage(Screen):
    pass

class RasPiReaderApp(App):
    def on_stop(self):
        self.root.stop.set()

    def build(self):
        img_dir_exists()
        root = RootWidget()
        return root
