#/usr/bin/python3.5
from tkinter import *

class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        #Button().grid(row=self.row, column=self.column)
        self.buttons = [
                { 'name':'Start',   'function':self.Start },
                { 'name':'Options', 'function':self.Options },
                { 'name':'Commit',  'function':self.Commit },
                { 'name':'Backup',  'function':self.Backup }
                ]
        self.BuildButtons(self.buttons)

    def BuildButtons(self, buttons):
        pos = 0
        for b in self.buttons:
            label = b['name']
            y = Button(self.parent, text=b['name'], command=b['function'])
            y.grid(row=3, column=2+pos)
            pos = pos + 2


    def Start(self):
        print("hello from start.")

    def Options(self):
        print("hello from boot loader")

    def Commit(self):
        print("hello from commit")

    def Backup(self):
        print("hello from Backup")



    def initUI(self):
        self.parent.title("RasPiReader")
        #self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)

