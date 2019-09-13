import socket, pickle, time, pygame, random, json
from _thread import *
from classes import Tank

server = "9.174.20.107"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for a connection...")

def reset_values():
    global index, spawn_timer, next_index, spawnpoint_maps, powerup, startingpos, powerup_spawns, game_timer
    powerup_spawns = []
    startingpos = []
    powerup = [(0,0),0]
    game_timer = time.time()
    spawn_timer = time.time()
    if index != next_index:
        index = next_index
    if index >= len(spawnpoint_maps):
        index = 0
    tank_map = spawnpoint_maps[index]
    powerup_map = spawnpoint_maps[index]
    for col in range(len(tank_map)):
        for row in range(len(tank_map)):
            if tank_map[row][col] == 1:
                startingpos.append((row*64 + 32,col*64 + 32))
    for col in range(len(powerup_map)):
        for row in range(len(powerup_map)):
            if powerup_map[row][col] == 2:
                powerup_spawns.append((row*64 + 22,col*64 + 22))

next_index = 0
index = -1
spawnpoint_maps = [json.load(open("maps\obstacle_map_1","r")),json.load(open("maps\obstacle_map_2","r"))]
reset_values()
connected = set()
powerup = [(0,0),0]
IDs = [1,2,3,4]
random.shuffle(IDs)
tanks = []
game_duration = 1

def get_index(tanks, ID):
    for i in range(len(tanks)):
        if tanks[i].ID == ID:
            return i

def threaded_client(conn, p_ID):
    global tanks, index, spawn_timer, powerup, next_index, game_duration, startingpos, powerup_spawns, IDs, game_timer
    conn.send(str.encode(str(p_ID)))
    p_i = get_index(tanks, p_ID)
    reply = ""
    tanks_len = len(tanks)
    playing = True
    game_timer = time.time()
    while playing:
        run = True
        while run:
            try:
                if game_timer + game_duration >= time.time():
                    data = pickle.loads(conn.recv(8192*4))
                    if not data:
                        break
                    else:
                        if data != "get":
                            if (spawn_timer + 20) < time.time():
                                random.shuffle(powerup_spawns)
                                random.shuffle(IDs)
                                powerup = [powerup_spawns[0],IDs[0]]
                                spawn_timer = time.time()
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
                                    tanks[i].immune = True
                            reply = (tanks, powerup)
                        else:
                            reply = (tanks, index)
                        conn.sendall(pickle.dumps(reply))
                else:
                    next_index = index + 1
                    run = False
            except:
                run = True
                break            
        if run:
            try:
                tanks[p_i].quit = True
                for i in range(len(tanks[p_i].projectiles)):
                    del tanks[p_i].projectiles[0]
                del tanks[p_i]
                print("player",p_ID,"left")
            except:
                pass
            print("Lost connection")
            conn.close()
            return
        data = pickle.loads(conn.recv(8192*4))
        reply = ("go",0)
        conn.sendall(pickle.dumps(reply))
        p_i = get_index(tanks, p_ID)
        reset_values()
        for i in range(len(tanks)):
            random.shuffle(startingpos)
            tanks[i].pos = startingpos[i]
            tanks[i].dead = False
            tanks[i].health = 100
            tanks[i].spawn_time=time.time()
            tanks[i].immune = True

p_ID = -1
print("new game")
while True:
    if len(tanks) < len(startingpos):
        p_ID += 1
        conn, addr = s.accept()
        print("Connected to:",addr)
        random.shuffle(startingpos)
        tanks.append(Tank(p_ID,startingpos[0]))
        start_new_thread(threaded_client, (conn, p_ID))
