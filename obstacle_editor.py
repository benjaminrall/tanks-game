import pygame, os, time, random, json

class Block():

    def __init__(self,pos,image_index = 0):
        self.pos = pos
        self.image_index = image_index

    def print_block(self,display,image):
        display.blit(pygame.transform.scale(image,(20,20)),self.pos)

    def check_clicked(self,mouse_pos,mouse_index):
        if mouse_pos[0] > self.pos[0] and mouse_pos[0] < self.pos[0] + 20:
            if mouse_pos[1] > self.pos[1] and mouse_pos[1] < self.pos[1] + 20:
                self.image_index = mouse_index

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
level_save = json.load(open("level_save","r"))
tiles_indexes = []
for col in range(len(level_save)):
    tiles_indexes.append([])
    tiles_i = tiles_indexes[col]
    for row in range(len(level_save)):
        tiles_i.append(level_save[row][col])
        
bg_img = pygame.Surface((524,524),pygame.SRCALPHA)
for col in range(len(tiles_indexes)):
    for row in range(len(tiles_indexes)):
        bg_img.blit(pygame.transform.scale(tiles[tiles_indexes[col][row]],(20,20)),((row)*21,(col)*21))

nothing = pygame.Surface((64,64),pygame.SRCALPHA)
player_spawn = pygame.Surface((64,64),pygame.SRCALPHA)
pygame.draw.rect(player_spawn,(0,255,0),(0,0,64,64))
powerup_spawn = pygame.Surface((64,64),pygame.SRCALPHA)
pygame.draw.rect(powerup_spawn,(255,0,0),(0,0,64,64))

boulder_1 = pygame.image.load("obstacles\\boulder_1.png")
boulder_2 = pygame.image.load("obstacles\\boulder_2.png")

stonewall_end_d = pygame.image.load("obstacles\stonewall_end_down.png")
stonewall_end_u = pygame.image.load("obstacles\stonewall_end_up.png")
stonewall_end_l = pygame.image.load("obstacles\stonewall_end_left.png")
stonewall_end_r = pygame.image.load("obstacles\stonewall_end_right.png")
stonewall_t_b_l = pygame.image.load("obstacles\stonewall_turn_bottom_left.png")
stonewall_t_b_r = pygame.image.load("obstacles\stonewall_turn_bottom_right.png")
stonewall_t_t_l = pygame.image.load("obstacles\stonewall_turn_top_left.png")
stonewall_t_t_r = pygame.image.load("obstacles\stonewall_turn_top_right.png")
stonewall_v = pygame.image.load("obstacles\stonewall_vertical.png")
stonewall_h = pygame.image.load("obstacles\stonewall_horizontal.png")
stonewall_v_d = pygame.image.load("obstacles\stonewall_vertical_door.png")
stonewall_h_d = pygame.image.load("obstacles\stonewall_horizontal_door.png")

tree_1 = pygame.image.load("obstacles\\tree_1.png")

water = pygame.image.load("obstacles\water.png")
water_box = pygame.image.load("obstacles\water_box.png")
water_d = pygame.image.load("obstacles\water_down.png")
water_u = pygame.image.load("obstacles\water_up.png")
water_l = pygame.image.load("obstacles\water_left.png")
water_r = pygame.image.load("obstacles\water_right.png")
water_o_d = pygame.image.load("obstacles\water_open_down.png")
water_o_u = pygame.image.load("obstacles\water_open_up.png")
water_o_l = pygame.image.load("obstacles\water_open_left.png")
water_o_r = pygame.image.load("obstacles\water_open_right.png")
water_e_d = pygame.image.load("obstacles\water_end_down.png")
water_e_u = pygame.image.load("obstacles\water_end_up.png")
water_e_l = pygame.image.load("obstacles\water_end_left.png")
water_e_r = pygame.image.load("obstacles\water_end_right.png")
water_c = pygame.image.load("obstacles\water_four_way.png")
water_v = pygame.image.load("obstacles\water_vertical.png")
water_h = pygame.image.load("obstacles\water_horizontal.png")
water_o_d_l = pygame.image.load("obstacles\water_open_dl.png")
water_o_l_d = pygame.image.load("obstacles\water_open_ld.png")
water_o_d_r = pygame.image.load("obstacles\water_open_dr.png")
water_o_r_d = pygame.image.load("obstacles\water_open_rd.png")
water_o_u_l = pygame.image.load("obstacles\water_open_ul.png")
water_o_l_u = pygame.image.load("obstacles\water_open_lu.png")
water_o_u_r = pygame.image.load("obstacles\water_open_ur.png")
water_o_r_u = pygame.image.load("obstacles\water_open_ru.png")
water_t_t_l = pygame.image.load("obstacles\water_turn_top_left.png")
water_t_t_r = pygame.image.load("obstacles\water_turn_top_right.png")
water_t_b_l = pygame.image.load("obstacles\water_turn_bottom_left.png")
water_t_b_r = pygame.image.load("obstacles\water_turn_bottom_right.png")
water_t_o_t_l = pygame.image.load("obstacles\water_turn_open_top_left.png")
water_t_o_t_r = pygame.image.load("obstacles\water_turn_open_top_right.png")
water_t_o_b_l = pygame.image.load("obstacles\water_turn_open_bottom_left.png")
water_t_o_b_r = pygame.image.load("obstacles\water_turn_open_bottom_right.png")
water_t_junction_u = pygame.image.load("obstacles\water_t_junction_up.png")
water_t_junction_d = pygame.image.load("obstacles\water_t_junction_down.png")
water_t_junction_l = pygame.image.load("obstacles\water_t_junction_left.png")
water_t_junction_r = pygame.image.load("obstacles\water_t_junction_right.png")
water_o_t_l = pygame.image.load("obstacles\water_open_top_left.png")
water_o_t_r = pygame.image.load("obstacles\water_open_top_right.png")
water_o_b_l = pygame.image.load("obstacles\water_open_bottom_left.png")
water_o_b_r = pygame.image.load("obstacles\water_open_bottom_right.png")

