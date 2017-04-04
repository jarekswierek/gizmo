# -*- coding: utf-8 -*-

from Tkinter import Tk


class Clipboard(object):
    """Clipboard tool.
    """
    @classmethod
    def copy(cls, value):
        """Copy value to clipboard.
        """
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(value)
        r.destroy()

    # WARNING - not tested
    # @classmethod
    # def clear_windows_clipboard(cls):
    #     from ctypes import windll
    #     if windll.user32.OpenClipboard(None):
    #         windll.user32.EmptyClipboard()
    #         windll.user32.CloseClipboard()
