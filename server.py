import socket
from _thread import *
import sys

SCR_WIDTH = 900
SCR_HEIGHT = 600
BG_COLOUR = (30, 30, 40)
PLAYER_COLOR = (154, 223, 252)

server_id = "192.168.1.3"
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_id, port))
server.listen(2)

print("Server started. Waiting for Connection...")

def readPos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def makePos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = [(SCR_WIDTH-20, SCR_HEIGHT//2 - 40), (10, SCR_HEIGHT//2 - 40)]

def client_thread(conn, playerNo):
    conn.sendall(str.encode(makePos(pos[playerNo])))
    while True:
        try:
            data = readPos(conn.recv(2048).decode())
            pos[playerNo] = data

            if not data:
                print("Disconnected")
                break

            else:
                if playerNo == 1:
                    reply = pos[0]

                else:
                    reply = pos[1]
                    
                #print("Received: ", data)
                #print("Sending: ", reply)

            conn.sendall(str.encode(makePos(reply)))

        except:
            break

    print("Lost Connection")
    conn.close()

currentPlayer = 0

while True:
    conn, addr = server.accept()
    print("Connected to: ", addr)

    start_new_thread(client_thread, (conn, currentPlayer))
    currentPlayer += 1