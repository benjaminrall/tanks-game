import socket, time, random, pygame, math
pygame.init()

IMAGES = [pygame.image.load("imgs\\turret.png"),pygame.image.load("imgs\\bullet.png"),
          pygame.image.load("imgs\gun.png"),pygame.image.load("obstacles\\boulder_1.png"),
          pygame.image.load("obstacles\\boulder_2.png"),pygame.image.load("obstacles\stonewall_end_down.png"),
          pygame.image.load("obstacles\stonewall_end_up.png"),pygame.image.load("obstacles\stonewall_end_left.png"),
          pygame.image.load("obstacles\stonewall_end_right.png"),pygame.image.load("obstacles\stonewall_turn_bottom_left.png"),
          pygame.image.load("obstacles\stonewall_turn_bottom_right.png"),pygame.image.load("obstacles\stonewall_turn_top_left.png"),
          pygame.image.load("obstacles\stonewall_turn_top_right.png"),pygame.image.load("obstacles\stonewall_vertical.png"),
          pygame.image.load("obstacles\stonewall_horizontal.png"),pygame.image.load("obstacles\stonewall_vertical_door.png"),
          pygame.image.load("obstacles\stonewall_horizontal_door.png"),pygame.image.load("obstacles\\tree_1.png"),
          pygame.image.load("obstacles\water.png"),pygame.image.load("obstacles\water_box.png"),
          pygame.image.load("obstacles\water_down.png"),pygame.image.load("obstacles\water_up.png"),
          pygame.image.load("obstacles\water_left.png"),pygame.image.load("obstacles\water_right.png"),
          pygame.image.load("obstacles\water_open_down.png"),pygame.image.load("obstacles\water_open_up.png"),
          pygame.image.load("obstacles\water_open_left.png"),pygame.image.load("obstacles\water_open_right.png"),
          pygame.image.load("obstacles\water_end_down.png"),pygame.image.load("obstacles\water_end_up.png"),
          pygame.image.load("obstacles\water_end_left.png"),pygame.image.load("obstacles\water_end_right.png"),
          pygame.image.load("obstacles\water_four_way.png"),pygame.image.load("obstacles\water_vertical.png"),
          pygame.image.load("obstacles\water_horizontal.png"),
          pygame.image.load("obstacles\water_open_dl.png"),pygame.image.load("obstacles\water_open_ld.png"),
          pygame.image.load("obstacles\water_open_dr.png"),pygame.image.load("obstacles\water_open_rd.png"),
          pygame.image.load("obstacles\water_open_ul.png"),pygame.image.load("obstacles\water_open_lu.png"),
          pygame.image.load("obstacles\water_open_ur.png"),pygame.image.load("obstacles\water_open_ru.png"),
          pygame.image.load("obstacles\water_turn_top_right.png"),pygame.image.load("obstacles\water_turn_top_left.png"),
          pygame.image.load("obstacles\water_turn_bottom_right.png"),pygame.image.load("obstacles\water_turn_bottom_left.png"),
          pygame.image.load("obstacles\water_turn_open_top_right.png"),pygame.image.load("obstacles\water_turn_open_top_left.png"),
          pygame.image.load("obstacles\water_turn_open_bottom_right.png"),pygame.image.load("obstacles\water_turn_open_bottom_left.png"),
          pygame.image.load("obstacles\water_t_junction_up.png"),pygame.image.load("obstacles\water_t_junction_down.png"),
          pygame.image.load("obstacles\water_t_junction_left.png"),pygame.image.load("obstacles\water_t_junction_right.png"),
          pygame.image.load("obstacles\water_open_top_right.png"),pygame.image.load("obstacles\water_open_top_left.png"),
          pygame.image.load("obstacles\water_open_bottom_right.png"),pygame.image.load("obstacles\water_open_bottom_left.png")
          ]

POWERUP_IMGS = [pygame.image.load("imgs\medkit.png"),pygame.image.load("imgs\speedboost.png"),
                pygame.image.load("imgs\damageboost.png"),pygame.image.load("imgs\defenceboost.png")]


