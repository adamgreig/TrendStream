# -*- coding: utf-8 -*-

import base64
import socket
import urllib
import urllib2
import Tkinter
import simplejson

# get auth data
username = raw_input("Twitter username: ")
password = raw_input("Twitter password: ")
auth_str = base64.b64encode(username + ":" + password)

# fetch twitter trends
trends_url = "http://search.twitter.com/trends.json"
f = urllib2.urlopen(trends_url)
json = simplejson.loads(f.read())
trends = []
for trend in json['trends']:
    trends.append(trend['name'])

# encode the trends as an http post request
post_data = urllib.urlencode([('track', ','.join(trends))])

# open the stream
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('stream.twitter.com', 80))
sock.send('POST /track.json HTTP/1.1\r\n')
sock.send('Authorization: Basic %s\r\n' % auth_str)
sock.send('User-Agent: Python-socket\r\n')
sock.send('Host: stream.twitter.com\r\n')
sock.send('Accept: */*\r\n')
sock.send('Content-Length: %s\r\n' % str(len(post_data)))
sock.send('Content-Type: application/x-www-form-urlencoded\r\n')
sock.send('\r\n')
sock.send(post_data)


root = Tkinter.Tk()
w = Tkinter.Label(root, text="Getting tweets...")
w.pack()

def update_tweet():
    global sock
    global w
    global root
    buf = sock.recv(4096)
    try:
        lines = buf.split('\r\n')
        j = simplejson.loads(lines[1])
        print j['user']['screen_name'] + ': ' + j['text']
        w['text'] = j['user']['screen_name'] + ': ' + j['text']
    except ValueError, TypeError:
        pass
    root.after(1, update_tweet)

root.after_idle(update_tweet)

root.mainloop()