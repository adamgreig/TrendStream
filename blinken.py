# -*- coding: utf-8 -*-
# TrendStream
# Adam Greig, Dec 2009

import serial
import threading
import time

import font

class Character:
    def __init__(self, char):
        self.char = char
        charcode = ord(char) - 32
        if charcode < 0 or charcode > 94:
            charcode = 31
        self.data = font.font[charcode]

    def lit(self, x, y):
        if self.data[y][x]:
            return True
        else:
            return False

class Message:
    def __init__(self, message):
        self.chars = []
        for char in message:
            self.chars.append(Character(char))
        self.x = 18

    def lit(self, x, y):
        x -= self.x
        if x > 0:
            return self.chars[x / 5].lit(x % 5, y)
        else:
            return False

class Blinken:
    def __init__(self, twitter):
        self.message = Message("")
        self.sock_cond = threading.Condition()
        self.twitter = twitter

    def add_streaming_message(self, message):
        self.message = Message(message)

    def check_twitter(self):
        while not self.twitter.tweets.empty():
            tweet = self.twitter.tweets.get(False)
            text = " " + tweet['user']['screen_name'] + ':' + tweet['text'] + "   "
            self.add_streaming_message(text)

    def send_animation(self):
        self.message.x = 20
        for x in range(len(self.message.chars) * 5):
            self.send_animation_frame()
            time.sleep(0.1)
        self.check_twitter();

    def send_animation_frame(self):
        self.message.x -= 1
        print "23 54 26 66", #magic
        print "00 08", #height 8
        print "00 12", #width 18
        print "00 01", #channels 1
        print "00 01" #maxval 1

        for row in range(8):
            for col in range(18):
                if self.message.lit(col, row):
                    print "O",
                else:
                    print " ",
            print

        print
        print

