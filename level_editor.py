import pygame, os, time, random, json

class Block():

    def __init__(self,pos,image_index = 1):
        self.pos = pos
        self.image_index = image_index

    def print_block(self,display,image):
        display.blit(pygame.transform.scale(image,(20,20)),self.pos)

    def check_clicked(self,mouse_pos,mouse_index):
        if mouse_pos[0] > self.pos[0] and mouse_pos[0] < self.pos[0] + 20:
            if mouse_pos[1] > self.pos[1] and mouse_pos[1] < self.pos[1] + 20:
                self.image_index = mouse_index

c_junction = pygame.image.load("tiles\cross_junction.png")
l_junction_b_l = pygame.image.load("tiles\l_junction_bottom_left.png")
l_junction_b_r = pygame.image.load("tiles\l_junction_bottom_right.png")
l_junction_t_l = pygame.image.load("tiles\l_junction_top_left.png")
l_junction_t_r = pygame.image.load("tiles\l_junction_top_right.png")
t_junction_r = pygame.image.load("tiles\\t_junction_right.png")
t_junction_l = pygame.image.load("tiles\\t_junction_left.png")
t_junction_u = pygame.image.load("tiles\\t_junction_up.png")
t_junction_d = pygame.image.load("tiles\\t_junction_down.png")
dirt_1 = pygame.image.load("tiles\dirt_1.png")
dirt_2 = pygame.image.load("tiles\dirt_2.png")
dirt_b_c_b_r = pygame.image.load("tiles\dirt_border_circle_bottom_right.png")
dirt_b_c_b_l = pygame.image.load("tiles\dirt_border_circle_bottom_left.png")
dirt_b_c_t_r = pygame.image.load("tiles\dirt_border_circle_top_right.png")
dirt_b_c_t_l = pygame.image.load("tiles\dirt_border_circle_top_left.png")
dirt_b_c_r = pygame.image.load("tiles\dirt_border_circle_right.png")
dirt_b_c_l = pygame.image.load("tiles\dirt_border_circle_left.png")
dirt_b_c_d = pygame.image.load("tiles\dirt_border_circle_down.png")
dirt_b_c_u = pygame.image.load("tiles\dirt_border_circle_up.png")
dirt_b_s_b_l = pygame.image.load("tiles\dirt_border_square_bottom_left.png")
dirt_b_s_b_r = pygame.image.load("tiles\dirt_border_square_bottom_right.png")
dirt_b_s_t_l = pygame.image.load("tiles\dirt_border_square_top_left.png")
dirt_b_s_t_r = pygame.image.load("tiles\dirt_border_square_top_right.png")
dirt_b_s_r = pygame.image.load("tiles\dirt_border_square_right.png")
dirt_b_s_l = pygame.image.load("tiles\dirt_border_square_left.png")
dirt_b_s_d = pygame.image.load("tiles\dirt_border_square_down.png")
dirt_b_s_u = pygame.image.load("tiles\dirt_border_square_up.png")
grass_1 = pygame.image.load("tiles\grass_1.png")
grass_2 = pygame.image.load("tiles\grass_2.png")
grass_b = pygame.image.load("tiles\grass_box.png")
grass_b_s_b_l = pygame.image.load("tiles\grass_border_square_bottom_left.png")
grass_b_s_b_r = pygame.image.load("tiles\grass_border_square_bottom_right.png")
grass_b_s_t_l = pygame.image.load("tiles\grass_border_square_top_left.png")
grass_b_s_t_r = pygame.image.load("tiles\grass_border_square_top_right.png")
road_v = pygame.image.load("tiles\\road_vertical.png")
road_h = pygame.image.load("tiles\\road_horizontal.png")
road_t_s_b_l = pygame.image.load("tiles\\road_turn_square_bottom_left.png")
road_t_s_b_r = pygame.image.load("tiles\\road_turn_square_bottom_right.png")
road_t_s_t_l = pygame.image.load("tiles\\road_turn_square_top_left.png")
road_t_s_t_r = pygame.image.load("tiles\\road_turn_square_top_right.png")
road_t_c_b_l = pygame.image.load("tiles\\road_turn_circle_bottom_left.png")
road_t_c_b_r = pygame.image.load("tiles\\road_turn_circle_bottom_right.png")
road_t_c_t_l = pygame.image.load("tiles\\road_turn_circle_top_left.png")
road_t_c_t_r = pygame.image.load("tiles\\road_turn_circle_top_right.png")
road_t_dirt_u = pygame.image.load("tiles\\road_to_dirt_up.png")
road_t_dirt_d = pygame.image.load("tiles\\road_to_dirt_down.png")
road_t_dirt_l = pygame.image.load("tiles\\road_to_dirt_left.png")
road_t_dirt_r = pygame.image.load("tiles\\road_to_dirt_right.png")
road_e_u = pygame.image.load("tiles\\road_end_up.png")
road_e_d = pygame.image.load("tiles\\road_end_down.png")
road_e_l = pygame.image.load("tiles\\road_end_left.png")
road_e_r = pygame.image.load("tiles\\road_end_right.png")

