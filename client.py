from ctypes.wintypes import MSG
import socket
import sys

class Client:
    def __init__(self, address, port):
        self.SERVER_ADDRESS = (address, port)
        self.MSG_BUFF = 1024

    def connectServer(self):
        c_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c_sock.connect(self.SERVER_ADDRESS)

        CONNECTED = True
        while CONNECTED:
            message = str(c_sock.recv(self.MSG_BUFF), "utf-8")
            print(message)
            toSend = input("me: ")
            c_sock.send(bytes(toSend, "utf-8"))
            if toSend == "quit":
                CONNECTED = False
        c_sock.close()
        sys.exit()

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