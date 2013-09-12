#!/usr/bin/env python

import sys
import string
from subprocess import call
import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        #Recv data
        print ("Client connected")
        self.data = self.request.recv(1024)
        print "DEBUG:1"
        data2 = string.split(self.data, "|")
        print ("DEBUG:2")
        print data2
        try:
            f = open('/tmp/festival_tmp','w')
            f.write(data2[1])
            f.close()
        except:
            print ("error writing temp file")

        if data2[0] =="mp4":
            call(["/usr/share/festival/bin/text2wave", "-o", "/tmp/festival_tmp.wav", "/tmp/festival_tmp"])
            call(["ffmpeg","-y","-i", "/tmp/festival_tmp.wav", "/tmp/festival_tmp."+data2[0]])
            call(["ffmpeg", "-i", "/tmp/festival_tmp."+data2[0], "copy", "-c:a", "libx264", "-vbr", "3","/tmp/festival_tmp_mp4.mp4"])
            call(["cp","/tmp/festival_tmp_mp4.mp4","/tmp/festival_tmp."+data2[0]])

        if data2[0] != "" or "mp4":
            call(["/usr/share/festival/bin/text2wave", "-o", "/tmp/festival_tmp.wav", "/tmp/festival_tmp"])
            call(["ffmpeg","-y","-i", "/tmp/festival_tmp.wav", "/tmp/festival_tmp."+data2[0]])

        try:
            #sends the converted file back to client
            sendfile = open("/tmp/festival_tmp."+data2[0])
            l = sendfile.read()
            self.request.sendall("SOF\n")
            self.request.sendall(l)
            self.request.sendall("\nEOF")
        except:
            print("error sending file")

        finally:
            self.request.close()
            print "Connection closed"
if __name__ == "__main__":
    try:
    #bind socet to port 
        HOST, PORT = "10.180.4.221", 5005
        server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
        server.serve_forever()
    except:
        print("Error binding socket")
        exit(1)

