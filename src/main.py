#!/usr/bin/python3.5

from app import App
import os

def main():
    if os.geteuid() != 0:
        exit("Needs root permissions to berform dd operations.")
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
