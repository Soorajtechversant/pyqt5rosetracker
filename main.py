import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
import time
from PyQt5.QtCore import QTime
from PyQt5.QtCore import QTimer, QDateTime
import sys
from PyQt5.QtCore import QTimer
from pynput import keyboard
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import sqlite3
import mysql.connector
from datetime import datetime
from PyQt5.QtCore import QThread, pyqtSignal

if os.path.exists("tracker.txt"):
    f = open("tracker.txt", "a")
else:
    f = open("tracker.txt", "x")
class WelcomeScreen(QDialog):
    close_window_signal = pyqtSignal()
    
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen.ui",self)
        self.login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotocreate)
        self.exit.clicked.connect(exit)
            
    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocreate(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def goBack(self):
        create = WelcomeScreen() 
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)
class LoginScreen(QDialog):
      
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)
        self.back.clicked.connect(self.goBack)
       
        
    def loginfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()

        if len(user)==0 or len(password)==0:
            message = QMessageBox()
            message.setText("Please fill in all inputs.")
            message.exec_()
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="trackeradmin",
                password="trackpass",
                database="trackerrose",
            )

            cur = conn.cursor()
            query = 'SELECT password FROM UserDetails WHERE username =\''+user+"\'"
            cur.execute(query)
            
            result = cur.fetchone()
            if result is not None:
                result_pass = result[0]
                if result_pass == password:
                    print("Successfully logged in.")
                    self.loadscreen()
                else:
                    print('error')
                    message = QMessageBox()
                    message.setText("Invalid inputs.")
                    message.exec_()
            else:
                print('error')
                message = QMessageBox()
                message.setText("Invalid username.")
                message.exec_()
            
    def loadscreen(self):
            create = TrackingScreen() 
            widget.addWidget(create)
            widget.setCurrentIndex(widget.currentIndex() + 1)         
                
    def goBack(self):
            create = WelcomeScreen() 
            widget.addWidget(create)
            widget.setCurrentIndex(widget.currentIndex() + 1)   
class TrackingScreen(QDialog):
    def __init__(self):
        super(TrackingScreen, self).__init__()
        loadUi("tracking.ui",self)
        self.stop_tracker.clicked.connect(self.stoptracking)
        self.startbutton.clicked.connect(self.on_clicked)
        self.profilebut.clicked.connect(self.profile)
        self.refresh_button.clicked.connect(self.refresh)
        self.logout_ext_but.clicked.connect(exit)       
        self.recent_button.clicked.connect(self.recent)

        #current time
        self.set_time.setText("")
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000) # Update every second
        
        #current date
        self.set_date.setText("")
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_date)
        self.timer.start()
    




            

            
            
        
        #mysql db connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="trackeradmin",
            password="trackpass",
            database="trackerrose",
        )
        
        cur = self.conn.cursor()
        cur.execute("SELECT username FROM UserDetails WHERE id = 1")
        row = cur.fetchone()
        username = row[0] if row else ""
        self.loggedinas.setText(username)
                
        cur = self.conn.cursor()
        cur.execute("SELECT start_time FROM TrackerSummary WHERE tracker_id = 1")
        row = cur.fetchone()
        
        
        start_time = row[0] if row else None
        if start_time:
            start_time_str = start_time.strftime('%H:%M:%S') # Convert datetime object to string
            self.login_time.setText(start_time_str) # Set text of the login_time widget to the formatted string
        else:
            self.login_time.setText("") # Set text of the login_time widget to an empty string
                
        with open('tracker.txt', 'r') as file:
                # self.timer = QTimer(self)
                # self.timer.timeout.connect(self.update_text)
                # self.timer.start(1000) 
                file_contents = file.read()

        # Set the contents of the QTextEdit widget to the contents of the text file
        self.TextEdit.setPlainText(file_contents)


    
    def update_time(self):
            # Get the current time and format it as desired
            current_time = datetime.now().strftime('%I:%M:%S %p')
            self.set_time.setText(current_time)

    def update_date(self):
            # Get the current time and format it as desired
            current_date = datetime.now().strftime('%d-%m-%Y')
            self.set_date.setText(current_date)
     
    def refresh(self):   
        self.update_text() 

    def db_connections(self):
            self.mydb = mysql.connector.connect(
            host="localhost",
            user="trackeradmin",
            password="trackpass",
            database="trackerrose"
                    )
            self.mycursor = self.mydb.cursor()
            # self.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # self.date = datetime.now().date()   
            # print(self.date)
            # print(self.start_time)
            
            # self.key_pressed = list()
                    
            # self.alphanumeric_key_count = 0
            # self.special_key_count = 0
            #             #########################    
            # self.listener = keyboard.Listener(on_press=self.on_clicked, on_release=self.on_release)
                        
            # self.listener.start()  
                
    def db_insertion(self):
        
            self.mydb = mysql.connector.connect(
            host="localhost",
            user="trackeradmin",
            password="trackpass",
            database="trackerrose"
                    )
            self.mycursor = self.mydb.cursor()
            
            sql = """INSERT INTO TrackerSummary (date, start_time, end_time, total_alphanumeric_keys, total_special_keys) VALUES (%s,%s,%s,%s,%s)"""
            self.mycursor.execute(sql, (self.date, self.start_time, self.end_time, self.alphanumeric_key_count,self.special_key_count))
            self.mydb.commit()
            summery_id = self.mycursor.lastrowid
            details_row = list()
            for keys in self.key_pressed:
                details_row.append((keys, summery_id))

            sql = """INSERT INTO TrackerDetails (Keys_pressed, summary_id) VALUES (%s,%s)"""

            self.mycursor.executemany(sql, (details_row))
            self.mydb.commit()
            self.mydb.close()   

    def on_clicked( self ,key ):
        
            # finished = pyqtSignal()
            self.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.date = datetime.now().date()   
            print(self.date)
            print(self.start_time)
            
            self.key_pressed = list()
                    
            self.alphanumeric_key_count = 0
            self.special_key_count = 0
            self.listener = keyboard.Listener(on_press=self.on_clicked, on_release=self.on_release)
            self.listener.start()        
    
    
            try:
                text = ("-key [ {0} ] pressed --".format(
                        key.char))
                f.writelines(text)
                self.alphanumeric_key_count += 1
                    
            except AttributeError:
                text = ("special key {0} pressed".format(
                        key))
                f.writelines(text)
                self.special_key_count += 1
                
                f.flush()
            self.key_pressed.append(text) 
            
    def on_release( self, key ):
        
       
            text = ("key [ {0} ] released ".format(
                key))
            f.writelines(f'{text} \n')
            f.flush()
            self.key_pressed.append(text)       
                                   
    def stoptracking(self):
        #  self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #  self.db_insertion()
        #  self.tracking = TrackingScreen()
        #  self.tracking.terminate()
        #  self.close()
        #  exit()  

        self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db_insertion()
     
    def profile(self):
        ui = Profile() 
        widget.addWidget(ui)
        widget.setCurrentIndex(widget.currentIndex() + 1)
            
    def update_text(self):
        # Open the text file and read its contents
        with open('tracker.txt', 'r') as file:
            file_contents = file.read()

        # Set the contents of the QTextEdit widget to the contents of the text file
        
        self.TextEdit.setPlainText(file_contents)
    
    def recent(self):
        ui = Recent() 
        widget.addWidget(ui)
        widget.setCurrentIndex(widget.currentIndex() + 1)       

    def time(self):    
        
        time_edit = QTimeEdit()

        # Set the time to the current time
        current_time = QTime.currentTime()
        time_edit.setTime(current_time)

        # Show the widget
        time_edit.show()  

 
