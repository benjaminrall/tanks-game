import socket, pickle, time, pygame, random, json
from _thread import *
from classes import Tank

server = "9.174.30.43"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for a connection...")

spawnpoint_maps = [json.load(open("maps\obstacle_map_1","r"))]
connected = set()
startingpos = []
tanks = []
idCount = 0
index = random.randint(1,len(spawnpoint_maps)) - 1
spawnpoint_map = spawnpoint_maps[index]
for col in range(len(spawnpoint_map)):
    for row in range(len(spawnpoint_map)):
        if spawnpoint_map[row][col] == 1:
            startingpos.append((row*64,col*64))

def threaded_client(conn, p):
    global idCount, tanks, index
    conn.send(str.encode(str(p)))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(8192*4))
            if not data:
                break
            else:
                if data != "get":
                    tanks[p] = data
                    for i in range(len(tanks)):
                        if tanks[i].dead:
                            random.shuffle(startingpos)
                            tanks[i].pos = startingpos[i]
                            tanks[i].dead = False
                            tanks[i].health = 100
                            tanks[i].spawn_time=time.time()
                    reply = tanks
                else:
                    reply = (tanks, index)
                conn.sendall(pickle.dumps(reply))
        except:
            break
    try:
        tanks[p].quit = True
        for i in range(len(tanks[p].projectiles)):
            del tanks[p].projectiles[0]
        print((p + 1),"left")
    except:
        pass
    idCount -=1
    print("Lost connection")
    conn.close()

p = -1
print("new game")
while True:
    if len(tanks) < len(startingpos):
        p += 1
        conn, addr = s.accept()
        print("Connected to:",addr)
        tanks.append(Tank(p,startingpos[p]))
        idCount += 1
        start_new_thread(threaded_client, (conn, p))
