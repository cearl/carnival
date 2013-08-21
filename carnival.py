#!/usr/bin/env python

import sys
import string
from subprocess import call
import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        #Recv data
        self.data = self.request.recv(1024).strip()
        data2 = string.split(self.data, "|")
        try:
            f = open('/tmp/festival_tmp','w')
            f.write(data2[1])
            f.close()
        except: 
            print ("error writing temp file")
           
        if data2[0] == "ogg":
            call(["/usr/share/festival/bin/text2wave", "-o", "/tmp/festival_tmp.tmp", "/tmp/festival_tmp"])
            call(["sox", "/tmp/festival_tmp.tmp", "/tmp/festival_tmp."+data2[0]])
        if data2[0] == "":
            l = "mp3 is not supported\n"
            self.request.sendall(l)
            
        try: 
            #sends the converted file back to client
            sendfile = open("/tmp/festival_tmp."+data2[0])
            l = sendfile.read()
            self.request.sendall(l)
        except:
            print("error sending file")
        
if __name__ == "__main__":
    try:
    #bind socet to port
        HOST, PORT = "10.180.4.221", 5005
        server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
        server.serve_forever()
    except:
        print("Error binding socket")
        exit(1)