images =(
(0, nothing,"delete"),
(1, player_spawn,"player spawn"),
(2, powerup_spawn,"powerup"),
(3, boulder_1,"boulder 1"),
(4, boulder_2,"boulder 2"),
(5, stonewall_end_d,"stonewall end down"),
(6, stonewall_end_u,"stonewall end up"),
(7, stonewall_end_l,"stonewall end left"),
(8, stonewall_end_r,"stonewall end right"),
(9, stonewall_t_b_l,"stonewall turn bottom left"),
(10, stonewall_t_b_r,"stonewall turn bottom right"),
(11, stonewall_t_t_l,"stonewall turn top left"),
(12, stonewall_t_t_r,"stonewall turn top right"),
(13, stonewall_v,"stonewall vertical"),
(14, stonewall_h,"stonewall horizontal"),
(15, stonewall_v_d,"stonewall vertical door"),
(16, stonewall_h_d,"stonewall horizontal door"),
(17, tree_1,"tree 1"),
(18, water,"water"),
(19, water_box,"water box"),
(20, water_d,"water down"),
(21, water_u,"water up"),
(22, water_l,"water left"),
(23, water_r,"water right"),
(24, water_o_d,"water open down"),
(25, water_o_u,"water open up"),
(26, water_o_l,"water open left"),
(27, water_o_r,"water open right"),
(28, water_e_d,"water end down"),
(29, water_e_u,"water end up"),
(30, water_e_l,"water end left"),
(31, water_e_r,"water end right"),
(32, water_c,"water cross"),
(33, water_v,"water vertical"),
(34, water_h,"water horizontal"),
(35, water_o_d_l,"water open down left"),
(36, water_o_l_d,"water open left down"),
(37, water_o_d_r,"water open down right"),
(38, water_o_r_d,"water open right down"),
(39, water_o_u_l,"water open up left"),
(40, water_o_l_u,"water open left up"),
(41, water_o_u_r,"water open up right"),
(42, water_o_r_u,"water open right up"),
(43, water_t_t_r,"water turn top right"),
(44, water_t_t_l,"water turn top left"),
(45, water_t_b_r,"water turn bottom right"),
(46, water_t_b_l,"water turn bottom left"),
(47, water_t_o_t_r,"water turn open top right"),
(48, water_t_o_t_l,"water turn open top left"),
(49, water_t_o_b_r,"water turn open bottom right"),
(50, water_t_o_b_l,"water turn open bottom left"),
(51, water_t_junction_u,"water t-junction up"),
(52, water_t_junction_d,"water t-junction down"),
(53, water_t_junction_l,"water t-junction left"),
(54, water_t_junction_r,"water t-junction right"),
(55, water_o_t_r,"water open top right"),
(56, water_o_t_l,"water open top left"),
(57, water_o_b_r,"water open bottom right"),
(58, water_o_b_l,"water open bottom left"),
)

block_grid = []
clock = pygame.time.Clock()
try:
    with open("obstacle_map_save","r") as f:
        data = json.load(f)
        print(data)
    for x in range(25):
        block_grid.append([])
        for y in range(25):
            block_grid[x].append(Block((x*21,y*21),data[x][y]))

except:

    for x in range(25):
        block_grid.append([])
        for y in range(25):
            block_grid[x].append(Block((x*21,y*21)))

display = pygame.display.set_mode((524,524))
pygame.display.set_caption("Obstacle Editor")
mouse_index = 1
display.fill((255,255,255))
mouse_down = False
while True:
    display.blit(bg_img,(0,0))
    for i in range(25):
        for j in range(25):
            block_grid[i][j].print_block(display,images[block_grid[i][j].image_index][1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_UP:
                mouse_index += 1
            if event.key == pygame.K_DOWN:
                mouse_index -= 1
            if mouse_index < 0:
                mouse_index = len(images) - 1
            if mouse_index > len(images) - 1:
                mouse_index = 0
            pygame.display.set_caption(images[mouse_index][2])
    if mouse_down:
        mouse_pos = pygame.mouse.get_pos()
        for x in range(25):
            for y in range(25):
                block_grid[x][y].check_clicked(mouse_pos,mouse_index)
    grid = []
    for d in range(25):
        grid.append([])
        for e in range(25):
            grid[d].append(images[block_grid[d][e].image_index])

    data = []
    for d in range(25):
        data.append([])
        for e in range(25):
            data[d].append(grid[d][e][0])
    
    with open("obstacle_map_save","w") as f:
        json.dump(data,f)
    pygame.display.set_icon(images[mouse_index][1])
    pygame.display.update()
    clock.tick(60)
