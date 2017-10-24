#!/usr/bin/python3.5

from raspireader import RasPiReaderApp
import os

def main():
    if os.geteuid() != 0:
        exit("Needs root permissions to berform dd operations.")
    else:
        print("Passed root check.")

    RasPiReaderApp().run()
    print("Quit complete.")


if __name__ == '__main__':
    main()
