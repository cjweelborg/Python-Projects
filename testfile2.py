# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 22:01:53 2017

@author: Christian
"""

import socket
import urllib2

socket.setdefaulttimeout(5)
s = socket.socket()
s.connect(("138.247.117.249",80))
#print(socket.gethostname())

sendData = bytearray()
sendData.append('dsu.edu')
s.send(sendData)

data = s.recv(1024)
s.close()



targetFile = open("testfile.txt", 'w')

targetFile.write(str(data))

targetFile.close()