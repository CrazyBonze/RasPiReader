# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

import tkinter as tk
from persistent_data import PersistentData
from wifi import *
from download_img import *

LARGE_FONT= ("Verdana", 12)

def navbar(frame, controller, current_page):
    #start button
    button1 = tk.Button(frame, text="Start",
        command=lambda: controller.show_frame(StartPage))
    button1.grid(row=0, column=0)
    #options button
    button2 = tk.Button(frame, text="Options",
        command=lambda: controller.show_frame(OptionsPage))
    button2.grid(row=0, column=1)
    #commit button
    button3 = tk.Button(frame, text="Commit",
        command=lambda: controller.show_frame(CommitPage))
    button3.grid(row=0, column=2)
    #backup button
    button4 = tk.Button(frame, text="Backup",
        command=lambda: controller.show_frame(BackupPage))
    button4.grid(row=0, column=3)
    label = tk.Label(frame, text=current_page, font=LARGE_FONT)
    label.grid(row=0, column=4)

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

        navbar_frame = tk.Frame(self)
        content_frame = tk.Frame(self)

        navbar(navbar_frame, controller, "Start Page")

        ISO_Entry = make_entry(content_frame, "select iso")
        data.setISOFile(ISO_Entry.get())
        ISO_Entry.grid(row=2, column=0)
        menu = make_menu(content_frame, image_list())

        navbar_frame.grid(row=0)
        content_frame.grid(row=1)

class OptionsPage(tk.Frame):
    def __init__(self, parent, controller):
        self.data = PersistentData()
        self.controller = controller
        tk.Frame.__init__(self, parent)

        self.canvas = tk.Canvas(self)
        navbar_frame = tk.Frame(self)
        self.content_frame = tk.Frame(self.canvas)

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.scrollbar.set)
        navbar_frame.pack()
        self.scrollbar.pack(side=tk.RIGHT, fill= tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.create_window((4,4), window=self.content_frame, anchor="nw")
        self.content_frame.bind("<Configure>", self.onFrameConfigure)

        navbar(navbar_frame, self.controller, "Options Page")
        self.populate()

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    # Add all settings to grid
    def populate(self):
        settings = [
            {"name": "hdmi_safe"},
            {"name": "disable_overscan"},
            {"name": "overscan_left"},
            {"name": "overscan_right"},
            {"name": "overscan_top"},
            {"name": "overscan_bottom"},
            {"name": "framebuffer_width"},
            {"name": "framebuffer_height"},
            {"name": "hdmi_force_hotplug"},
            {"name": "hdmi_group"},
            {"name": "hdmi_mode"},
            {"name": "hdmi_drive"},
            {"name": "config_hdmi_boost"},
            {"name": "sdtv_mode"},
            {"name": "arm_freq"},
            {"name": "i2c"},
            {"name": "i2s"},
            {"name": "spi"},
            {"name": "lirc-rpi"},
            {"name": "audio"}
        ]
        current_row = 1
        for setting in settings:
           tk.Label(self.content_frame, text=setting["name"]).grid(row=current_row, column=0)
           make_entry(self.content_frame, "").grid(row=current_row, column=1)
           current_row = current_row + 1

        button1 = tk.Button(self.content_frame, text="Next",
            command=lambda: self.controller.show_frame(CommitPage))
        button1.grid(row=current_row, column=4)

class CommitPage(tk.Frame):
    def __init__(self, parent, controller):
        data = PersistentData()
        tk.Frame.__init__(self, parent)

        navbar_frame = tk.Frame(self)
        content_frame = tk.Frame(self)

        navbar(navbar_frame, controller, "Commit Page")

        navbar_frame.grid(row=0)
        content_frame.grid(row=1)

class BackupPage(tk.Frame):
    def __init__(self, parent, controller):
        data = PersistentData()
        tk.Frame.__init__(self, parent)

        navbar_frame = tk.Frame(self)
        content_frame = tk.Frame(self)

        navbar(navbar_frame, controller, "Backup Page")

        navbar_frame.grid(row=0)
        content_frame.grid(row=1)


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

