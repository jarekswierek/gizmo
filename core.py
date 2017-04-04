# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from Tkconstants import END, CENTER, VERTICAL, Y, LEFT
from Tkinter import RIGHT, BOTH, RAISED, Label, Entry, Listbox, Scrollbar, \
    Button, TclError
import tkMessageBox
from ttk import Frame, Style
from functools import partial
from clipboard import Clipboard

import settings
from database import GizmoDB


class MainView(Frame):
    """Main View.
    """
    db = GizmoDB()

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.init_ui()

    def save_data(self, entry_name, entry_login, entry_password,
                  listbox_accounts):
        """Save new data.
        """
        name = entry_name.get()
        login = entry_login.get()
        password = entry_password.get()
        if all([name, login, password]):
            data = {
                'name': name,
                'login': login,
                'password': password
            }
            code, msg = self.db.save(data)
            if code == GizmoDB.SUCCESS_CODE:
                tkMessageBox.showinfo(message=msg)
            else:
                tkMessageBox.showwarning(message=msg)
        else:
            tkMessageBox.showwarning(message='Please fill all fields.')
        self.update_listbox_accounts(listbox_accounts)
        entry_name.delete(0, END)
        entry_login.delete(0, END)
        entry_password.delete(0, END)

    def copy_value(self, listbox_accounts, field_name):
        """Copy value from database to clipboard.
        """
        try:
            name = listbox_accounts.get(listbox_accounts.curselection())
        except TclError:
            msg = 'First choose an account from a list'
            tkMessageBox.showinfo(message=msg)
        else:
            data = self.db.load()
            row = [row for row in data if row.get('name') == name]
            if len(row) > 0:
                Clipboard.copy(row[0].get(field_name))
            else:
                msg = 'We have some problems with copy value :('
                tkMessageBox.showwarning(message=msg)

    def copy_login(self, listbox_accounts):
        """Copy login of selected account to clipboard.
        """
        self.copy_value(listbox_accounts, 'login')

    def copy_password(self, listbox_accounts):
        """Copy password of selected account to clipboard.
        """
        self.copy_value(listbox_accounts, 'password')

    def update_listbox_accounts(self, listbox_accounts):
        """Refresh listbox with accounts.
        """
        listbox_accounts.delete(0, END)
        for account in self.db.get_accounts():
            listbox_accounts.insert(END, account)

    def init_ui(self):
        self.parent.title(settings.APP_NAME)
        self.style = Style()
        self.style.theme_use('default')

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        # label
        label_name = Label(frame, text='Label')
        entry_name = Entry(frame, borderwidth=5, justify=CENTER, width=40)
        label_name.pack()
        entry_name.pack(padx=35, pady=5)

        # login
        label_login = Label(frame, text='Login')
        entry_login = Entry(frame, borderwidth=5, justify=CENTER, width=40)
        label_login.pack()
        entry_login.pack(padx=35, pady=5)

        # password
        label_password = Label(frame, text='Pasword')
        entry_password = Entry(frame, show='*', borderwidth=5, justify=CENTER, width=40)
        label_password.pack()
        entry_password.pack(padx=35, pady=5)

        # listbox
        scrollbar = Scrollbar(frame, orient=VERTICAL)
        label_listbox_accounts = Label(frame, text='Accounts')
        listbox_accounts = Listbox(frame, borderwidth=5, width=60,
                                   yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox_accounts.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        label_listbox_accounts.pack()
        listbox_accounts.pack(side=LEFT, fill=BOTH)
        self.update_listbox_accounts(listbox_accounts)

        self.pack(fill=BOTH, expand=True)

        # buttons
        button_save = Button(self, text='Save', command=partial(
            self.save_data, entry_name, entry_login, entry_password,
            listbox_accounts))
        button_save.pack(side=RIGHT, padx=5, pady=5)
        button_quit = Button(self, text='Quit', command=self.quit)
        button_quit.pack(side=RIGHT)

        button_copy_login = Button(
            self, text='Get Login',
            command=partial(self.copy_login, listbox_accounts),
            activebackground='lightgreen', background='lightgreen',
            highlightbackground='lightgreen')
        button_copy_login.pack(side=LEFT, padx=5, pady=5)

        button_copy_pass = Button(
            self, text='Get Password',
            command=partial(self.copy_password, listbox_accounts),
            activebackground='lightgreen', background='lightgreen',
            highlightbackground='lightgreen')
        button_copy_pass.pack(side=LEFT)
