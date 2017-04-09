# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

import tkinter as tk
from persistent_data import PersistentData
from wifi import *
from download_img import *

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
        f = tk.Frame(self)
        #start button
        button1 = tk.Button(f, text="Start",
                command=lambda: controller.show_frame(StartPage))
        button1.grid(row=0, column=0)
        #options button
        button2 = tk.Button(f, text="Options",
                command=lambda: controller.show_frame(OptionsPage))
        button2.grid(row=0, column=1)
        #commit button
        button3 = tk.Button(f, text="Commit",
                command=lambda: controller.show_frame(CommitPage))
        button3.grid(row=0, column=2)
        #backup button
        button4 = tk.Button(f, text="Backup",
                command=lambda: controller.show_frame(BackupPage))
        button4.grid(row=0, column=3)
        label = tk.Label(f, text="Start Page", font=LARGE_FONT)
        label.grid(row=0, column=4)

        ISO_Entry = make_entry(f, "select iso")
        data.setISOFile(ISO_Entry.get())
        ISO_Entry.grid(row=2, column=0)

        menu = make_menu(f, image_list())
        f.pack(fill=tk.BOTH, expand=1)




class OptionsPage(tk.Frame):
    def __init__(self, parent, controller):
        data = PersistentData()
        #print(data.getISOFile())
        tk.Frame.__init__(self, parent)
        #start button
        f = tk.Frame(self)
        button1 = tk.Button(f, text="Start",
                command=lambda: controller.show_frame(StartPage))
        button1.grid(row=0, column=0)
        #options button
        button2 = tk.Button(f, text="Options",
                command=lambda: controller.show_frame(OptionsPage))
        button2.grid(row=0, column=1)
        #commit button
        button3 = tk.Button(f, text="Commit",
                command=lambda: controller.show_frame(CommitPage))
        button3.grid(row=0, column=2)
        #backup button
        button4 = tk.Button(f, text="Backup",
                command=lambda: controller.show_frame(BackupPage))
        button4.grid(row=0, column=3)
        label = tk.Label(f, text="Options Page", font=LARGE_FONT)
        label.grid(row=0, column=4)

        ISO_Menue = make_menu(f, ssid_scan())
        ISO_Menue.grid(row=1, column=0)

        ISO_Entry = make_entry(f, data.getISOFile())
        ISO_Entry.grid(row=1, column=1)
        data.setISOFile(ISO_Entry.get())
        f.pack(fill=tk.BOTH, expand=1)

class CommitPage(tk.Frame):
    def __init__(self, parent, controller):
        data = PersistentData()
        tk.Frame.__init__(self, parent)
        f = tk.Frame(self)
        #start button
        button1 = tk.Button(f, text="Start",
                command=lambda: controller.show_frame(StartPage))
        button1.grid(row=0, column=0)
        #options button
        button2 = tk.Button(f, text="Options",
                command=lambda: controller.show_frame(OptionsPage))
        button2.grid(row=0, column=1)
        #commit button
        button3 = tk.Button(f, text="Commit",
                command=lambda: controller.show_frame(CommitPage))
        button3.grid(row=0, column=2)
        #backup button
        button4 = tk.Button(f, text="Backup",
                command=lambda: controller.show_frame(BackupPage))
        button4.grid(row=0, column=3)
        label = tk.Label(f, text="Commit Page", font=LARGE_FONT)
        label.grid(row=0, column=4)
        f.pack(fill=tk.BOTH, expand=1)

class BackupPage(tk.Frame):
    def __init__(self, parent, controller):
        data = PersistentData()
        tk.Frame.__init__(self, parent)
        f = tk.Frame(self)
        #start button
        button1 = tk.Button(f, text="Start",
                command=lambda: controller.show_frame(StartPage))
        button1.grid(row=0, column=0)
        #options button
        button2 = tk.Button(f, text="Options",
                command=lambda: controller.show_frame(OptionsPage))
        button2.grid(row=0, column=1)
        #commit button
        button3 = tk.Button(f, text="Commit",
                command=lambda: controller.show_frame(CommitPage))
        button3.grid(row=0, column=2)
        #backup button
        button4 = tk.Button(f, text="Backup",
                command=lambda: controller.show_frame(BackupPage))
        button4.grid(row=0, column=3)
        label = tk.Label(f, text="Backup Page", font=LARGE_FONT)
        label.grid(row=0, column=4)
        f.pack(fill=tk.BOTH, expand=1)


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

def make_checkbutton(parent, caption, onval=1, offval=0):
    var = tk.StringVar()
    return tk.Checkbutton(parent,
            text=caption,
            variable=var,
            onvalue=onval,
            offvalue=offval)

