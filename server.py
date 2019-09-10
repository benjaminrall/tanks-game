import socket, pickle, time, pygame, random
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

connected = set()
tanks = []
idCount = 0
tanks_map = pygame.image.load("maps\\tanks_map.png")
tanks_pa = pygame.PixelArray(tanks_map)
startingpos = []
for col in range(len(tanks_pa)):
    for row in range(len(tanks_pa)):
        if tanks_pa[row,col] == tanks_map.map_rgb((0, 0, 0)):
            startingpos.append(((row + 1)*40,(col + 1)*40))
random.shuffle(startingpos)

def threaded_client(conn, p):
    global idCount, tanks
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
                            tanks[i].pos = startingpos[i]
                            tanks[i].dead = False
                            tanks[i].health = 100
                            tanks[i].spawn_time=time.time()
                reply = tanks
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
if len(tanks) < len(startingpos):
    while True:
        p += 1
        conn, addr = s.accept()
        print("Connected to:",addr)
        tanks.append(Tank(p,startingpos[p]))
        idCount += 1
        start_new_thread(threaded_client, (conn, p))