images =(
(0, dirt_1,"dirt_1"),
(1, dirt_2,"dirt_2"),
(2, grass_1,"grass_1"),
(3, grass_2,"grass_2"),
(4, c_junction,"cross_junction"),
(5, dirt_b_s_b_l,"dirt_border_square_bottom_left"),
(6, dirt_b_s_b_r,"dirt_border_square_bottom_right"),
(7, dirt_b_c_d,"dirt_border_circle_down"),
(8, dirt_b_c_b_l,"dirt_border_circle_bottom_left"),
(9, dirt_b_c_b_r,"dirt_border_circle_bottom_right"),
(10, dirt_b_c_l,"dirt_border_circle_left"),
(11, dirt_b_c_r,"dirt_border_circle_right"),
(12, dirt_b_c_u,"dirt_border_circle_up"),
(13, dirt_b_c_t_l,"dirt_border_circle_top_left"),
(14, dirt_b_c_t_r,"dirt_border_circle_top_right"),
(15, dirt_b_s_d,"dirt_border_square_down"),
(16, dirt_b_s_l,"dirt_border_square_left"),
(17, dirt_b_s_r,"dirt_border_square_right"),
(18, dirt_b_s_u,"dirt_border_square_up"),
(19, dirt_b_s_t_l,"dirt_border_square_top_left"),
(20, dirt_b_s_t_r,"dirt_border_square_top_right"),
(21, grass_b_s_b_l,"grass_border_square_bottom_left"),
(22, grass_b_s_b_r,"grass_border_square_bottom_right"),
(23, grass_b_s_t_l,"grass_border_square_top_left"),
(24, grass_b_s_t_r,"grass_border_square_top_right"),
(25, grass_b,"grass_box"),
(26, l_junction_b_l,"l_junction_bottom_left"),
(27, l_junction_b_r,"l_junction_bottom_right"),
(28, l_junction_t_l,"l_junction_top_left"),
(29, l_junction_t_r,"l_junction_top_right"),
(30, road_e_d,"road_end_down"),
(31, road_e_l,"road_end_left"),
(32, road_e_r,"road_end_right"),
(33, road_e_u,"road_end_up"),
(34, road_h,"road_horizontal"),
(35, road_t_dirt_d,"road_to_dirt_down"),
(36, road_t_dirt_l,"road_to_dirt_left"),
(37, road_t_dirt_r,"road_to_dirt_right"),
(38, road_t_dirt_u,"road_to_dirt_up"),
(39, road_t_c_b_l,"road_turn_circle_bottom_left"),
(40, road_t_c_b_r,"road_turn_circle_bottom_right"),
(41, road_t_c_t_l,"road_turn_circle_top_left"),
(42, road_t_c_t_r,"road_turn_circle_top_right"),
(43, road_t_s_b_l,"road_turn_square_bottom_left"),
(44, road_t_s_b_r,"road_turn_square_bottom_right"),
(45, road_t_s_t_l,"road_turn_square_top_left"),
(46, road_t_s_t_r,"road_turn_square_top_right"),
(47, road_v,"road_vertical"),
(48, t_junction_d,"t_junction_down"),
(49, t_junction_l,"t_junction_left"),
(50, t_junction_r,"t_junction_right"),
(51, t_junction_u,"t_junction_up"))


block_grid = []
clock = pygame.time.Clock()
for x in range(25):
    block_grid.append([])
    for y in range(25):
        block_grid[x].append(Block((x*30,y*30)))

display = pygame.display.set_mode((800,800))
pygame.display.set_caption("Level Editor")
mouse_index = 1
display.fill((255,255,255))
mouse_down = False
while True:
    display.fill((255,255,255))
    for i in range(25):
        for j in range(25):
            block_grid[i][j].print_block(display,images[block_grid[i][j].image_index][1])

    for event in pygame.event.get():
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
                mouse_index = 51
            if mouse_index > 51:
                mouse_index = 0
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
    
    with open("level_save","w") as f:
        json.dump(data,f)
    pygame.display.set_caption(images[mouse_index][2])
    pygame.display.set_icon(images[mouse_index][1])
    pygame.display.update()
    clock.tick(60)
