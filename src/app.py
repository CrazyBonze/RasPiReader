#/usr/bin/python3.5
from tkinter import *

class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("hello")
        self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)

