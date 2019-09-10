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

c_junction = pygame.image.load("Tiles\cross_junction.png")
l_junction_b_l = pygame.image.load("Tiles\l_junction_bottom_left.png")
l_junction_b_r = pygame.image.load("Tiles\l_junction_bottom_right.png")
l_junction_t_l = pygame.image.load("Tiles\l_junction_top_left.png")
l_junction_t_r = pygame.image.load("Tiles\l_junction_top_right.png")
t_junction_r = pygame.image.load("Tiles\\t_junction_right.png")
t_junction_l = pygame.image.load("Tiles\\t_junction_left.png")
t_junction_u = pygame.image.load("Tiles\\t_junction_up.png")
t_junction_d = pygame.image.load("Tiles\\t_junction_down.png")

dirt_1 = pygame.image.load("Tiles\dirt_1.png")
dirt_2 = pygame.image.load("Tiles\dirt_2.png")
dirt_b_c_b_r = pygame.image.load("Tiles\dirt_border_circle_bottom_right.png")
dirt_b_c_b_l = pygame.image.load("Tiles\dirt_border_circle_bottom_left.png")
dirt_b_c_t_r = pygame.image.load("Tiles\dirt_border_circle_top_right.png")
dirt_b_c_t_l = pygame.image.load("Tiles\dirt_border_circle_top_left.png")
dirt_b_c_r = pygame.image.load("Tiles\dirt_border_circle_right.png")
dirt_b_c_l = pygame.image.load("Tiles\dirt_border_circle_left.png")
dirt_b_c_d = pygame.image.load("Tiles\dirt_border_circle_down.png")
dirt_b_c_u = pygame.image.load("Tiles\dirt_border_circle_up.png")
dirt_b_s_b_l = pygame.image.load("Tiles\dirt_border_square_bottom_left.png")
dirt_b_s_b_r = pygame.image.load("Tiles\dirt_border_square_bottom_right.png")
dirt_b_s_t_l = pygame.image.load("Tiles\dirt_border_square_top_left.png")
dirt_b_s_t_r = pygame.image.load("Tiles\dirt_border_square_top_right.png")
dirt_b_s_r = pygame.image.load("Tiles\dirt_border_square_right.png")
dirt_b_s_l = pygame.image.load("Tiles\dirt_border_square_left.png")
dirt_b_s_d = pygame.image.load("Tiles\dirt_border_square_down.png")
dirt_b_s_u = pygame.image.load("Tiles\dirt_border_square_up.png")

grass_1 = pygame.image.load("Tiles\grass_1.png")
grass_2 = pygame.image.load("Tiles\grass_2.png")
grass_b = pygame.image.load("Tiles\grass_box.png")
grass_b_s_b_l = pygame.image.load("Tiles\grass_border_square_bottom_left.png")
grass_b_s_b_r = pygame.image.load("Tiles\grass_border_square_bottom_right.png")
grass_b_s_t_l = pygame.image.load("Tiles\grass_border_square_top_left.png")
grass_b_s_t_r = pygame.image.load("Tiles\grass_border_square_top_right.png")

road_v = pygame.image.load("Tiles\\road_vertical.png")
road_h = pygame.image.load("Tiles\\road_horizontal.png")
road_t_s_b_l = pygame.image.load("Tiles\\road_turn_square_bottom_left.png")
road_t_s_b_r = pygame.image.load("Tiles\\road_turn_square_bottom_right.png")
road_t_s_t_l = pygame.image.load("Tiles\\road_turn_square_top_left.png")
road_t_s_t_r = pygame.image.load("Tiles\\road_turn_square_top_right.png")
road_t_c_b_l = pygame.image.load("Tiles\\road_turn_circle_bottom_left.png")
road_t_c_b_r = pygame.image.load("Tiles\\road_turn_circle_bottom_right.png")
road_t_c_t_l = pygame.image.load("Tiles\\road_turn_circle_top_left.png")
road_t_c_t_r = pygame.image.load("Tiles\\road_turn_circle_top_right.png")
road_t_dirt_u = pygame.image.load("Tiles\\road_to_dirt_up.png")
road_t_dirt_d = pygame.image.load("Tiles\\road_to_dirt_down.png")
road_t_dirt_l = pygame.image.load("Tiles\\road_to_dirt_left.png")
road_t_dirt_r = pygame.image.load("Tiles\\road_to_dirt_right.png")
road_e_u = pygame.image.load("Tiles\\road_end_up.png")
road_e_d = pygame.image.load("Tiles\\road_end_down.png")
road_e_l = pygame.image.load("Tiles\\road_end_left.png")
road_e_r = pygame.image.load("Tiles\\road_end_right.png")

images =(
(0, dirt_1),
(1, dirt_2),
(2, grass_1),
(3, grass_2),
(4, c_junction),
(5, dirt_b_s_b_l),
(6, dirt_b_s_b_r),
(7, dirt_b_c_d),
(8, dirt_b_c_b_l),
(9, dirt_b_c_b_r),
(10, dirt_b_c_l),
(11, dirt_b_c_r),
(12, dirt_b_c_u),
(13, dirt_b_c_t_l),
(14, dirt_b_c_t_r),
(15, dirt_b_s_d),
(16, dirt_b_s_l),
(17, dirt_b_s_r),
(18, dirt_b_s_u),
(19, dirt_b_s_t_l),
(20, dirt_b_s_t_r),
(21, grass_b_s_b_l),
(22, grass_b_s_b_r),
(23, grass_b_s_t_l),
(24, grass_b_s_t_r),
(25, grass_b),
(26, l_junction_b_l),
(27, l_junction_b_r),
(28, l_junction_t_l),
(29, l_junction_t_r),
(30, road_e_d),
(31, road_e_l),
(32, road_e_r),
(33, road_e_u),
(34, road_h),
(35, road_t_dirt_d),
(36, road_t_dirt_l),
(37, road_t_dirt_r),
(38, road_t_dirt_u),
(39, road_t_c_b_l),
(40, road_t_c_b_r),
(41, road_t_c_t_l),
(42, road_t_c_t_r),
(43, road_t_s_b_l),
(44, road_t_s_b_r),
(45, road_t_s_t_l),
(46, road_t_s_t_r),
(47, road_v),
(48, t_junction_d),
(49, t_junction_l),
(50, t_junction_r),
(51, t_junction_u))


block_grid = []
clock = pygame.time.Clock()
for x in range(25):
    block_grid.append([])
    for y in range(25):
        block_grid[x].append(Block((x*30,y*30)))

display = pygame.display.set_mode((800,800))
pygame.display.set_caption("theo died in the making of this")

mouse_index = 1
print("1")
display.fill((255,255,255))
while True:
    print("2")
    display.fill((255,255,255))
    for i in range(25):
        for j in range(25):
            block_grid[i][j].print_block(display,images[block_grid[i][j].image_index][1])

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for x in range(25):
                for y in range(25):
                    block_grid[x][y].check_clicked(mouse_pos,mouse_index)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                mouse_index += 1
            if event.key == pygame.K_DOWN:
                mouse_index -= 1
            if mouse_index < 0:
                mouse_index = 51
            if mouse_index > 51:
                mouse_index = 0

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

    pygame.display.update()
    clock.tick(60)
