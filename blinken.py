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
        self.ser = serial.Serial( '/dev/ttyUSB0', '57600' )

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

        self.ser.write('\x23\x54\x26\x66')  # magic numbers
        self.ser.write('\x00\x08')          # height 8
        self.ser.write('\x00\x12')          # width 18
        self.ser.write('\x00\x01')          # channels 1
        self.ser.write('\x00\x07')          # maxval 7

        for row in range(8):
            for col in range(18):
                if self.message.lit(col, row):
                    self.ser.write('\x07')
                    if self.testing:
                        print "O",
                else:
                    self.ser.write('\x00')
                    if self.testing:
                        print " ",
            if self.testing:
                print

        if self.testing:
            print
            print

