#!/usr/bin/python3.5

#from app import App
from raspireader import RasPiReaderApp
import os

def main():
    if os.geteuid() != 0:
        exit("Needs root permissions to berform dd operations.")
    print("in main")
    #app = App()
    #app.mainloop()
    RasPiReaderApp().run()



if __name__ == '__main__':
    print("entering main")
    main()
