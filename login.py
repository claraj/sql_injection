import sqlite3
import sys

from tkinter import *

__author__ = 'clara @ mctc'

database_filename = "itec_2865_sql_injection_demo.db"


# Represents the GUI window.
class LoginGUI(Frame):

    def __init__(self):

        # Create and add GUI components to the screen
        Frame.__init__(self)
        self.master.title("Login Screen")

        self.master.minsize(300, 200)
        self.pack()

        self._usernameLabel = Label(self, text="Enter username")
        self._usernameLabel.pack()

        self._usernameVar = StringVar()
        self._usernameEntry = Entry(self, textvariable=self._usernameVar, width=30)
        self._usernameEntry.pack()

        self._passwordLabel = Label(self, text="Enter password")
        self._passwordLabel.pack()

        self._passwordVar = StringVar()
        self._passwordEntry = Entry(self, textvariable=self._passwordVar, width=30)
        self._passwordEntry.pack()

        self._loginButton = Button(self, text="Login", command=self._login)
        self._loginButton.pack()

        self._resultVar = StringVar()
        self._resultLabel = Label(self, text=" \n ", textvariable=self._resultVar)
        self._resultLabel.pack()

        self._quitButton = Button(self, text="Quit", command=self._quit)
        self._quitButton.pack()

    def _auth(self, uname, password):

        # Authentication for a specified username and password.
        # Connect to the database, and select name from users where user = 'admin' and password = 'kittens'
        # Or whatever the user typed in. Unfortunately, there is no validation so anything the user
        # enters will be send directly to the database with NO validation.

        print('Attempting to login user with username: %s \npassword: %s' % (uname, password))

        db = sqlite3.connect(database_filename)
        db.row_factory = sqlite3.Row  # Row factory allows us to refer to columns by name (default is by integer index)
        cursor = db.cursor()

        # Execute the SQL statement we created
        cursor.execute('SELECT name FROM users WHERE username = ? and password = ?', (uname, password))

        result = None  # Assume login fails, unless DB returns a row for this user

        # This loop won't run if no results are returned.
        for row in cursor:
            result = row['name']  # Extract name from first row
            break

        db.close()

        return result


    def _quit(self):

        exit(0)


    def _login(self):
        username = self._usernameVar.get()
        password = self._passwordVar.get()
        result = self._auth(username, password)

        if result is None:
            display_result = "Username or password incorrect"
        else:
            display_result = "Welcome, " + result

        self._resultVar.set(display_result)


def setup_database():

    db = sqlite3.connect(database_filename)
    cursor = db.cursor()

    # Delete any existing data
    cursor.execute('DROP TABLE IF EXISTS users')

    db.commit()

    # Create a database table with columns for user's name (name), user id (user),  and password (password)
    cursor.execute('CREATE TABLE users (username text, name text, password text) ')

    # Add some sample data. Note that the admin is the first entry in the table, as is often the case
    cursor.execute('''INSERT INTO users VALUES ( 'admin', 'Abby Admin', 'kittens') ''')
    cursor.execute('''INSERT INTO users VALUES ( 'bill', 'Bill S Preston', 'excellent!') ''')
    cursor.execute('''INSERT INTO users VALUES ( 'bart', 'Bart Simpson', 'eatmyshorts') ''')
    cursor.execute('''INSERT INTO users VALUES ( 'miley', 'Miley Cyrus', 'top40' ) ''')

    # commit saves changes
    db.commit()

    # and then close the connection to the database.
    db.close()


def start_gui():

    LoginGUI().mainloop()


def quit():

    sys.exit()


def main():
    setup_database()
    start_gui()


if __name__ == '__main__':
    main()