class Profile(QDialog):
    def __init__(self):
        super(Profile, self).__init__()
        loadUi("showprofile.ui", self)
        self.savebut.clicked.connect(lambda: self.save())
        self.backbut.clicked.connect(self.goBack)

        self.conn = mysql.connector.connect(
            host="localhost",
            user="trackeradmin",
            password="trackpass",
            database="trackerrose",
        )

        cur = self.conn.cursor()
        cur.execute("SELECT username FROM UserDetails WHERE id = 1")
        row = cur.fetchone()
        username = row[0] if row else ""

        cur = self.conn.cursor()
        cur.execute("SELECT email FROM UserDetails WHERE id = 1")
        row = cur.fetchone()
        email = row[0] if row else ""

        cur = self.conn.cursor()
        cur.execute("SELECT phone FROM UserDetails WHERE id = 1")
        row = cur.fetchone()

        phone = row[0] if row else ""

        self.nameedit.setText(username)
        self.emailedit.setText(email)
        self.mobedit.setText(str(phone))

    def save(self):
        # Retrieve user's information from the input fields
        username = self.nameedit.text()
        email = self.emailedit.text()
        phone = self.mobedit.text()

        # Establish a connection to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="trackeradmin",
            password="trackpass",
            database="trackerrose",
        )

        # Define an SQL query to update the user's information in the database
        query = "UPDATE UserDetails SET username = %s, email = %s, phone = %s WHERE id = 1"

        # Prepare the query with the values retrieved from the input fields
        values = (username, email, phone)
        cursor = mydb.cursor()
        cursor.execute(query, values)

        # Commit the changes to the database
        mydb.commit()

        # Close the database connection
        cursor.close()
        mydb.close()

        # Clear the input fields
        self.nameedit.setText(username)
        self.emailedit.setText(email)
        self.mobedit.setText(str(phone))

        # Show a message box to confirm that the data was saved
        QtWidgets.QMessageBox.information(self, "Success", "Kindly Login again ")
        
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def goBack(self):
        create = TrackingScreen() 
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)   
        
class CreateAccScreen(QDialog):
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        loadUi("createacc.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signupfunction)
        self.back.clicked.connect(self.goBack)

    def signupfunction(self):
        username = self.username.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()
        email = self.email.text()
        phone = self.phone.text()

        if len(username)==0 or len(password)==0 or len(confirmpassword)==0 or len(email)==0 or len(phone)==0:
            self.error.setText("Please fill in all inputs.")

        elif password!=confirmpassword:
            self.error.setText("Passwords do not match.")
        else:
            
            conn = mysql.connector.connect(
                host="localhost",
                user="trackeradmin",
                password="trackpass",
                database="trackerrose",
            )

            cur = conn.cursor()
            user_info = [username, password , email , phone ]
            cur.execute('INSERT INTO UserDetails (username, password , email , phone ) VALUES (%s, %s, %s , %s )', user_info)
            conn.commit()
            conn.close()

            message = QMessageBox()
            message.setText("Created Successfully Kindly log in")
            message.exec_()   
            
            login = LoginScreen()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
    
                    
    def goBack(self):
        create = WelcomeScreen() 
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Recent(QDialog):
    

    def __init__(self):
        super(Recent, self).__init__()
        loadUi("recent.ui",self)
        
        with open('tracker.txt', 'r') as file:
            file_contents = file.read()

    # Set the contents of the QTextEdit widget to the contents of the text file
        
        self.recent_keys.setPlainText(file_contents)       

        self.back_button.clicked.connect(self.goBack)
        # self.recent_keys.setText(self.recent_text_tracked())

    def goBack(self):
        create = TrackingScreen() 
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)    
        

 # Open the text file and read its contents


# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_()) 
except:
    print("Exiting")