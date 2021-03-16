import socket
from _thread import *

SCR_WIDTH = 900
SCR_HEIGHT = 600
BG_COLOUR = (30, 30, 40)
PLAYER_COLOR = (154, 223, 252)

server_id = "192.168.1.7"
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_id, port))
server.listen(2)

print("Server started. Waiting for Connection...")

def readPos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3])

def makePos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])

pos = [(SCR_WIDTH-20, SCR_HEIGHT//2 - 40, 4, 4), (10, SCR_HEIGHT//2 - 40, 4, 4)]

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

            conn.sendall(str.encode(makePos(reply)))

        except:
            break

    print("Lost Connection")
    conn.close()

currentPlayer = 0
lst = []

while True:
    conn, addr = server.accept()
    print("Connected to: ", addr)
    lst.append(conn)

    if len(lst) > 1:
        conn_1 = lst[0]
        conn_2 = lst[1]
        start_new_thread(client_thread, (conn_1, currentPlayer))
        currentPlayer += 1
        start_new_thread(client_thread, (conn_2, currentPlayer))