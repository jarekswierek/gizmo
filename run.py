# -*- coding: utf-8 -*-
from Tkinter import Tk

from core import MainView
from settings import GEOMETRY


def main():
    root = Tk()
    root.geometry(GEOMETRY)
    MainView(root)
    root.mainloop()


if __name__ == '__main__':
    main()
