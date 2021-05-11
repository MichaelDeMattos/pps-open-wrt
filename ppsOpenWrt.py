#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Michael M. Ortiz"
__copyright__ = ("Copyright 2021, The Cogent Project")
__credits__ = ["Michael M. Ortiz", "OpenWrt.org"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Michael M. Ortiz"
__email__ = "chelmto3000@gmail.com"
__status__ = "Production"

import os
import json
import time
import socket
import threading
from datetime import datetime

__all__ = ["Server"]

class Server(object):
    def __init__(self):
        """ Var for loop independent  """
        self.loop = True
         
        """ Servers Config """
        self.config = json.loads(
            open(os.path.sep+"usr"+os.path.sep+"local"+os.path.sep+"bin"+os.path.sep+"config.json", "rb").read()
        )
        
        """ File Log """
        self.log = open("log.txt", "wb")
        
        """ Port 1 """
        self.create_thread(
            host=self.config["host"],
            port=self.config["port0"],
            usb_port=self.config["p0addr"]
        )

    """ This function create thread for loop independent do websocket """
    def create_thread(self, host, port, usb_port):
        t = threading.Thread(target=self.printers_openWRT, args=[host, port, usb_port])
        t.daemon = True
        t.start()
    
    """ This function push data in usb_port """
    def printers_openWRT(self, host, port, usb_port):
        """ Max data recept in socket """
        data_payload = 2048

        """ Socket TCP """
        sock = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server = (host, port)
        sock.bind(server)
        sock.listen(5) 

        while True: 
            try:
                print("Server address: %s:%s" % server)
                client, address = sock.accept() 
                recept = client.recv(data_payload)

                command = "echo -e '%s' > %s" % (recept, usb_port)
                os.system(command)

                """ Response your client """
                client.send(200)

                """ Write log sucess """
                self.log.write("Print sucess! \t Date: %s" % datetime.now())

                if self.loop is None: break

            except Exception as error:
                print("Error: ", error)
                client.send(500)
                self.log.write("Error: %s Date: %s" % (str(error), datetime.now()))
                continue

if __name__ == ("__main__"):
    Server()