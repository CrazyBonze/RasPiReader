#!/usr/bin/python3.5

from raspireader import RasPiReaderApp
import os, argparse

def main():
    #TODO finish the command line arguments stuff
    app = argparse.ArgumentParser(
            prog='RasPiReader',
            description='RasPiReader is a program for helping with burning and modifying images for the Rasperry Pi computer.')
    app.add_argument('--version', action='version', version='%(prog)s 0.1')

    #TODO check for sudo disable command line argument
    if os.geteuid() != 0:
        exit("Needs root permissions to berform dd operations.")
    else:
        print("Passed root check.")

    #TODO run in debug mode if command line argument exists
    RasPiReaderApp().run()
    print("Quit complete.")


if __name__ == '__main__':
    main()
