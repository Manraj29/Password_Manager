from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import random
import string
from main import main


# Home window
class application(main):
    global conn
    global cur
    global usern
    global passw
    global username
    global password
    global frame
    global add
    global edit
    global search
    global delete

    def encrypt_password(self, password):
        password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(10)) + password + ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(10))
        return password


    def decrypt_password(self, password):
        password = password[10:-9]
        return password


    def __init__(self, user, passw):
        # super().__init__()
        self.frame = Tk()
        self.frame.title("Home")
        self.frame.geometry("280x250")
        self.frame.resizable(False, False)
        self.frame.eval('tk::PlaceWindow . center')
        self.usern = user
        self.userxx = user
        self.passw = passw
        fontx = ("Arial", 12, "bold")
        ttk.Label(self.frame, text="Welcome " + user + "!", padding=5).grid(row=0, column=1)
        ttk.Label(self.frame, text="", padding=20).grid(row=0, column=2)
        Button(self.frame, text="Exit", width=8, command=self.logout).grid(row=0, column=4)
        # button 1 for adding new password
        Button(self.frame, text="Add", width=15, command=self.add_password).grid(row=1, column=1, columnspan=2)
        ttk.Label(self.frame, text="", padding=5).grid(row=2, column=1)
        # button 2 for viewing all passwords
        Button(self.frame, text="View", width=15, command=self.view_password).grid(row=1, column=3, columnspan=2)
        ttk.Label(self.frame, text="", padding=5).grid(row=4, column=1)
        # button 3 for deleting a password
        Button(self.frame, text="Delete", width=15, command=self.del_password).grid(row=5, column=1, columnspan=2)
        ttk.Label(self.frame, text="", padding=5).grid(row=6, column=1)
        # button 4 for searching a password
        Button(self.frame, text="Search", width=15, command=self.search_password).grid(row=5, column=3, columnspan=2)

        self.frame.mainloop()

    # When logout is clicked
    def logout(self):
        self.frame.destroy()
        messagebox.showinfo("Logout", "Thank you,\nYour passwords are safe with us!")
        exit(0)

    def insert_password(self):
        main.connect_db(self)
        self.cur.execute(
            "INSERT INTO " + self.usern + " VALUES('" + self.username.get() + "', '" + self.password.get() + "', '" + self.website.get() + "')")
        self.conn.commit()
        messagebox.showinfo("Success", "Password added successfully")
        self.add.destroy()
        self.frame.deiconify()

    # when back is clicked
    def add_back(self):
        self.add.destroy()
        self.frame.deiconify()

    def edit_back(self):
        self.edit.destroy()
        self.search_password()

    def search_back(self):
        self.search.destroy()
        self.frame.deiconify()

    def delete_back(self):
        self.deletex.destroy()
        self.frame.deiconify()

    # when add password is clicked
    def add_password(self):
        self.add = Tk()
        self.add.title("Add Password")
        self.add.geometry("300x280")
        self.add.resizable(False, False)
        self.add.eval('tk::PlaceWindow . center')
        self.frame.withdraw()
        ttk.Label(self.add, text="ADD PASSWORD", padding=5).grid(row=0, column=1)
        ttk.Label(self.add, text="", padding=15).grid(row=0, column=2)
        Button(self.add, text="Back", width=5, command=self.add_back).grid(row=0, column=3)
        # Add username
        ttk.Label(self.add, text="Username", padding=5).grid(row=1, column=1)
        self.username = ttk.Entry(self.add)
        self.username.focus()
        self.username.grid(row=1, column=2)
        # Add password
        ttk.Label(self.add, text="Password", padding=5).grid(row=2, column=1)
        self.password = ttk.Entry(self.add)
        self.password.config(show="*")
        self.password.grid(row=2, column=2)
        # Add website
        ttk.Label(self.add, text="Domain", padding=5).grid(row=3, column=1)
        self.website = ttk.Entry(self.add)
        self.website.grid(row=3, column=2)
        ttk.Label(self.add, text="", padding=4).grid(row=6, column=1)
        # add save button
        Button(self.add, text="Save", width=8, command=self.insert_password).grid(row=7, column=1, columnspan=2)
        ttk.Label(self.add, text="", padding=5).grid(row=8, column=1)
        # add cancel button
        Button(self.add, text="Cancel", width=8, command=self.add_back).grid(row=7, column=2, columnspan=2)
        self.add.focus()
        self.add.mainloop()

    def view_password(self, search_usr=None):
        view = Tk()
        view.title("View Password")
        view.geometry("300x280")
        view.eval('tk::PlaceWindow . center')

        sheet = ttk.Treeview(view)
        sheet["columns"] = ("one", "two")
        sheet.column("#0", width=0, stretch=NO)
        sheet.column("one", anchor=W, width=100)
        sheet.column("two", anchor=W, width=100)
        sheet.heading("#0", text="", anchor=W)
        sheet.heading("one", text="Username", anchor=W)
        sheet.heading("two", text="Domain", anchor=W)
        main.connect_db(self)
        if search_usr is None:
            self.cur.execute("SELECT username, domain FROM " + self.usern)
            rows = self.cur.fetchall()
        else:
            self.cur.execute(
                "SELECT username, domain FROM " + self.usern + " WHERE username LIKE '%" + search_usr + "%'")
            rows = self.cur.fetchall()

        if len(rows) == 0:
            messagebox.showinfo("No Passwords", "No passwords found")
            view.destroy()
            return

        for row in rows:
            sheet.insert("", 0, values=(row[0], row[1]))
        sheet.pack()
        view.eval('tk::PlaceWindow . center')
        view.geometry("300x280")
        Button(view, text="Back", width=5, command=view.destroy).pack()
        view.mainloop()

    def edit_password(self, usern, domain):

        self.edit = Tk()
        self.edit.title("Edit Password")
        self.edit.geometry("300x280")
        self.edit.resizable(False, False)
        self.edit.eval('tk::PlaceWindow . center')
        self.frame.withdraw()
        ttk.Label(self.edit, text="EDIT PASSWORD", padding=5).grid(row=0, column=1)
        ttk.Label(self.edit, text="", padding=15).grid(row=0, column=2)
        Button(self.edit, text="Back", width=5, command=self.edit_back).grid(row=0, column=3)
        # Add username
        ttk.Label(self.edit, text="Username", padding=5).grid(row=1, column=1)
        self.username = ttk.Entry(self.edit)
        self.username.focus()

        self.username.grid(row=1, column=2)
        self.username.insert(0, usern)
        self.username.config(state="readonly")
        main.connect_db(self)

        self.cur.execute("SELECT password FROM " + self.usern + " WHERE username = '" + usern + "' AND domain = '" + domain + "'")


        passn = self.cur.fetchone()

        ttk.Label(self.edit, text="Password", padding=5).grid(row=2, column=1)
        self.password = ttk.Entry(self.edit)
        self.password.config(show="*")
        self.password.grid(row=2, column=2)
        self.password.insert(0, passn[0])
        ttk.Label(self.edit, text="Confirm Password", padding=5).grid(row=3, column=1)
        self.confirm = ttk.Entry(self.edit)
        self.confirm.config(show="*")
        self.confirm.grid(row=3, column=2)
        self.confirm.insert(0, passn[0])

        ttk.Label(self.edit, text="Domain", padding=5).grid(row=4, column=1)
        self.domain = ttk.Entry(self.edit)
        self.domain.grid(row=4, column=2)
        self.domain.insert(0, domain)
        self.domain.config(state="readonly")
        ttk.Label(self.edit, text="", padding=4).grid(row=7, column=1)
        # add save button
        Button(self.edit, text="Save", width=8, command=self.update_password).grid(row=8, column=1, columnspan=2)
        Button(self.edit, text="Delete", width=8, command=self.delete_password).grid(row=8, column=2, columnspan=2)



    def update_password(self):
        main.connect_db(self)
        if self.password.get() == "" or self.confirm.get() == "" or self.domain.get() == "":
            messagebox.showerror("Update Password", "Password or Domain cannot be empty", icon="error")
        elif self.password.get() != self.confirm.get():
            messagebox.showerror("Update Password", "Password and Confirm Password must be same", icon="error")
        else:
            self.cur.execute("UPDATE `" + self.usern + "` SET `password` = '" + self.password.get() + "' WHERE `domain` = '" + self.domain.get() + "' AND `username` = '" + self.username.get() + "';")
            print("UPDATE `" + self.usern + "` SET `password` = '" + self.password.get() + "' WHERE `domain` = '" + self.domain.get() + "' AND `username` = '" + self.username.get() + "';")
            self.conn.commit()
            messagebox.showinfo("Update Password", "Password updated", icon="info")
            self.edit.destroy()
            self.search_password()

    def delete_password(self):
        main.connect_db(self)
        self.cur.execute("DELETE FROM `" + self.usern + "` WHERE `username` = '" + self.username.get() + "' AND `domain` = '" + self.domain.get() + "';")
        self.conn.commit()
        print("DELETE FROM `" + self.usern + "` WHERE `username` = '" + self.username.get() + "' AND `domain` = '" + self.domain.get() + "';")
        messagebox.showinfo("Delete Password", "Password deleted", icon="info")
        self.edit.destroy()
        self.deletex.destroy()
        self.search_password()

    def edit_msg(self):
        messagebox.showinfo("Edit Password",
                            "Continue to check in database?\nIf yes, click 'Check' again\nIf no, click 'Cancel' and try again",
                            icon="warning", type="okcancel")

    def search_msg(self, event=None):
        main.connect_db(self)
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Search Password", "Username or Password cannot be empty", icon="error")
        else:
            if event is None:
                self.cur.execute("SELECT password FROM " + self.usern + " WHERE username = '" + self.username.get() + "'")
                if self.cur.fetchone() is None:
                    messagebox.showerror("Search Password", "No password found", icon="error")
                else:
                    if self.password.get() == self.passw:
                        messagebox.showinfo("Search Password", "Password found", icon="info")
                        self.view_password(self.username.get())
                        self.search.withdraw()
                    else:
                        messagebox.showerror("Search Password", "App password differs", icon="error")
            elif event == "edit":
                if self.domain.get() == "":
                    messagebox.showerror("Search Password", "Please enter the domain too", icon="error")
                else:
                    self.cur.execute("SELECT password FROM " + self.usern + " WHERE username = '" + self.username.get() + "' AND domain = '" + self.domain.get() + "'")
                    if self.cur.fetchone() is None:
                        messagebox.showerror("Search Password", "No password found", icon="error")
                    else:
                        if self.password.get() == self.passw:
                            messagebox.showinfo("Search Password", "Password found", icon="info")
                            self.edit_password(self.username.get(), self.domain.get())
                            self.search.destroy()
                        else:
                            messagebox.showerror("Search Password", "App password differs", icon="error")

    def search_password(self):
        self.search = Tk()
        self.search.title("Search Password")
        self.search.geometry("300x280")
        self.search.resizable(False, False)
        self.search.eval('tk::PlaceWindow . center')
        self.frame.withdraw()
        ttk.Label(self.search, text="SEARCH PASSWORD", padding=5).grid(row=0, column=1)
        ttk.Label(self.search, text="", padding=15).grid(row=0, column=2)
        Button(self.search, text="Back", width=5, command=self.search_back).grid(row=0, column=3)
        # Add username
        ttk.Label(self.search, text="*Username", padding=5).grid(row=1, column=1)
        self.username = ttk.Entry(self.search)
        self.username.focus()
        self.username.grid(row=1, column=2)
        # Add password
        ttk.Label(self.search, text="*App Password", padding=5).grid(row=2, column=1)
        self.password = ttk.Entry(self.search)
        self.password.config(show="*")
        self.password.grid(row=2, column=2)
        # domain
        ttk.Label(self.search, text="Domain", padding=5).grid(row=3, column=1)
        self.domain = ttk.Entry(self.search)
        self.domain.grid(row=3, column=2)
        ttk.Label(self.search, text="", padding=10).grid(row=4, column=1)
        ttk.Label(self.search, text="", padding=5).grid(row=5, column=1)
        Button(self.search, text="Search", width=8, command=lambda: self.show_all_password(self.username.get())).grid(row=5, column=1, columnspan=2)
        Button(self.search, text="Edit", width=8, command=lambda: self.search_msg("edit")).grid(row=5, column=2, columnspan=2)


    def del_password(self):
        self.deletex = Tk()
        self.deletex.title("Delete Password")
        self.deletex.geometry("300x280")
        self.deletex.resizable(False, False)
        self.deletex.eval('tk::PlaceWindow . center')
        self.frame.withdraw()
        ttk.Label(self.deletex, text="DELETE PASSWORD", padding=5).grid(row=0, column=1)
        ttk.Label(self.deletex, text="", padding=15).grid(row=0, column=2)
        Button(self.deletex, text="Back", width=5, command=self.delete_back).grid(row=0, column=3)
        # Add username
        ttk.Label(self.deletex, text="Username", padding=5).grid(row=1, column=1)
        self.username = ttk.Entry(self.deletex)
        self.username.focus()
        self.username.grid(row=1, column=2)
        main.connect_db(self)
        ttk.Label(self.deletex, text="Domain", padding=5).grid(row=4, column=1)
        self.domain = ttk.Entry(self.deletex)
        self.domain.grid(row=4, column=2)
        ttk.Label(self.deletex, text="", padding=4).grid(row=7, column=1)
        # add delete button
        Button(self.deletex, text="Delete", width=8, command=self.delete_password).grid(row=8, column=2, columnspan=2)



    def show_all_password(self, username):
        view = Tk()
        view.title("View Password")
        view.geometry("300x280")
        view.eval('tk::PlaceWindow . center')

        sheet = ttk.Treeview(view)
        sheet["columns"] = ("one", "two", "three")
        sheet.column("#0", width=0, stretch=NO)
        sheet.column("one", anchor=W, width=100)
        sheet.column("two", anchor=W, width=100)
        sheet.column("three", anchor=W, width=100)
        sheet.heading("#0", text="", anchor=W)
        sheet.heading("one", text="Username", anchor=W)
        sheet.heading("two", text="Password", anchor=W)
        sheet.heading("three", text="Domain", anchor=W)
        main.connect_db(self)
        self.cur.execute("SELECT * FROM " + self.usern + " WHERE username = '" + username + "'")
        rows = self.cur.fetchall()
        for row in rows:
            sheet.insert("", END, text="", values=(row[0], row[1], row[2]))
        sheet.pack(side=TOP, fill=X)
        Button(self.search, text="Edit", width=8, command=self.search_msg).grid(row=5, column=2, columnspan=2)

        view.mainloop()

