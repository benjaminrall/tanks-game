from network import Network
from classes import *
import random, socket, time, pygame, math, json


win_width = 800
win_height = 800

display = pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("Tank Game")
border = pygame.image.load("imgs\\border.png")
clock = pygame.time.Clock()
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)
update_speed = 2
font = pygame.font.Font("imgs\clab.otf",25)

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
effect_icons = [pygame.image.load("imgs\speedboost.png"),pygame.image.load("imgs\damageboost.png"),pygame.image.load("imgs\defenceboost.png")]

def get_centered_pos(pos, tank):
    pos = (pos[0]- tank.pos[0]+(win_width/2),pos[1] - tank.pos[1]+(win_height/2))
    return (int(pos[0]),int(pos[1]))

obstacle_maps = [json.load(open("maps\obstacle_map_1","r")),json.load(open("maps\obstacle_map_2","r"))]

def get_index(tanks, ID):
    for i in range(len(tanks)):
        if tanks[i].ID == ID:
            return i

def display_message(text, pos, font, colour,display):
    surface = font.render(text,True,colour)
    display.blit(surface,pos)


in_menu = True
while in_menu:
    break

n = Network()
playing = True
while playing:
    slip = 0.5
    last_update = -1 - update_speed
    frames = 0      
    max_speed = 3
    x = 100
    y = 100
    xv = 0
    yv = 0
    players = []
    effects = []
    speed_timer_start = 0
    damage_timer_start = 0
    defence_timer_start = 0
    speed_powerup_active = False
    damage_powerup_active = False
    defence_powerup_active = False
    speed_duration = 10
    damage_duration = 10
    defence_duration = 10
    proj_damage = 10
    player_ID = int(n.getP())
    player_index = player_ID
    data = n.send("get")
    players, index = data[0], data[1]
    active_powerups = []
    print("You are player",player_ID)

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
        
    run = True
    players_len = 0
    last_shot = time.time()
    mouse_down = False
    previous_pos = (64,64)
    while run:
        if len(players) != players_len:
            player_index = get_index(players, player_ID)
        to_send = (players[player_index].pos,players[player_index].projectiles,
                   players[player_index].kills,players[player_index].deaths,
                   players[player_index].score,players[player_index].immune,
                   players[player_index].health,players[player_index].direction,
                   players[player_index].xv,players[player_index].yv,
                   players[player_index].xa,players[player_index].ya,
                   players[player_index].dead)
        if last_update + update_speed < frames:
            data = n.send(to_send)
            last_update = frames
        if data[0] == "go":
            run = False
            break
        players = data[0]
        powerup = data[1]
        if len(players) != players_len:
            player_index = get_index(players, player_ID)
        display.blit(border,get_centered_pos((-400,-400),players[player_index]))
        display.blit(bg_img,get_centered_pos((0,0),players[player_index]))
        if powerup[1] != 0:
            valid = True
            for active_powerup in active_powerups:
                if powerup[0] == active_powerup.pos:
                    valid = False
            if valid:
                active_powerups.append(Powerup(powerup[0],powerup[1]))
        for barrier in barriers:
            barrier.display_barrier(display, players[player_index])
        for powerup in active_powerups:
            powerup.display_powerup(display, players[player_index])
        players_len = len(players)
        for player in players:
            
            for projectile in player.projectiles:
                projectile.print_projectile(display, players[player_index])
            player.display_tank(display, players[player_index])
            for i in range(len(effects)):
                icon = effect_icons[effects[i] - 2]
                display.blit(pygame.transform.scale(icon,(40,40)),(10, i*45 + 10))
                    
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
                        player.projectiles.append(Projectile(player.ID,(player.pos[0],player.pos[1]),7,frames,display,proj_damage))
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

                collision, collision_data  = player.check_collision(players, barriers, active_powerups)
                if player.spawn_time + 5 < time.time():
                    player.immune = False
                if collision == 1:
                    if not player.immune:
                        player.health -= collision_data/player.defence
                        player.score -= 2
                    if player.health <= 0:
                        player.deaths += 1
                        player.score -= 15
                        player.dead = True
                elif collision == 2:
                    player.pos = previous_pos
                    player.xv = 0
                    player.yv = 0                
                    player.xa = 0
                    player.ya = 0
                elif collision == 3:
                    player.pos = previous_pos
                    player.xv = 0
                    player.yv = 0
                    player.xa = 0
                    player.ya = 0
                elif collision == 4:
                    if collision_data == 1:
                        if player.health <= 50:
                            player.health += 50
                        else:
                            player.health = 100
                    elif collision_data == 2:
                        speed_powerup_active = True
                        max_speed = 5
                        speed_timer_start = time.time()
                        if 2 not in effects:
                            effects.append(2)
                    elif collision_data == 3:
                        proj_damage = 20
                        damage_powerup_active = True
                        damage_timer_start = time.time()
                        if 3 not in effects:
                            effects.append(3)
                    elif collision_data == 4:
                        player.defence = 2
                        defence_powerup_active = True
                        defence_timer_start = time.time()
                        if 4 not in effects:
                            effects.append(4)
                
                if speed_powerup_active and speed_timer_start + speed_duration < time.time():
                    max_speed = 3
                    for i in range(len(effects)):
                        if effects[i] == 2:
                            del effects[i]
                            break

                if damage_powerup_active and damage_timer_start + damage_duration < time.time():
                    proj_damage = 10
                    for i in range(len(effects)):
                        if effects[i] == 3:
                            del effects[i]
                            break

                if defence_powerup_active and defence_timer_start + defence_duration < time.time():
                    player.defence = 1
                    for i in range(len(effects)):
                        if effects[i] == 4:
                            del effects[i]
                            break
                

                for i in range(len(player.projectiles)):
                    collision = player.projectiles[i].check_collision(players, barriers)
                    if collision:
                        del player.projectiles[i]
                        break
                for i in range(len(active_powerups)):
                    collision = active_powerups[i].check_collision(players)
                    if active_powerups[i].dead:
                        if active_powerups[i].dead_timer + 20 < time.time():
                            del active_powerups[i]
                            break
                for projectile in player.projectiles:
                    projectile.pos = (projectile.pos[0] + projectile.velocity[0], projectile.pos[1] + projectile.velocity[1])

                previous_pos = player.pos
        pygame.display.update()
        frames += 1
        clock.tick(60)

    can_continue = False
    reply = "0"
    end_menu = True
    while end_menu:
        
        scores = []
        for player in players:
            scores.append([player.score,player.ID,player.name,player.deaths,player.kills])
        scores = sorted(scores,reverse = True,key=lambda x:x[0])
        text = ("%-10s%-15s%-9s%-10s%-7s%-9s"%("RANK","NAME","KILLS","DEATHS","K/D","SCORE"))
        display_message(text, (75,100), font, white, display)
        for i in range(min(len(scores),5)):
            data = scores[i]
            if data[3] != 0:
                kd = str(round(data[4]/data[3],1))
            else:
                kd = str(data[4])
            display_message(str(i + 1), (77,i*40 + 140), font, white, display)
            display_message(data[2], (184,i*40 + 140), font, white, display)
            display_message(str(data[4]), (325,i*40 + 140), font, white, display)
            display_message(str(data[3]), (417,i*40 + 140), font, white, display)
            display_message(kd, (546,i*40 + 140), font, white, display)
            display_message(str(data[0]), (617,i*40 + 140), font, white, display)

        text = "YOU:"
        display_message(text,(77,340),font,white,display)
        
        for i in range(len(scores)):
            
            if scores[i][1] == player_ID:
                data = scores[i]
                if data[3] != 0:
                    kd = str(round(data[4]/data[3],1))
                else:
                    kd = str(data[4])
                display_message(str(i + 1), (77,380), font, white, display)
                display_message(data[2], (184,380), font, white, display)
                display_message(str(data[4]), (325,380), font, white, display)
                display_message(str(data[3]), (417,380), font, white, display)
                display_message(kd, (546, + 380), font, white, display)
                display_message(str(data[0]), (617,380), font, white, display)

        quit_button = pygame.draw.rect(display,(255,0,0),(67,520,97,50))
        display_message("QUIT",(82,535),font,black,display)
        contine_button = pygame.draw.rect(display,(0,255,0),(535,520,165,50))
        display_message("CONTINUE",(547,535),font,black,display)

        reply = "0"
        if reply == "0":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    can_continue = n.send("q")
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[1] > 520 and mouse_pos[1] < 570:
                        if mouse_pos[0] > 67 and mouse_pos[0] < 164:
                            can_continue = n.send("q")
                            pygame.quit()
                            quit()
                        if mouse_pos[0] > 535 and mouse_pos[0] < 700:
                            reply = "c"
                
        can_continue = n.send(reply)
        
        pygame.display.update()
        clock.tick(60)
        if can_continue:
            break
