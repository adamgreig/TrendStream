# -*- coding: utf-8 -*-
# TrendStream Twitter Interface
# Adam Greig, July 2009

import Queue
import base64
import socket
import urllib
import urllib2
import threading
import simplejson

class Twitter:
    def __init__(self):
        self.tweets = Queue.Queue()
        self.sock_cond = threading.Condition()
    
    def get_trends(self):
        '''Fetch the current trends from Twitter'''
        try:
            f = urllib2.urlopen("http://search.twitter.com/trends.json")
            json = simplejson.loads(f.read())
        except (ValueError, urllib2.URLError, TypeError):
            print "Error getting current Twitter trends, retrying..."
            self.get_trends()
        else:
            self.trends = []
            for trend in json['trends']:
                self.trends.append(trend['name'])
    
    def open_socket(self, username, password):
        '''Open a streaming socket to Twitter'''
        trends_string = ','.join(self.trends).encode('utf-8')
        post_data = urllib.urlencode([('track', trends_string)])
        auth_str = base64.b64encode(username + ":" + password)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('stream.twitter.com', 80))
        self.sock.send('POST /track.json HTTP/1.1\r\n')
        self.sock.send('Authorization: Basic %s\r\n' % auth_str)
        self.sock.send('User-Agent: TrendStream Alpha\r\n')
        self.sock.send('Host: stream.twitter.com\r\n')
        self.sock.send('Accept: */*\r\n')
        self.sock.send('Content-Length: %s\r\n' % str(len(post_data)))
        self.sock.send('Content-Type: application/x-www-form-urlencoded\r\n')
        self.sock.send('\r\n')
        self.sock.send(post_data)
    
    def get_tweets(self):
        try:
            buf = self.sock.recv(4096)
        except socket.error:
            pass
        
        if not buf:
            return
        
        lines = buf.split('\r\n')
        for line in lines:
            try:
                j = simplejson.loads(line)
            except ValueError:
                continue
            
            try:
                tweet = {
                    'text': j['text'],
                    'date': j['created_at'],
                    'id': j['id'],
                    'user': {
                                'screen_name': j['user']['screen_name'],
                                'id': j['user']['id'],
                                'location': j['user']['location']
                            }
                }
            except TypeError, KeyError:
                continue
            
            self.tweets.put(tweet)
