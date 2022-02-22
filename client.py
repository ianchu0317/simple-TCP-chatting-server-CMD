from ctypes.wintypes import MSG
import threading
import socket
import sys
import curses


class Client:
    def __init__(self, address, port):
        self.SERVER_ADDRESS = (address, port)
        self.MSG_BUFF = 1024

    # Connect to server
    def connectServer(self):
        c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c_sock.connect(self.SERVER_ADDRESS)

        # Possible entry: server or user input, using threading for receive connections
        serverUpdate = threading.Thread(target=self.updateFromServer, args=(c_sock))
        serverUpdate.start()
        sys.exit()

    # Receive messages
    def updateFromServer(self, c_sock):
        CONNECTED = True
        while CONNECTED:
            try:
                message = str(c_sock.recv(self.MSG_BUFF), "utf-8")
                print(message)
            except:
                continue


    def exitServer(self):
        pass
# Get user input for server information
def getServerInfo():
    if len(sys.argv) == 3:
        try: 
            address = sys.argv[1]
            port = int(sys.argv[2])
            return address, port
        except ValueError:
            print("[!] Invalid input !")
            print("Usage: server.py <IP> <PORT>")
            sys.exit()

    else:
        print("[!] Invalid input !")
        print("Usage: server.py <IP> <PORT>")
        sys.exit()



if __name__ == '__main__':
    address, port = getServerInfo()
    my_client = Client(address, port)
    my_client.connectServer()