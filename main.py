from network import Network
from classes import *
import random, socket, time, pygame, math, json


win_width = 800
win_height = 800
x = 100
y = 100
xv = 0
yv = 0
display = pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("Tank Game")
border = pygame.image.load("imgs\\border.png")
clock = pygame.time.Clock()
players = []
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
n = Network()
player_ID = int(n.getP())
player_index = player_ID
data = n.send("get")
players, index = data[0], data[1]
print("You are player",player_ID)
max_speed = 4
levels = [json.load(open("maps\level_1","r")),json.load(open("maps\level_2","r"))]

tiles = [pygame.image.load("tiles\dirt_1.png"),pygame.image.load("tiles\grass_1.png"),
         pygame.image.load("tiles\cross_junction.png"),pygame.image.load("tiles\dirt_border_square_bottom_left.png"),
         pygame.image.load("tiles\dirt_border_square_bottom_right.png"),pygame.image.load("tiles\dirt_border_circle_bottom_left.png"),
         pygame.image.load("tiles\dirt_border_circle_bottom_right.png"),pygame.image.load("tiles\dirt_border_circle_top_left.png"),
         pygame.image.load("tiles\dirt_border_circle_top_right.png"),pygame.image.load("tiles\dirt_border_square_down.png"),
         pygame.image.load("tiles\dirt_border_square_left.png"),pygame.image.load("tiles\dirt_border_square_right.png"),
         pygame.image.load("tiles\dirt_border_square_up.png"),pygame.image.load("tiles\dirt_border_square_top_left.png"),
         pygame.image.load("tiles\dirt_border_square_top_right.png"),pygame.image.load("tiles\grass_border_square_bottom_left.png"),
         pygame.image.load("tiles\grass_border_square_bottom_right.png"),pygame.image.load("tiles\grass_border_square_top_left.png"),
         pygame.image.load("tiles\grass_border_square_top_right.png"),pygame.image.load("tiles\grass_box.png"),
         pygame.image.load("tiles\l_junction_bottom_left.png"),pygame.image.load("tiles\l_junction_bottom_right.png"),
         pygame.image.load("tiles\l_junction_top_left.png"),pygame.image.load("tiles\l_junction_top_right.png"),
         pygame.image.load("tiles\\road_end_down.png"),pygame.image.load("tiles\\road_end_left.png"),
         pygame.image.load("tiles\\road_end_right.png"),pygame.image.load("tiles\\road_end_up.png"),
         pygame.image.load("tiles\\road_horizontal.png"),pygame.image.load("tiles\\road_to_dirt_down.png"),
         pygame.image.load("tiles\\road_to_dirt_left.png"),pygame.image.load("tiles\\road_to_dirt_right.png"),
         pygame.image.load("tiles\\road_to_dirt_up.png"),pygame.image.load("tiles\\road_turn_circle_bottom_left.png"),
         pygame.image.load("tiles\\road_turn_circle_bottom_right.png"),pygame.image.load("tiles\\road_turn_circle_top_left.png"),
         pygame.image.load("tiles\\road_turn_circle_top_right.png"),pygame.image.load("tiles\\road_turn_square_bottom_left.png"),
         pygame.image.load("tiles\\road_turn_square_bottom_right.png"),pygame.image.load("tiles\\road_turn_square_top_left.png"),
         pygame.image.load("tiles\\road_turn_square_top_right.png"),pygame.image.load("tiles\\road_vertical.png"),
         pygame.image.load("tiles\\t_junction_down.png"),pygame.image.load("tiles\\t_junction_left.png"),
         pygame.image.load("tiles\\t_junction_right.png"),pygame.image.load("tiles\\t_junction_up.png")]
obstacles_data = [True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,
                  False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,
                  False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,
                  False,False,False]


def get_centered_pos(pos, tank):
    pos = (pos[0]- tank.pos[0]+(win_width/2),pos[1] - tank.pos[1]+(win_height/2))
    return (int(pos[0]),int(pos[1]))

obstacle_maps = [json.load(open("maps\obstacle_map_1","r")),json.load(open("maps\obstacle_map_2","r"))]


tiles_indexes = []
level = levels[index]
obstacle_map = obstacle_maps[index]
for col in range(len(level)):
    tiles_indexes.append([])
    tiles_i = tiles_indexes[col]
    for row in range(len(level)):
        tiles_i.append(level[row][col])
        
obstacles = []
for col in range(len(obstacle_map)):
    for row in range(len(obstacle_map)):
        if obstacle_map[row][col] != 0 and obstacle_map[row][col] != 1 and obstacle_map[row][col] != 2:
            obstacles.append([(row*64,col*64),obstacle_map[row][col],obstacles_data[obstacle_map[row][col]-3]])

