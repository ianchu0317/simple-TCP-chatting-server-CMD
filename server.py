#!/bin/env python3
import socket
import sys
import threading
import string
import random

# Server class
class Server:
    def __init__(self, address, port, connections):
        self.SERVER_ADDRESS = (address, port)
        self.SERVER_IP = address
        self.PORT_NO = port
        self.MAX_CONNECTIONS = connections
        self.ACTIVE_CLIENTS = dict() # ALL CLIENTS[ID] = [CLIENT SOCKET, CLIENT THREAD ID]
        self.MSG_BUFF = 1024
    
    # Start listening and accepting incoming connections
    def startServer(self):
        self.s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_sock.bind(self.SERVER_ADDRESS)
        self.s_sock.listen()
        print("Server listening on {}:{}...".format(self.SERVER_IP, self.PORT_NO))

        CONN = 0

        while CONN <= self.MAX_CONNECTIONS:
            c_sock, c_addr = self.s_sock.accept()
            currentClientID = self.giveUniqueID() # Give ID
            currentClientThread = threading.Thread(target=self.handleClient, args=(currentClientID,))
            self.ACTIVE_CLIENTS[currentClientID] = [c_sock, currentClientThread, c_addr]
            currentClientThread.start()
    
            CONN += 1
            print(f"ACTIVE MEMBERS: {CONN}")

        # join threads, wait for finish
        for c_id in self.ACTIVE_CLIENTS:
            self.ACTIVE_CLIENTS.get(c_id)[1].join()
        
        self.s_sock.close() # End server

        
    # Handle client connection by reciving incoming messages
    def handleClient(self, c_id):
        CONNECTED = True
        c_sock = self.ACTIVE_CLIENTS.get(c_id)[0]
        c_sock.send(bytes("You're now connected to the server !", "utf-8"))
        while CONNECTED:
            try:
                message = str(c_sock.recv(self.MSG_BUFF), "utf-8")
                if message != "quit":
                    self.broadcastMessage(c_id, message)
                else:
                    CONNECTED = False
            except:
                continue
        c_sock.close()
        del self.ACTIVE_CLIENTS[c_id]
        return


    # Broadcast the message for all client except the client who sended that msg
    def broadcastMessage(self, user_id, message):
        print(f"{user_id}: {message}")
        for c_id in self.ACTIVE_CLIENTS:
            if c_id != user_id:
                self.ACTIVE_CLIENT.get(c_id)[0].send(bytes(f"{message}", "utf-8"))

    # Get random user ID
    def giveUniqueID(self):
        return  "".join(random.choice(string.ascii_letters + string.digits) for x in range(5))

# Get user input for server information
def getServerInfo():
    if len(sys.argv) == 4:
        try: 
            address = sys.argv[1]
            port = int(sys.argv[2])
            connections = int(sys.argv[3])
            return address, port, connections
        except ValueError:
            print("[!] Invalid input !")
            print("Usage: server.py <IP> <PORT> <NUMBER OF CONNECTIONS>")
            sys.exit()
    else:
        print("[!] Invalid input !")
        print("Usage: server.py <IP> <PORT> <NUMBER OF CONNECTIONS>")
        sys.exit()

if __name__ == '__main__':
    address, port, connections = getServerInfo()
    my_server = Server(address, port, connections)
    my_server.startServer()