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

blank = pygame.Surface((64,64),pygame.SRCALPHA)
pygame.draw.rect(blank, (0,0,0), (0,0,64,64))
boulder_1 = pygame.image.load("obstacles\\boulder_1.png")


images =(
(0, blank, ""),
(1, boulder_1, "boulder_1"))


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
                mouse_index = len(images) - 1
            if mouse_index > len(images) - 1:
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

    pygame.display.set_caption(images[mouse_index][2])
    
    with open("obstacle_save","w") as f:
        json.dump(data,f)

    pygame.display.update()
    clock.tick(60)
