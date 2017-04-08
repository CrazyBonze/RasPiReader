#!/usr/bin/python3.5
#from OS import *

from tkinter import Tk
from app import App

def main():
    root = Tk()
    app = App(root)
    root.geometry("460x460+300+300")
    root.mainloop()

if __name__ == '__main__':
    main()
