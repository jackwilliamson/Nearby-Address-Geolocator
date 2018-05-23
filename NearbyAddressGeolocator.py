from Tkinter import Tk

import sys
import os

from GUI import GUI
import firebase_admin
from firebase_admin import credentials


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
        relative_path = relative_path +"/"+relative_path
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main():
    cred = credentials.Certificate(resource_path('nearbygeolocatio-1523547949481-firebase-adminsdk-hxbi6-6611129219.json'))
    fb_app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://nearbygeolocatio-1523547949481.firebaseio.com/'})
    root = Tk()
    my_gui = GUI(root)
    root.mainloop()


main()
