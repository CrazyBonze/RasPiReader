# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

import tkinter as tk
from persistent_data import PersistentData
from wifi import *
from download_img import *
from list_disk import *
from write_config import *
from dd import *

LARGE_FONT= ("Verdana", 12)

def navbar(frame, controller, current_page):
    buttons = [
        {
            "name": "Start",
            "page": StartPage
        },
        {
            "name": "Options",
            "page": OptionsPage
        },
        {
            "name": "Commit",
            "page": CommitPage
        },
        {
            "name": "Backup",
            "page": BackupPage
        }
    ]
    current_column = 0
    for button in buttons:
        # The lambda binds to button so it will not be overwritten on next iteration.
        b = tk.Button(frame, text=button["name"], command=lambda button=button: controller.show_frame(button["page"]))
        b.grid(row=0, column=current_column)
        current_column = current_column + 1

    label = tk.Label(frame, text=current_page, font=LARGE_FONT)
    label.grid(row=0, column=current_column)

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

        navbar(navbar_frame, controller, "Start Page")

        self.populate()

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def populate(self):
        iso_label = tk.Label(self.content_frame, text="local img")
        iso_label.grid(row=0, sticky=tk.W)
        iso_var = tk.StringVar(self.content_frame)
        ISO_Menu = make_menu(self.content_frame, iso_var, directory_list())
        ISO_Menu.grid(row=0, column=1, columnspan=2, sticky=tk.W)
        self.data.setISOFile(iso_var.get())

        img_label = tk.Label(self.content_frame, text="get img")
        img_label.grid(row=1, sticky=tk.W)
        img_var = tk.StringVar(self.content_frame)
        DL_Img_Menu = make_menu(self.content_frame, img_var, image_list())
        DL_Img_Menu.grid(row=1, column=1, columnspan=2, sticky=tk.W)
        self.data.setISODownloadImg(img_var.get())

        dsk_label = tk.Label(self.content_frame, text="SD card")
        dsk_label.grid(row=2, sticky=tk.W)
        dsk_var = tk.StringVar(self.content_frame)
        Disks_Menu = make_menu(self.content_frame, dsk_var, list_disks())
        Disks_Menu.grid(row=2, column=1, columnspan=2, sticky=tk.W)
        self.data.setDiskSD(dsk_var.get())

        next_button = tk.Button(self.content_frame, text="Next",
            command=lambda: self.controller.show_frame(OptionsPage))
        next_button.grid(row=12, column=12)

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


    def next_button_callback(self):
        new_settings = {}
        for key, value in self.entries.items():
            new_settings[key] = value.get()
        self.data.setSettings(new_settings)
        self.controller.show_frame(CommitPage)

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
        current_settings = self.data.getSettings()
        self.entries = {}
        for setting in settings:
            tk.Label(self.content_frame, text=setting["name"]).grid(row=current_row, column=0)
            value = tk.StringVar()
            # Get setting's value from data or default to ""
            value.set(current_settings.get(setting["name"], ""))
            # Make entry with default value of settings
            entry = make_entry(self.content_frame, value.get())
            entry.grid(row=current_row, column=1)
            self.entries[setting["name"]] = entry
            current_row = current_row + 1

        next_button = tk.Button(self.content_frame, text="Next", command=self.next_button_callback)
        next_button.grid(row=current_row, column=4)


class CommitPage(tk.Frame):
    def __init__(self, parent, controller):
        self.data = PersistentData()
        tk.Frame.__init__(self, parent)

        navbar_frame = tk.Frame(self)
        content_frame = tk.Frame(self)

        navbar(navbar_frame, controller, "Commit Page")
        commit_button = tk.Button(content_frame, text="Commit", command=self.commit_button_callback)
        commit_button.grid(row=7, column=4)

        navbar_frame.grid(row=0)
        content_frame.grid(row=1)

    def commit_button_callback(self):
        sdcard = self.data.getDiskSD()
        dd(self.data.getISOFile, sdcard)
        write_config(sdcard, self.data.getSettings())

class BackupPage(tk.Frame):
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

        navbar(navbar_frame, controller, "Backup Page")

        self.populate()

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def populate(self):
        dsk_label = tk.Label(self.content_frame, text="SD card")
        dsk_label.grid(row=2, sticky=tk.W)
        dsk_var = tk.StringVar(self.content_frame)
        Disks_Menu = make_menu(self.content_frame, dsk_var, list_disks())
        Disks_Menu.grid(row=2, column=1, columnspan=2, sticky=tk.W)
        self.data.setDiskSD(dsk_var.get())

        next_button = tk.Button(self.content_frame, text="Backup",
            command=lambda: self.Backup())
        next_button.grid(row=12, column=12)

    def Backup(self):
        print("backup")

def make_entry(parent, caption, width=None, **options):
    tk.Label(parent, text=caption)
    entry = tk.Entry(parent, **options)
    entry.insert(0, caption)
    if width:
        entry.config(width=sidth)
    return entry

def make_menu(parent, var, options):
    #var = tk.StringVar(parent)
    var.set(options[0])
    return tk.OptionMenu(parent, var, *options)

def make_checkbutton(parent, var, caption, onval=1, offval=0):
    #var = tk.StringVar()
    return tk.Checkbutton(parent,
            text=caption,
            variable=var,
            onvalue=onval,
            offvalue=offval)