class Tank():

    def __init__(self,ID,pos,xv=0,yv=0,xa=0,ya=0,direction=0,name=''):
        self.ID = ID
        self.quit = False
        self.name = name
        self.image = 0
        if self.name == '':
            self.name = "Player" + str(self.ID+1)
        self.pos = pos
        self.xv = xv
        self.yv = yv
        self.xa = xa
        self.turret_index = 0
        self.gun_index = 2
        self.ya = ya
        self.projectiles = []
        self.direction = direction
        self.green = (0,255,0)
        self.dark_green = (9,171,3)
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.health = 100
        self.dead = False
        self.spawn_time = time.time()
        self.defence = 1
        self.immune = False
        self.kills = 0
        self.deaths = 0
        self.score = 0

    def get_mask(self):
        image = IMAGES[self.turret_index]
        return pygame.mask.from_surface(image)

    def rotate(self,surface,angle,pivot,offset):
        rotated_image = pygame.transform.rotozoom(surface,-angle,1)
        rotated_offset = offset.rotate(angle)
        rect = rotated_image.get_rect(center = pivot+rotated_offset)
        return rotated_image, rect

    def display_message(self,text,font_size,pos,display):
        surface = pygame.font.Font("imgs\clab.otf",font_size).render(text,True,(255,255,255))
        s_h = surface.get_height()
        s_w = surface.get_width()
        display.blit(surface,(pos[0]-(s_w/2),pos[1]-(s_h/2)))        

    def get_angle(self):
        mouse = pygame.mouse.get_pos()
        x_dif = mouse[0] - self.cen_x
        y_dif = mouse[1] - self.cen_y
        self.x_dif = x_dif
        self.y_dif = y_dif
        if x_dif == 0:
            x_dif += 0.01
        if y_dif == 0:
            y_dif += 0.01
        angle = math.degrees((math.atan((y_dif/x_dif))))
        if x_dif < 0:
            if y_dif < 0:
                angle += 180
            elif y_dif > 0:
                angle += 180
        elif x_dif > 0:
            if y_dif < 0:
                angle += 360
        return angle

    def get_centered_pos(self, pos, tank):
        pos = (pos[0]- tank.pos[0]+self.cen_x,pos[1] - tank.pos[1]+self.cen_y)
        return (int(pos[0]),int(pos[1]))

    def display_tank(self,display,player_tank,):
        if not self.quit:
            display_size = pygame.display.get_surface().get_size()
            cen_x = int(display_size[0]/2)
            cen_y = int(display_size[1]/2)
            self.cen_x, self.cen_y = cen_x, cen_y
            angle = self.direction
            turret = pygame.Surface((27,18),pygame.SRCALPHA)
            turret.blit(IMAGES[self.gun_index],(0,0))
            offset = pygame.math.Vector2(23,0)
            image = IMAGES[self.turret_index]
                   
            if self.ID == player_tank.ID:
                pivot = [cen_x,cen_y]
                rotated_image,rect = self.rotate(turret,angle,pivot,offset)
                display.blit(rotated_image,rect)
                image_s = image.get_size()
                display.blit(image,(cen_x-(image_s[0]/2),cen_y-(image_s[1]/2)))
                pygame.draw.rect(display,(0,0,0),(cen_x-11,cen_y-30,22,5))
                colour = ()
                if self.health < 21:
                    colour = (255,0,0)
                elif self.health < 51:
                    colour = (255,255,0)
                else:
                    colour = (0,255,0)
                pygame.draw.rect(display,colour,(cen_x-10,cen_y-29,self.health/5,3))
                self.display_message(self.name,14,(cen_x,cen_y-40),display)
                self.display_message("Kills: "+str(self.kills),20,(cen_x,30),display)
            else:
                pos = self.get_centered_pos(self.pos, player_tank)
                pivot = [pos[0], pos[1]]
                rotated_image,rect = self.rotate(turret,angle,pivot,offset)
                display.blit(rotated_image,rect)
                image_s = image.get_size()
                display.blit(image,(pos[0]-(image_s[0]/2),pos[1]-(image_s[1]/2)))
                pygame.draw.rect(display,(0,0,0),(pos[0]-11,pos[1]-30,22,5))
                colour = ()
                if self.health < 21:
                    colour = (255,0,0)
                elif self.health < 51:
                    colour = (255,255,0)
                else:
                    colour = (0,255,0)
                pygame.draw.rect(display,colour,(pos[0]-10,pos[1]-29,self.health/5,3))                
                self.display_message(self.name,14,(pos[0],pos[1]-40),display)
                
    def check_collision(self,players, barriers, powerups):
        for player in players:
            if not player.quit:
                if player.ID != self.ID:
                    # check projectile collision
                    for projectile in player.projectiles:
                        xd = self.pos[0] - projectile.pos[0]
                        yd = self.pos[1] - projectile.pos[1]
                        if (xd > -100 and xd < 100) and (yd > -100 and yd < 100):
                            player_image = IMAGES[self.turret_index]
                            player_s = player_image.get_size()
                            proj_image = IMAGES[projectile.bullet_index]
                            proj_s = proj_image.get_size()
                            offset = (int((projectile.pos[0] - (proj_s[0]/2)) - (self.pos[0] - (player_s[0]/2))), int((projectile.pos[1] - (proj_s[1]/2)) - (self.pos[1] - (player_s[1]/2))))
                            body = self.get_mask()
                            projectile_body = projectile.get_mask()
                            collision = body.overlap(projectile_body,offset)
                            if collision:
                                return 1, projectile.damage
                    # check tank collision          
                    xd = self.pos[0] - player.pos[0]
                    yd = self.pos[1] - player.pos[1]
                    if (xd > -100 and xd < 100) and (yd > -100 and yd < 100):
                        player_image = IMAGES[self.turret_index]
                        player_s = player_image.get_size()
                        
                        offset = (int((player.pos[0]-(player_s[0]/2))- (self.pos[0]-(player_s[0]/2))),int((player.pos[1]-(player_s[1]/2)) - (self.pos[1]-(player_s[1]/2))))
                        body = self.get_mask()
                        player_body = player.get_mask()
                        collision = body.overlap(player_body,offset)
                        if collision:
                            return 2, collision

        for barrier in barriers:
            xd = self.pos[0] - barrier.pos[0]
            yd = self.pos[1] - barrier.pos[1]
            if (xd > -200 and xd < 200) and (yd > -200 and yd < 200):
                player_image = IMAGES[self.turret_index]
                player_s = player_image.get_size()
                offset = (int((barrier.pos[0]) - (self.pos[0] - (player_s[0]/2))),int((barrier.pos[1]) - (self.pos[1] - (player_s[1]/2))))
                body = self.get_mask()
                barrier_body = barrier.get_mask()
                collision = body.overlap(barrier_body,offset)
                if collision:
                    return 3, collision

        for powerup in powerups:
            if not powerup.dead:
                xd = self.pos[0] - powerup.pos[0]
                yd = self.pos[1] - powerup.pos[1]
                if (xd > -100 and xd < 100) and (yd > -100 and yd < 100):
                    player_image = IMAGES[self.turret_index]
                    player_s = player_image.get_size()
                    offset = (int((powerup.pos[0]) - (self.pos[0] - (player_s[0]/2))),int((powerup.pos[1]) - (self.pos[1] - (player_s[1]/2))))
                    body = self.get_mask()
                    powerup_body = powerup.get_mask()
                    collision = body.overlap(powerup_body,offset)
                    if collision:
                        return 4, powerup.ID
        return 0,0
                

