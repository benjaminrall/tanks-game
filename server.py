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
powerups = []
tanks = []
idCount = 0
index = random.randint(1,len(spawnpoint_maps)) - 1
tank_map = spawnpoint_maps[index]
powerup_map = spawnpoint_maps[index]
for col in range(len(tank_map)):
    for row in range(len(tank_map)):
        if tank_map[row][col] == 1:
            startingpos.append((row*64 + 32,col*64 + 32))
for col in range(len(powerup_map)):
    for row in range(len(powerup_map)):
        if powerup_map[row][col] == 2:
            powerup_spawns.append([(row*64 + 22,col*64 + 22), 0])

def get_index(tanks, ID):
    for i in range(len(tanks)):
        if tanks[i].ID == ID:
            return i

def threaded_client(conn, p_ID):
    global idCount, tanks, index
    conn.send(str.encode(str(p_ID)))
    p_i = get_index(tanks, p_ID)
    tanks_len = len(tanks)
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(8192*4))
            if not data:
                break
            else:
                if data == "powerup":
                    reply = powerups
                elif data != "get":
                    if len(tanks) != tanks_len:
                        p_i = get_index(tanks, p_ID)
                    tanks_len = len(tanks)
                    tanks[p_i] = data
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
        tanks[p_i].quit = True
        for i in range(len(tanks[p_i].projectiles)):
            del tanks[p_i].projectiles[0]
        del tanks[p_i]
        print("player",p_ID,"left")
    except:
        pass
    idCount -=1
    print("Lost connection")
    conn.close()

p_ID = -1
print("new game")
while True:
    if len(tanks) < len(startingpos):
        p_ID += 1
        conn, addr = s.accept()
        print("Connected to:",addr)
        random.shuffle(startingpos)
        tanks.append(Tank(p_ID,startingpos[0]))
        idCount += 1
        start_new_thread(threaded_client, (conn, p_ID))
