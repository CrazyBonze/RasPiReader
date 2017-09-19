from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class StartPage(Screen):
    pass

class OptionsPage(Screen):
    pass

class CommitPage(Screen):
    pass

class BackupPage(Screen):
    pass

#Creating screen manager
sm = ScreenManager()
sm.add_widget(StartPage(name="startpage"))
sm.add_widget(OptionsPage(name="optionspage"))
sm.add_widget(CommitPage(name="commitpage"))
sm.add_widget(BackupPage(name="backupPage"))

class RasPiReaderApp(App):
    def build(self):
        return sm