bg_img = pygame.Surface((1600,1600),pygame.SRCALPHA)
for col in range(len(tiles_indexes)):
    for row in range(len(tiles_indexes)):
        bg_img.blit(tiles[tiles_indexes[col][row]],((row)*64,(col)*64))

barriers = [Barrier((-100,-100),2,False)]
for obstacle in obstacles:
    barriers.append(Barrier(obstacle[0],obstacle[1],obstacle[2]))

slip = 0.5
frames = 0

def get_index(tanks, ID):
    for i in range(len(tanks)):
        if tanks[i].ID == ID:
            return i

run = True
players_len = 0
last_shot = time.time()
mouse_down = False
previous_pos = 0
while run:
    if len(players) != players_len:
        player_index = get_index(players, player_ID)
    display.blit(border,get_centered_pos((-400,-400),players[player_index]))
    display.blit(bg_img,get_centered_pos((0,0),players[player_index]))
    players = n.send(players[player_index])
    players_len = len(players)
    for player in players:
        if player.ID == player_ID:
            for barrier in barriers:
                while True:
                    try:
                        barrier.display_barrier(display, players[player_index])
                        break
                    except:
                        player_index = get_index(players, player_ID)
        for projectile in player.projectiles:
            projectile.print_projectile(display, players[player_index])
        player.display_tank(display, players[player_index])
        if player.ID == player_ID:
  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_down = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_down = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.xa = slip * -1
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.xa = slip
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        player.ya = slip * -1
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        player.ya = slip
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.xa = 0
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.xa = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        player.ya = 0
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        player.ya = 0

            
            player.direction = player.get_angle()
            player.xv += player.xa
            player.yv += player.ya
            if player.xv > max_speed and player.xa == slip:
                player.xv = max_speed
            if player.yv > max_speed and player.ya == slip:
                player.yv = max_speed
            if player.xv < max_speed * -1 and player.xa == slip * -1:
                player.xv = max_speed * -1
            if player.yv < max_speed * -1 and player.ya == slip * -1:
                player.yv = max_speed * -1
            if player.xv > 0 and player.xa == 0:
                player.xv -= slip
            if player.yv > 0 and player.ya == 0:
                player.yv -= slip
            if player.xv < 0 and player.xa == 0:
                player.xv += slip
            if player.yv < 0 and player.ya == 0:
                player.yv += slip
            for i in range(len(player.projectiles)):
                if player.projectiles[0].start_time + 120 <= frames:
                    del player.projectiles[0]

            if mouse_down:
                if last_shot + 0.2 < time.time():
                    player.projectiles.append(Projectile(player.ID,(player.pos[0],player.pos[1]),7,frames,display))
                    last_shot = time.time()

            
            if player.pos[0] >= 20 and player.pos[0] <= 1580 and player.pos[1] >= 20 and player.pos[1] <= 1580:
                player.pos = (int(player.pos[0] + (player.xv)),int(player.pos[1] + (player.yv)))
            else:
                player.xv = 0
                player.yv = 0
                player.xa = 0
                player.ya = 0
                if player.pos[0] <= 19:
                    player.pos = (20, player.pos[1])
                if player.pos[0] >= 1581:
                    player.pos = (1580, player.pos[1])
                if player.pos[1] <= 19:
                    player.pos = (player.pos[0],20)
                if player.pos[1] >= 1581:
                    player.pos = (player.pos[0],1580)

            collision, collision_pos  = player.check_collision(players, barriers)
            if collision == 1:
                if player.spawn_time + 5 < time.time():
                    player.health -= 10
                if player.health <= 0:
                    player.dead = True
            elif collision == 2:
                if player.spawn_time + 5 < time.time():
                    player.health -= 30
                player.pos = previous_pos
                player.xv = 0
                player.yv = 0                
                player.xa = 0
                player.ya = 0
                if player.health <= 0:
                    player.dead = True
            elif collision == 3:
                player.pos = previous_pos
                player.xv = 0
                player.yv = 0
                player.xa = 0
                player.ya = 0

            for i in range(len(player.projectiles)):
                collision = player.projectiles[i].check_collision(players, barriers)
                if collision:
                    del player.projectiles[i]
                    break
            for projectile in player.projectiles:
                projectile.pos = (projectile.pos[0] + projectile.velocity[0], projectile.pos[1] + projectile.velocity[1])

            previous_pos = player.pos
    pygame.display.update()
    frames += 1
    clock.tick(60)