class Projectile():
    def __init__(self,ID,pos,speed,start_time, display, damage):
        self.ID = ID
        self.damage = damage
        self.pos = pos
        self.speed = speed
        self.bullet_index = 1
        self.image = 0
        self.velocity = self.get_velocity(display)
        self.quit = False
        self.start_time = start_time
        self.dead = False
        
    def get_mask(self):
        image = IMAGES[self.bullet_index]
        return pygame.mask.from_surface(image)

    def get_centered_pos(self, pos, tank):
        pos = (pos[0]- tank.pos[0]+self.cen_x,pos[1] - tank.pos[1]+self.cen_y)
        return (int(pos[0]),int(pos[1]))

    def get_index(self, tanks, ID):
        for i in range(len(tanks)):
            if tanks[i].ID == ID:
                return i

    def get_velocity(self, display):
        mouse = pygame.mouse.get_pos()
        display_size = pygame.display.get_surface().get_size()
        cen_x = int(display_size[0]/2)
        cen_y = int(display_size[1]/2)
        self.cen_x, self.cen_y = cen_x, cen_y
        x_dif = mouse[0] - self.cen_x
        y_dif = mouse[1] - self.cen_y
        dist = max(1, math.hypot(x_dif, y_dif))
        xv = self.speed * (x_dif / dist)
        yv = self.speed * (y_dif / dist)
        return (xv,yv)

    def print_projectile(self, display, tank):
        if not self.quit:
            pos = self.get_centered_pos(self.pos, tank)
            image = IMAGES[self.bullet_index]
            image_s = image.get_size()
            display.blit(image,(pos[0]-(image_s[0]/2),pos[1]-(image_s[1]/2)))
            #print("1",self.image)

    def check_collision(self,players,barriers):
        for player in players:
            if not player.quit:
                if player.ID != self.ID:
                    xd = self.pos[0] - player.pos[0]
                    yd = self.pos[1] - player.pos[1]
                    if (xd > -100 and xd < 100) and (yd > -100 and yd < 100):
                        player_image = IMAGES[player.turret_index]
                        player_s = player_image.get_size()
                        proj_image = IMAGES[self.bullet_index]
                        proj_s = proj_image.get_size()
                        offset = (int((player.pos[0] - (player_s[0]/2)) - (self.pos[0] - (proj_s[0]/2))),int((player.pos[1] - (player_s[1]/2)) - (self.pos[1] - (proj_s[1]/2))))
                        body = self.get_mask()
                        player_body = player.get_mask()
                        collision = body.overlap(player_body,offset)
                        if collision:
                            if not player.immune:
                                index = self.get_index(players,self.ID)
                                players[index].score += 5
                                if player.health - (self.damage/player.defence) <= 0:
                                    players[index].score += 20
                                    players[index].kills += 1
                            return True

        for barrier in barriers:
            xd = self.pos[0] - barrier.pos[0]
            yd = self.pos[1] - barrier.pos[1]
            if (xd > -200 and xd < 200) and (yd > -200 and yd < 200):
                if barrier.solid:
                    barrier_image = IMAGES[barrier.image_index]
                    proj_image = IMAGES[self.bullet_index]
                    proj_s = proj_image.get_size()
                    offset = (int((barrier.pos[0]) - (self.pos[0] - (proj_s[0]/2))),int((barrier.pos[1]) - (self.pos[1] - (proj_s[1]/2))))
                    body = self.get_mask()
                    barrier_body = barrier.get_mask()
                    collision = body.overlap(barrier_body,offset)
                    if collision:
                        return True
                   
        return False

