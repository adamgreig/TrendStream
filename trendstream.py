# -*- coding: utf-8 -*-
# TrendStream
# Adam Greig, July 2009

import sys
import Queue
import threading

import gui
import twitter

class GUIThread(threading.Thread):
    def __init__(self, twitter):
        self.twitter = twitter
        threading.Thread.__init__(self)
    
    def run(self):
        self.gui = gui.GUI(self.twitter)
        self.gui.ask_auth()
        self.gui.root.mainloop()

class TwitterThread(threading.Thread):
    def __init__(self, twitter):
        self.twitter = twitter
        threading.Thread.__init__(self)
    
    def run(self):
        self.twitter.sock_cond.acquire()
        twitter.sock_cond.wait()
        self.twitter.sock_cond.release()
        while 1:
            self.twitter.get_tweets()

if __name__ == '__main__':
    twitter = twitter.Twitter()
    twitter.get_trends()
    
    twitter_thread = TwitterThread(twitter)
    gui_thread = GUIThread(twitter)
    
    twitter_thread.start()
    gui_thread.start()
    
    gui_thread.join()
    
    sys.exit()