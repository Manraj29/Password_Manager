from tkinter import *
from tkinter import ttk
import application
from tkinter import messagebox
import mysql.connector as mysql
import random
import string

class main():
    global usern
    global passw
    global username
    global password
    global confirmpassword
    global question
    global answer
    global frame
    global cur
    global conn
    global que_try
    que_try = 0


    def encrypt_password(self, password):
        password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(10)) + password + ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(10))
        return password


    def decrypt_password(self, password):
        password = password[10:-9]
        return password


    def reusern(self):
        return self.username.get()

    # Login window
    def __init__(self):
        self.frame = Tk()
        self.frame.title("Login")
        self.frame.geometry("250x250")
        self.frame.resizable(False, False)
        self.frame.eval('tk::PlaceWindow . center')

        ttk.Label(self.frame, text="Username", padding=15).grid(row=0)

        self.username = ttk.Entry(self.frame)
        self.username.focus()
        self.username.grid(row=0, column=1)

        ttk.Label(self.frame, text="Password", padding=15).grid(row=1)
        self.password = ttk.Entry(self.frame)
        self.password.config(show="*")
        self.password.grid(row=1, column=1)
        Button(text="Login", command=self.login).grid(row=2, column=1)
        ttk.Label(self.frame, text="", padding=15).grid(row=3)
        Button(self.frame, text="Forgot password?", command=self.forgot_pass).grid(row=3, column=1, columnspan=2)
        ttk.Label(self.frame, text="New user?", padding=15).grid(row=4)
        Button(self.frame, text="Register", command=self.registeration).grid(row=4, column=1)

        self.frame.mainloop()

    def login(self):
        usern = self.username.get()
        passw = self.password.get()
        self.connect_db()
        if usern == "" or passw == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            # get password from database and cut 10 randoms before and after password
            self.cur.execute("SELECT password FROM users WHERE name='" + usern + "'")
            row = self.cur.fetchone()
            if row == None:
                messagebox.showerror("Error", "Username or password is incorrect")
            else:
                if self.decrypt_password(row[0]) == passw:
                    messagebox.showinfo("Success", "Login successful")
                    self.frame.destroy()
                    application.application(usern, passw)
                else:
                    messagebox.showerror("Error", "Username or password is incorrect")




            # self.cur.execute("SELECT * FROM users WHERE name='" + usern + "' AND password='" + passw + "'")
            # row = self.cur.fetchone()
            # if row == None:
            #     messagebox.showerror("Error", "Username or password is incorrect")
            # else:
            #     messagebox.showinfo("Success", "Login successful")
            #     self.frame.destroy()
            #     application.application(usern, passw)

    def back_welcome(self):
        self.register.destroy()
        self.frame.deiconify()

    def check_password(self):
        if self.username.get() == "" or self.password.get() == "" or self.confirmpassword.get() == "" or self.question.get() == "" or self.answer.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            if self.password.get() == self.confirmpassword.get():
                if len(self.password.get()) < 8 or len(self.password.get()) > 20 or not any(
                        char.isdigit() for char in self.password.get()) or not any(
                    char.isupper() for char in self.password.get()) or not any(
                    char.islower() for char in self.password.get()):
                    messagebox.showerror("Error",
                                         "Password must be at least 8 characters\n less than 20 characters\n at least one number\n at least one uppercase letter\n at least one lowercase letter")
                else:
                    # ask continue or not
                    answer = messagebox.showinfo("confirmation", "Entered information is correct?", type="yesno")
                    if answer == "yes":
                        self.connect_db()
                        self.insert_data()
                        self.register.destroy()

                        messagebox.showinfo("Success", "Registration successful\nPlease retry application")
                        exit(0)
                    else:
                        messagebox.showinfo("Retry", "RETRY registration")
            else:
                messagebox.showerror("Error", "Password does not match")

    def registeration(self):
        self.register = Tk()
        self.register.title("Register")
        self.register.geometry("400x400")
        self.register.eval('tk::PlaceWindow . center')
        self.frame.withdraw()
        ttk.Label(self.register, text="Register", padding=15).grid(row=0, column=1)
        ttk.Label(self.register, text="Username", padding=15).grid(row=1, column=1)
        self.username = ttk.Entry(self.register)
        self.username.focus()
        self.username.grid(row=1, column=2)
        ttk.Label(self.register, text="Password", padding=15).grid(row=2, column=1)
        self.password = ttk.Entry(self.register)
        self.password.config(show="*")
        self.password.grid(row=2, column=2)
        ttk.Label(self.register, text="Confirm password", padding=15).grid(row=3, column=1)
        self.confirmpassword = ttk.Entry(self.register)
        self.confirmpassword.config(show="*")
        self.confirmpassword.grid(row=3, column=2)
        #         select question from combo box
        ttk.Label(self.register, text="Select question", padding=15).grid(row=4, column=1)
        self.question = ttk.Combobox(self.register,
                                     values=["What is the maiden name of your mother?", "What is the name of your pet?",
                                             "What is your favorite color?", "What is your favorite food?"], width=35)
        self.question.grid(row=4, column=2)
        self.question.current(0)
        self.question.config(state="readonly")
        ttk.Label(self.register, text="Answer", padding=15).grid(row=5, column=1)
        self.answer = ttk.Entry(self.register)
        self.answer.grid(row=5, column=2)
        #         register button
        Button(self.register, text="Register", command=self.check_password).grid(row=7, column=2)
        Button(self.register, text="Back", command=self.back_welcome).grid(row=7, column=1)

        self.register.mainloop()

    def connect_db(self):
        self.conn = mysql.connect(host="localhost", user="root", password="", database="passman")
        self.cur = self.conn.cursor()

    def insert_data(self):
        # check if username already exists
        self.cur.execute("SELECT * FROM users WHERE name='" + self.username.get() + "'")
        if self.cur.fetchone() is not None:
            messagebox.showerror("Error", "Username already exists")
            self.register.deiconify()
            self.register.mainloop()
        else:
            en_pass = self.encrypt_password(self.password.get())
            print(en_pass)
            self.cur.execute(
                "INSERT INTO users VALUES('" + self.username.get() + "','" + en_pass + "','" + self.question.get() + "','" + self.answer.get() + "')")
            self.conn.commit()
            self.cur.execute("CREATE TABLE " + self.username.get() + "(username VARCHAR(255), password text, domain VARCHAR(255))")


    def forgot_pass(self):
        self.frame.withdraw()
        self.forgot = Tk()
        self.forgot.title("Forgot password")
        self.forgot.geometry("400x400")
        self.forgot.eval('tk::PlaceWindow . center')
        ttk.Label(self.forgot, text="Forgot password", padding=15).grid(row=0, column=1)
        ttk.Label(self.forgot, text="Username", padding=15).grid(row=1, column=1)
        self.username = ttk.Entry(self.forgot)
        self.username.focus()
        self.username.grid(row=1, column=2)
        ttk.Label(self.forgot, text="Select question", padding=15).grid(row=2, column=1)
        self.question = ttk.Combobox(self.forgot,
                                     values=["What is the maiden name of your mother?", "What is the name of your pet?",
                                             "What is your favorite color?", "What is your favorite food?"], width=35)
        self.question.grid(row=2, column=2)
        self.question.current(0)
        self.question.config(state="readonly")
        ttk.Label(self.forgot, text="Answer", padding=15).grid(row=3, column=1)
        self.answer = ttk.Entry(self.forgot)
        self.answer.grid(row=3, column=2)
        Button(self.forgot, text="Submit", command=self.check_answer).grid(row=4, column=2)
        Button(self.forgot, text="Back", command=self.back_home).grid(row=4, column=1)
        self.forgot.mainloop()

    def check_answer(self):
        global que_try
        self.connect_db()
        self.cur.execute("SELECT * FROM users WHERE name='" + self.username.get() + "'")
        if self.cur.fetchone() is not None:
            self.cur.execute("SELECT * FROM users WHERE name='" + self.username.get() + "' AND select_que='" + self.question.get() + "' AND que_ans='" + self.answer.get() + "'")
            if self.cur.fetchone() is not None:
                self.cur.execute("SELECT password FROM users WHERE name='" + self.username.get() + "'")
                password = self.cur.fetchone()
                de_pass = self.decrypt_password(password[0])
                print(de_pass)
                messagebox.showinfo("Password", "Your password is " + de_pass)
                self.forgot.destroy()
                self.frame.deiconify()
            else:
                que_try += 1
                if que_try == 3:
                    messagebox.showerror("Error", "You have exceeded the number of tries")
                    self.forgot.destroy()
                    self.frame.deiconify()
                    exit(0)
                else:
                    messagebox.showerror("Error", "Wrong answer")
        else:
            messagebox.showerror("Error", "Username does not exist")

    def back_home(self):
        self.forgot.destroy()
        self.frame.deiconify()

# Main
if __name__ == "__main__":
    s = main()
