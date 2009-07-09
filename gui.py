# -*- coding: utf-8 -*-
# TrendStream GUI
# Adam Greig, July 2009

import Queue
import Tkinter

class StreamingMessage:
    def __init__(self, canvas, text_widget, initposx, initposy):
        self.canvas = canvas
        self.text = text_widget
        self.posx = initposx
        self.posy = initposy
    
    def update(self):
        self.canvas.coords(self.text, self.posx, self.posy)
    
    def move_down(self, distance=1):
        self.posy += distance
        self.update()

class GUI:
    def __init__(self, twitter):
        '''Create the root window, set its title and size it'''
        self.root = Tkinter.Tk()
        self.root.title("TrendStream Alpha")
        self.root.minsize(512, 768)
        self.root.resizable(0, 0)
        self.twitter = twitter
    
    def ask_auth(self):
        '''Display a frame asking for a username and password'''
        self.auth_frame = Tkinter.Frame(self.root)
        
        self.auth_label = Tkinter.Label(self.auth_frame,
            text="Please login with your Twitter account:")
        self.username_label = Tkinter.Label(self.auth_frame, text="Username:")
        self.username_entry = Tkinter.Entry(self.auth_frame)
        self.password_label = Tkinter.Label(self.auth_frame, text="Password:")
        self.password_entry = Tkinter.Entry(self.auth_frame, show="*")
        self.login_button = Tkinter.Button(self.auth_frame, text="Login",
            command=self.process_auth)
        
        self.auth_label.grid(row=0, column=0, columnspan=2, sticky=Tkinter.W)
        self.username_label.grid(row=1, column=0, sticky=Tkinter.W)
        self.username_entry.grid(row=1, column=1, sticky=Tkinter.W)
        self.password_label.grid(row=2, column=0, sticky=Tkinter.W)
        self.password_entry.grid(row=2, column=1, sticky=Tkinter.W)
        self.login_button.grid(row=3, columnspan=2, sticky=Tkinter.N)
        
        self.username_entry.bind('<Return>',
            lambda event: self.login_button.invoke())
        self.password_entry.bind('<Return>',
            lambda event: self.login_button.invoke())
        
        self.auth_frame.pack()
        self.username_entry.focus()
    
    def process_auth(self):
        '''Get the entered username and password and use them'''
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.auth_frame.destroy()
        
        self.twitter.sock_cond.acquire()
        self.twitter.open_socket(username, password)
        self.twitter.sock_cond.notify()
        self.twitter.sock_cond.release()
        
        trend_string = "Trending Topics: "
        for trend in self.twitter.trends:
            trend_string += "%s, " % trend
        trend_string = trend_string[:-2]
        
        self.setup_canvas(trend_string)
    
    def setup_canvas(self, title):
        '''Set up the canvas widgets'''
        self.canvas = Tkinter.Canvas(self.root, width=512, height=768,
            bg="black")
        self.canvas.pack()
        self.canvas_title = self.canvas.create_text(5, 5, text=title,
            width=500, fill="white", font=("Courier", 12, "bold"),
            anchor=Tkinter.NW)
        self.streaming_messages = []
        #self.root.after(100, self.move_stream_callback, 1)
        self.root.after(100, self.check_twitter)
    
    def add_streaming_message(self, message, posx=5):
        self.move_stream(60)
        text = self.canvas.create_text(5, 100, text=message, width=350,
            fill="green", font=("Courier", 10), anchor=Tkinter.NW)
        streaming_message = StreamingMessage(self.canvas, text, 5, 100)
        self.streaming_messages.append(streaming_message)
    
    def move_stream(self, amount=1):
        '''Move all stream messages down a pixel'''
        for message in self.streaming_messages:
            message.move_down(amount)
            if message.posy > 768:
                self.canvas.delete(message.text)
                self.streaming_messages.remove(message)
    
    def move_stream_callback(self, amount=1):
        self.move_stream(amount)
        self.root.after(100, self.move_stream_callback, amount)
    
    def check_twitter(self):
        while not self.twitter.tweets.empty():
            tweet = self.twitter.tweets.get(False)
            text = tweet['user']['screen_name'] + ': ' + tweet['text']
            self.add_streaming_message(text)
        self.root.after(100, self.check_twitter)
