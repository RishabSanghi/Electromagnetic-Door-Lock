#!/usr/bin/env python3
import sys
import MySQLdb
from threading import Thread
import threading
import time
import RPi.GPIO as GPIO
import json
from random import randint
from evdev import InputDevice
from select import select
from twilio.rest import Client

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(13,GPIO.OUT)
GPIO.output(13,GPIO.HIGH)


try:
    # python 2
    import Tkinter as tk
    import ttk
except ImportError:
    # python 3
    import tkinter as tk
    from tkinter import ttk
    
class Fullscreen_Window:
    
    global dbHost
    global dbName
    global dbUser
    global dbPass
    
    dbHost = 'localhost'
    dbName = 'db_name'
    dbUser = 'pi_userame'
    dbPass = 'pi_pwd'
    
    def __init__(self):
        self.tk = tk.Tk()
        self.tk.title("Tag8 Door Lock")
        self.frame = tk.Frame(self.tk)
        self.frame.grid()
        self.tk.columnconfigure(0, weight=1)
        
        self.tk.attributes('-zoomed', True)
        self.tk.attributes('-fullscreen', True)
        self.state = True
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.config(cursor="none")
        
        self.show_idle()
        
        t = Thread(target=self.listen_rfid)
        t.daemon = True
        t.start()
        
    def show_idle(self):
        self.welcomeLabel = ttk.Label(self.tk, text="Please Present\nYour Token")
        self.welcomeLabel.config(font='size, 20', justify='center', anchor='center')
        self.welcomeLabel.grid(sticky=tk.W+tk.E, pady=210)
    
    def pin_entry_forget(self):
        self.validUser.grid_forget()
        self.photoLabel.grid_forget()
        self.enterPINlabel.grid_forget()
        count = 0
        while (count < 12):
            self.btn[count].grid_forget()
            count += 1
        
    def returnToIdle_fromPINentry(self):
        self.pin_entry_forget()
        self.show_idle()
        
    def returnToIdle_fromPINentered(self):
        self.PINresultLabel.grid_forget()
        self.show_idle()
        
    def returnToIdle_fromAccessGranted(self):
        GPIO.output(13,GPIO.HIGH)
        self.SMSresultLabel.grid_forget()
        self.show_idle()
    
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"
        
    def listen_rfid(self):
        rfid_presented = ""

        keys = "X^1234567890XXXXqwertzuiopXXXXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
        dev = InputDevice('/dev/input/event0')
        rfid_presented = ""

        while True:
            r,w,x = select([dev], [], [])
            for event in dev.read():
                if event.type==1 and event.value==1:
                    if event.code==28:
                        
                        dbConnection = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName)
                        cur = dbConnection.cursor(MySQLdb.cursors.DictCursor)
                        cur.execute("SELECT * FROM access_list WHERE rfid_code = '%s'" % (rfid_presented))
            
                        if cur.rowcount != 1:
                            self.welcomeLabel.config(text="ACCESS DENIED")
                                    #Log access attempt
                            cur.execute("INSERT INTO access_log SET rfid_presented_datetime = NOW()" )
                            dbConnection.commit()
                            time.sleep(3)
                            self.welcomeLabel.grid_forget()
                            self.show_idle()
                        else:
                            user_info = cur.fetchone()
                            self.welcomeLabel.grid_forget()
                            self.validUser = ttk.Label(self.tk, text="Welcome\n %s!" % (user_info['name']), font='size, 15', justify='center', anchor='center')
                            self.validUser.grid(columnspan=3, sticky=tk.W+tk.E)
                            GPIO.output(13,GPIO.LOW)
                            rfid_presented = ""
                            uname = user_info['name']
                            cur.execute("INSERT INTO access_log SET  user_name = '%s'    , rfid_presented_datetime = NOW()" % (uname))
                            dbConnection.commit()
                            dbConnection.close()
                            time.sleep(2)
                            self.validUser.grid_forget()
                            self.show_idle()
                            self.doorOpenTimeout = threading.Timer(1, self.returnToIdle_fromAccessGranted)
                            self.doorOpenTimeout.start()
                    else:
                        rfid_presented += keys[ event.code ]
if __name__ == '__main__':
        w = Fullscreen_Window()
        w.tk.mainloop()


