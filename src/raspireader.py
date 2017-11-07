# Kivy files
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.selectableview import SelectableView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.properties import NumericProperty, ObjectProperty, StringProperty, BooleanProperty
from kivy.core.window import Window
from kivy.adapters.listadapter import ListAdapter
from kivy.network.urlrequest import UrlRequest
import os, threading, zipfile, re
from functools import partial
from threading import Thread
from download_img import *
from list_disk import *
from flash import *
import json

# Persistent Data
from persistent_data import PersistentData
data = PersistentData()

class DownloadButton(Button):
    image = StringProperty()

class DownloadIMGDialog(Popup):
    stop = threading.Event()
    def getdownloadlist(self):
        download_list = data.getDownloadImg()
        if not download_list:
            print("Fetching download list")
            self.ids.layout2.add_widget(Label(text='Loading...'))
            Thread(target=self.scrollPopup).start()
        else:
            print("already fetched download list")
            self.scrollPopup()

    def scrollPopup(self):
        images = image_list()
        data.setDownloadImg(images)
        scrlv = self.ids.scroll_view
        s = self.ids.slider
        layout2 = self.ids.layout2
        layout2.clear_widgets()
        scrlv.bind(scroll_y=partial(self.slider_change, s))
        s.bind(value=partial(self.scroll_change, scrlv))
        layout2.bind(minimum_height=layout2.setter('height'))
        for i in images:
            btn = DownloadButton()
            btn.image = i
            layout2.add_widget(btn)

    def scroll_change(self, scrlv, instance, value):
        scrlv.scroll_y = value

    def slider_change(self, s, instance, value):
        if value >= 0:
            s.value = value

    def setDLImage(self, img):
        self.dl_image = img
        self.dl_disable = False
        self.dismiss()

    def cancel(self):
        self.dl_image = "Pick Image"
        self.dl_disable = True
        self.dismiss()

class LoadIMGDialog(Popup):
    def load(self, path, selection):
        if not selection:
            return
        self.choosen_file = selection[0]
        Window.title = selection[0][selection[0].rfind(os.sep) + 1:]
        data.setIMGFile(selection[0])
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
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

    def print_to_screen(self):
        data.print_to_screen()

class PageManager(ScreenManager):
    pass

class DownloadProgress(Popup):
    image = StringProperty()
    stop = threading.Event()
    zip_file = ""

    def download_content(self, f):
        file_tuple = download_img(f)
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

    def cancel(self):
        #delete partial file
        os.remove(self.zip_file)
        self.dismiss()

class StartPage(Screen):
    img_file = StringProperty('No Image Chosen')
    download_file = StringProperty('Pick Image')
    download_disable = BooleanProperty(True)
    def get_img_file(self):
        return data.getIMGFile()

    def file_pick(self):
        self.load_dialog = LoadIMGDialog()
        self.load_dialog.open()
        self.load_dialog.bind(choosen_file=self.setter('img_file'))

    def download_pick(self):
        self.download_dialog = DownloadIMGDialog()
        self.download_dialog.open()
        self.download_dialog.bind(dl_image=self.setter('download_file'))
        self.download_dialog.bind(dl_disable=self.setter('download_disable'))
        self.download_dialog.getdownloadlist()

    def download_image(self, f):
        self.download_progress = DownloadProgress()
        self.download_progress.image = f
        self.download_progress.open()
        self.download_progress.download_content(f)

class SettingInfo(GridLayout):
    pass

class TextSetting(GridLayout):
    enable = BooleanProperty()
    pass

class BoolSetting(GridLayout):
    enable = BooleanProperty()
    state = BooleanProperty(True)
    def get_state(self):
        print(state)

class SliderSetting(GridLayout):
    enable = BooleanProperty(True)
    pass

class Setting(GridLayout):
    def __init__(self, label, setting, **kwargs):
        super(Setting, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)
        self._setting = setting
        self.label = label

    def _finish_init(self, dt):
        self.cols = 2
        self.height = 100
        self.setting_type = ''
        try:
            self.setting_type = self._setting['type']
            info = SettingInfo()
            info.ids.name.text = self._setting['name']
            info.ids.enable.value = self._setting['enable']
            self.add_widget(info)
        except:
            print("error")
        if(self.setting_type == 'bool'):
            bset = BoolSetting()
            self.add_widget(bset)
        elif(self.setting_type == 'slider'):
            sldr = SliderSetting()
            sldr.ids.slider.min = self._setting['min']
            sldr.ids.slider.max = self._setting['max']
            sldr.ids.slider.value = self._setting['default']
            self.add_widget(sldr)
        elif(self.setting_type == 'text'):
            text = TextSetting()
            self.add_widget(text)
        else:
            self.add_widget(Label(text=self.label))