class Barrier():
    def __init__(self,pos,image_index,solid = True):
        self.pos = pos
        self.image_index = image_index
        self.solid = solid

    def get_mask(self):
        image = IMAGES[self.image_index]
        return pygame.mask.from_surface(image)

    def get_centered_pos(self, pos, tank):
        pos = (pos[0]- tank.pos[0]+self.cen_x,pos[1] - tank.pos[1]+self.cen_y)
        return (int(pos[0]),int(pos[1]))

    def display_barrier(self,display,tank):
        display_size = pygame.display.get_surface().get_size()
        self.cen_x = int(display_size[0]/2)
        self.cen_y = int(display_size[1]/2)
        pos = self.get_centered_pos(self.pos,tank)
        image = IMAGES[self.image_index]
        display.blit(image, pos)

class Powerup():
    def __init__(self,pos,ID):
        self.pos = pos
        self.dead = False
        self.dead_timer = 0
        self.ID = ID
        self.image_index = ID - 1

    def get_mask(self):
        image = POWERUP_IMGS[self.image_index]
        return pygame.mask.from_surface(image)

    def get_centered_pos(self, pos, tank):
        pos = (pos[0]- tank.pos[0]+self.cen_x,pos[1] - tank.pos[1]+self.cen_y)
        return (int(pos[0]),int(pos[1]))

    def display_powerup(self,display,tank):
        if not self.dead:
            display_size = pygame.display.get_surface().get_size()
            self.cen_x = int(display_size[0]/2)
            self.cen_y = int(display_size[1]/2)
            pos = self.get_centered_pos(self.pos,tank)
            image = POWERUP_IMGS[self.image_index]
            display.blit(image, pos)

    def check_collision(self,players):
        if not self.dead:
            for player in players:
                if not player.quit:
                    xd = self.pos[0] - player.pos[0]
                    yd = self.pos[1] - player.pos[1]
                    if (xd > -100 and xd < 100) and (yd > -100 and yd < 100):
                        player_image = IMAGES[player.turret_index]
                        player_s = player_image.get_size()
                        offset = (int((player.pos[0] - (player_s[0]/2)) - self.pos[0]),int((player.pos[1] - (player_s[1]/2)) - self.pos[1]))
                        body = self.get_mask()
                        player_body = player.get_mask()
                        collision = body.overlap(player_body,offset)
                        if collision:
                            self.dead = True
                            self.dead_timer = time.time()
                            return True



        
