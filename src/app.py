#!/usr/bin/python3.5
#import tkinter as tk   # python3
#import Tkinter as tk   # python
# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import tkinter as tk


LARGE_FONT= ("Verdana", 12)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("460x460+300+300")
        self.title("RasPiReader")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, OptionsPage, CommitPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.buttons = [
                {   'name':'Start',
                    'function':self.Start,
                    'cont':StartPage },
                {   'name':'Options',
                    'function':self.Options,
                    'cont':OptionsPage }
                ]
        self.BuildButtons(self.buttons, controller)

    def BuildButtons(self, buttons, controller):
        pos = 0
        for b in self.buttons:
            label = b['name']
            y = tk.Button(self, text=b['name'],
                    command=lambda: controller.show_frame(b['cont']))
            y.pack()

    def Start(self):
        self.controller.show_rame(PageOne)
        print("hello from start")

    def Options(self):
        print("hellow from options")


class StartPage(Screen):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.buttons = [
                {   'name':'Start',
                    'function':self.Start,
                    'cont':StartPage },
                {   'name':'Options',
                    'function':self.Options,
                    'cont':OptionsPage }
                ]
        self.BuildButtons(self.buttons, controller)

    def BuildButtons(self, buttons, controller):
        pos = 0
        for b in self.buttons:
            label = b['name']
            y = tk.Button(self, text=b['name'],
                    command=lambda: controller.show_frame(b['cont']))
            y.pack()

    def Start(self):
        self.controller.show_rame(PageOne)
        print("hello from start")

    def Options(self):
        print("hellow from options")




class OptionsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class CommitPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


