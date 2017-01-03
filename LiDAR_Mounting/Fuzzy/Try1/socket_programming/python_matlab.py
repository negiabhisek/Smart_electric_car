#!/usr/bin/env python

# Echo server program
import socket
import time
HOST = 'localhost' 
PORT = 50004
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print "waiting for response from client at port ",PORT
conn, addr = s.accept()
print 'Connected by', addr
print 'hello'
#time.sleep(5)
#while True:
print conn.recv(16)
conn.sendall("Hello\n")
conn.sendall("Hello\n")
conn.sendall("Hello\n")
conn.sendall("Hello\n")
print conn.recv(16)
     #print data
     #if not data: break
     #clientdata="hello client"
     #conn.sendall(clientdata)
conn.sendall("Hello")
     
conn.close()
