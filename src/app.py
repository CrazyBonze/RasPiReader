# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

import tkinter as tk
from persistent_data import PersistentData
from wifi import *

LARGE_FONT= ("Verdana", 12)

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        data = PersistentData()
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("460x460+300+300")
        self.title("RasPiReader")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, OptionsPage, CommitPage, BackupPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        data = PersistentData()
        tk.Frame.__init__(self, parent)
        #start button
        button1 = tk.Button(self, text="Start",
                command=lambda: controller.show_frame(StartPage))
        button1.pack(side=tk.LEFT, anchor=tk.N)
        #options button
        button2 = tk.Button(self, text="Options",
                command=lambda: controller.show_frame(OptionsPage))
        button2.pack(side=tk.LEFT, anchor=tk.N)
        #commit button
        button3 = tk.Button(self, text="Commit",
                command=lambda: controller.show_frame(CommitPage))
        button3.pack(side=tk.LEFT, anchor=tk.N)
        #backup button
        button4 = tk.Button(self, text="Backup",
                command=lambda: controller.show_frame(BackupPage))
        button4.pack(side=tk.LEFT, anchor=tk.N)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(anchor=tk.N)

        ISO_Entry = make_entry(self, "select iso")
        ISO_Entry.pack(anchor=tk.W)
        data.setISOFile(ISO_Entry.get())

        ISO_Menue = make_menu(self, ssid_scan())
        ISO_Menue.pack()





class OptionsPage(tk.Frame):
    def __init__(self, parent, controller):
        data = PersistentData()
        #print(data.getISOFile())
        tk.Frame.__init__(self, parent)
        #start button
        button1 = tk.Button(self, text="Start",
                command=lambda: controller.show_frame(StartPage))
        button1.pack(side=tk.LEFT, anchor=tk.N)
        #options button
        button2 = tk.Button(self, text="Options",
                command=lambda: controller.show_frame(OptionsPage))
        button2.pack(side=tk.LEFT, anchor=tk.N)
        #commit button
        button3 = tk.Button(self, text="Commit",
                command=lambda: controller.show_frame(CommitPage))
        button3.pack(side=tk.LEFT, anchor=tk.N)
        #backup button
        button4 = tk.Button(self, text="Backup",
                command=lambda: controller.show_frame(BackupPage))
        button4.pack(side=tk.LEFT, anchor=tk.N)
        label = tk.Label(self, text="Options Page", font=LARGE_FONT)
        label.pack(anchor=tk.N)

        ISO_Entry = make_entry(self, data.getISOFile())
        ISO_Entry.pack(anchor=tk.W)
        data.setISOFile(ISO_Entry.get())

class CommitPage(tk.Frame):
    def __init__(self, parent, controller):
        data = PersistentData()
        tk.Frame.__init__(self, parent)
        #start button
        button1 = tk.Button(self, text="Start",
                command=lambda: controller.show_frame(StartPage))
        button1.pack(side=tk.LEFT, anchor=tk.N)
        #options button
        button2 = tk.Button(self, text="Options",
                command=lambda: controller.show_frame(OptionsPage))
        button2.pack(side=tk.LEFT, anchor=tk.N)
        #commit button
        button3 = tk.Button(self, text="Commit",
                command=lambda: controller.show_frame(CommitPage))
        button3.pack(side=tk.LEFT, anchor=tk.N)
        #backup button
        button4 = tk.Button(self, text="Backup",
                command=lambda: controller.show_frame(BackupPage))
        button4.pack(side=tk.LEFT, anchor=tk.N)
        label = tk.Label(self, text="Commit Page", font=LARGE_FONT)
        label.pack(anchor=tk.N)

class BackupPage(tk.Frame):
    def __init__(self, parent, controller):
        data = PersistentData()
        tk.Frame.__init__(self, parent)
        #start button
        button1 = tk.Button(self, text="Start",
                command=lambda: controller.show_frame(StartPage))
        button1.pack(side=tk.LEFT, anchor=tk.N)
        #options button
        button2 = tk.Button(self, text="Options",
                command=lambda: controller.show_frame(OptionsPage))
        button2.pack(side=tk.LEFT, anchor=tk.N)
        #commit button
        button3 = tk.Button(self, text="Commit",
                command=lambda: controller.show_frame(CommitPage))
        button3.pack(side=tk.LEFT, anchor=tk.N)
        #backup button
        button4 = tk.Button(self, text="Backup",
                command=lambda: controller.show_frame(BackupPage))
        button4.pack(side=tk.LEFT, anchor=tk.N)
        label = tk.Label(self, text="Backup Page", font=LARGE_FONT)
        label.pack(anchor=tk.N)


def make_entry(parent, caption, width=None, **options):
    tk.Label(parent, text=caption)
    entry = tk.Entry(parent, **options)
    entry.insert(0, caption)
    if width:
        entry.config(width=sidth)
    return entry

def make_menu(parent, options):
    var = tk.StringVar(parent)
    var.set(options[0])
    return tk.OptionMenu(parent, var, *options)
