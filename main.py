import os
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


if os.path.exists("prova3.txt"):
    f = open("prova3.txt", "a")
else:
    f = open("prova3.txt", "x")


class WelcomeScreen(QDialog):
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

    # def startscreen(self):
    #     create = StartScreen() 
    #     widget.addWidget(create)
    #     widget.setCurrentIndex(widget.currentIndex() + 1)

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
            conn = sqlite3.connect("shop_data.db")
            cur = conn.cursor()
            query = 'SELECT password FROM login_info WHERE username =\''+user+"\'"
            cur.execute(query)
            result_pass = cur.fetchone()[0]
            if result_pass == password:
                print("Successfully logged in.")
                # StartScreen = StartScreen()
                # widget.addWidget(StartScreen)
                # widget.setCurrentIndex(widget.currentIndex()+1)
                self.loadscreen()
                
                
                
                
                
            else:
                message = QMessageBox()
                message.setText("Invalid inputs.")
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
        self.logoutextbut.clicked.connect(self.stoptracking)
        self.startbutton.clicked.connect(self.on_clicked)
        
        
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_text)
        # self.timer.start(1000) 
        # with open('prova3.txt', 'r') as file:
        #     file_contents = file.read()

        # # Set the contents of the QTextEdit widget to the contents of the text file
        # self.TextEdit.setPlainText(file_contents)
        
        
        with open('prova3.txt', 'r') as file:
                self.timer = QTimer(self)
                self.timer.timeout.connect(self.update_text)
                self.timer.start(1000) 
                file_contents = file.read()

        # Set the contents of the QTextEdit widget to the contents of the text file
        
        self.TextEdit.setPlainText(file_contents)
       
        
    def db_insertion(self):
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
 
   
    
    def db_connections(self):
            self.mydb = mysql.connector.connect(
            host="localhost",
            user="trackeradmin",
            password="trackpass",
            database="trackerrose"
                    )
            self.mycursor = self.mydb.cursor()
            self.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.date = datetime.now().date()   
            print(self.date)
            print(self.start_time)
            
            self.key_pressed = list()
                    
            self.alphanumeric_key_count = 0
            self.special_key_count = 0
                        #########################    
            self.listener = keyboard.Listener(on_press=self.on_clicked, on_release=self.on_release)
                        
            self.listener.start()        
    
             
                
    
    def on_clicked( self ,key ):
        
            self.db_connections()
    
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
            
            
    def update_text(self):
        # Open the text file and read its contents
        with open('prova3.txt', 'r') as file:
            file_contents = file.read()

        # Set the contents of the QTextEdit widget to the contents of the text file
        
        self.TextEdit.setPlainText(file_contents)
        
    def stoptracking(self):
         self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
         self.db_insertion()
         exit()  
        
class CreateAccScreen(QDialog):
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        loadUi("createacc.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signupfunction)
        self.back.clicked.connect(self.goBack)

    def signupfunction(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()

        if len(user)==0 or len(password)==0 or len(confirmpassword)==0:
            self.error.setText("Please fill in all inputs.")

        elif password!=confirmpassword:
            self.error.setText("Passwords do not match.")
        else:
            conn = sqlite3.connect("shop_data.db")
            cur = conn.cursor()
            user_info = [user, password]
            cur.execute('INSERT INTO login_info (username, password) VALUES (?,?)', user_info)
            conn.commit()
            conn.close()
            fillprofile = FillProfileScreen()
            widget.addWidget(fillprofile)
            widget.setCurrentIndex(widget.currentIndex()+1)
            
    def goBack(self):
        create = WelcomeScreen() 
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class FillProfileScreen(QDialog):
    def __init__(self):
        super(FillProfileScreen, self).__init__()
        loadUi("fillprofile.ui",self)
        self.image.setPixmap(QPixmap('placeholder.png'))
        self.back.clicked.connect(self.goBack)
        self.continue_2.clicked.connect(self.login)

    def goBack(self):
        create = WelcomeScreen() 
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def login(self):
        LoginScreen()
    




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