class OptScreen(Screen):
    def __init__(self, settings, **kwargs):
        super(OptScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._finish_init)
        self._settings = settings

    def _finish_init(self, dt):
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        for setting in self._settings:
            s = Setting(setting['name'], setting)
            s.size_hint_y = None
            s.height = 60
            self.layout.add_widget(s)
        self.view = ScrollView(size=self.size, scroll_type=['bars'])
        self.add_widget(self.view)
        self.view.add_widget(self.layout)

class OptionsPage(Screen):
    def __init__(self, **kwargs):
        super(OptionsPage, self).__init__(**kwargs)
        with open('options.json') as options_data:
            self.opts = json.load(options_data)
        Clock.schedule_once(self._finish_init)

    def _finish_init(self, dt):
        self.optionsmenue = self.ids.optionsmenue
        self.optionsmanager = self.ids.optionsmanager
        for section in self.opts['sections']:
            btn = Button(text=section['title'])
            btn.bind(on_release=lambda btn: self.switchpage(btn.text))
            self.optionsmenue.add_widget(btn)
            screen = OptScreen(section['settings'])
            screen.name = section['title']
            self.optionsmanager.add_widget(screen)

    def switchpage(self, page):
        print(page)
        self.optionsmanager.current = page

class FlashProgress(Popup):
    image = StringProperty()
    disk = StringProperty()
    progress_counter = StringProperty("0% eta 0s")
    progress_value = NumericProperty(0)
    check = BooleanProperty()
    unmount = BooleanProperty()

    def __init__(self, **kwargs):
        super(FlashProgress, self).__init__(**kwargs)
        self.f = None
        self.event = None
        self.image = data.getIMGFile()
        self.disk = '/dev/{0}'.format(data.getDiskSD()[0])

    def flash_card(self):
        self.f = Flasher(self.disk, self.image, self.unmount, self.validate)
        self.f.flash()
        self.event = Clock.schedule_interval(self.update_progress, 1/25)

    def update_progress(self, dt):
        update = self.f.read()
        if update in Exit_code:
            self.ids['progress_area'].clear_widgets()
            status = Label(text=update)
            self.ids['progress_area'].add_widget(status)
            self.event.cancel()
            self.ids['command_button'].clear_widgets()
            finish_btn = Button(text= "Dismiss")
            finish_btn.bind(on_release=lambda x: self.finish())
            self.ids['command_button'].add_widget(finish_btn)
        elif update:
            regex = re.compile(".*\[(.*?)\]")
            prog = ''
            try:
                prog = '[{0}]'.format(re.findall(regex, update)[0])
                update = update.replace(prog, '')
                self.progress_counter = update
                value = re.search(r'\d+', update)
                if value:
                    self.progress_value = int(value.group())/100
            except:
                print(update)

    def finish(self):
        self.dismiss()

    def cancel(self):
        self.f.kill()
        self.event.cancel()
        self.dismiss()

class CommitPage(Screen):
    commit_disable = BooleanProperty(True)
    sd = StringProperty("SD card")
    def __init__(self, **kwargs):
        super(CommitPage, self).__init__(**kwargs)
        self.dd = DropDown()

    def sd_dd(self):
        types = list_disks()
        if not types:
            self.dd.clear_widgets()
            self.sd = "SD card"
            self.commit_disable = True
            return
        self.dd.clear_widgets()
        for i in types:
            btn = Button(text=i, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.dd.select(btn.text))
            self.dd.add_widget(btn)
        self.ids['dd_btn'].bind(on_release=self.dd.open)
        self.dd.bind(on_select=lambda instance, x: self.pick_sd(x))

    def pick_sd(self, x):
        self.sd = x
        data.setDiskSD(x)
        self.commit_disable = False

    def commit(self):
        if data.validate():
            print("Commiting to SD card")
            self.flash_progress = FlashProgress()
            self.flash_progress.validate = self.ids['validate'].active
            self.flash_progress.unmount = self.ids['unmount'].active
            self.flash_progress.flash_card()
            self.flash_progress.open()
        else:
            print("Failed to validate")

class BackupPage(Screen):
    pass

class RasPiReaderApp(App):
    def on_stop(self):
        self.root.stop.set()

    def build(self):
        img_dir_exists()
        root = RootWidget()
        return root
