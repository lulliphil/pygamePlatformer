import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

tile_size = 100

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (screen_width, screen_height))

n_horizontal_lines = screen.get_height()/tile_size
n_vertical_lines = screen.get_width()/tile_size


def draw_grid():
    for line in range(int(n_horizontal_lines)):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size), 1)
    for line in range(int(n_vertical_lines)):
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height), 1)

class Player():
    def __init__(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 7):
            img_right = pygame.image.load(f'guy{num}.png')
            img_right = pygame. transform.scale(img_right, (30, 70))
            img_left = pygame. transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        
    def update(self):
        dx = 0
        dy = 0
        walk_cooldown = 20
        
        
        #get key presses
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = -15
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 10
            self.counter += 1
        if key[pygame.K_RIGHT]:
            dx += 10
            self.counter += 1
        
        
        #handle animation
        if self.counter > walk_cooldown:
            self.countr = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            self.image = self.images_right[self.index]
        
        
        #gavity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y    
            
        self.rect.x += dx
        self.rect.y += dy
        
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0
            
            

        
        screen.blit(self.image, self.rect)
        
        
class Wolrd():
    def __init__(self, data):
         self.tile_list = []
        
         
         grass_img = pygame.image.load('grass.png')
         dirt_img = pygame.image.load('dirt.png')
         
         row_count = 0
         for row in data:
             col_count = 0
             for tile in row:
                 #PLACE DIRT (tile = 1)
                 if tile == 1:
                     img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                     img_rect = img.get_rect()
                     img_rect.x = col_count * tile_size
                     img_rect.y = row_count * tile_size
                     tile = (img, img_rect)
                     self.tile_list.append(tile)
                
                 #PLACE GRASS (tile = 2)
                 elif tile == 2:
                     img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                     img_rect = img.get_rect()
                     img_rect.x = col_count * tile_size
                     img_rect.y = row_count * tile_size
                     tile = (img, img_rect)
                     self.tile_list.append(tile)
                     
                     
                 col_count += 1
             row_count += 1
            
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])     
                  

world_data = [
[1,0,0,0,0,0,0,0,0,0],
[1,0,0,0,2,0,0,2,2,2],
[1,0,0,2,0,0,0,0,0,0],
[1,2,0,0,0,0,0,0,0,0],
[1,1,2,2,2,2,0,0,0,0],
[0,0,0,0,0,0,0,2,0,0],
[0,0,0,0,0,0,2,1,2,0],
[2,2,2,2,2,2,1,1,1,2]]


player = Player(150, screen_height - tile_size - 160)
world =  Wolrd(world_data)

run = True

while run:
    
    clock.tick(fps)
    
    screen.blit(BG, (0, 0))
    
    #SCREEN.BLIT() METHODS TO VISUALIZE
    world.draw()
    player.update()
    
    draw_grid()
    
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.display.update()
    

pygame.quit()
    