import pygame
import sys
import random

SCREEN_WIDTH  = 480
SCREEN_HEIGHT = 480
GRIDSIZE = 20
GRIDWIDTH = SCREEN_HEIGHT/ GRIDSIZE
GRIDHEIGHT = SCREEN_WIDTH/ GRIDSIZE

lightgrid = 200,200,200
darkgrid = 250,250,250

running = True

 
UP = 0,-1
DOWN =  0,1
LEFT = -1,0
RIGHT = 1,0
MOVEMENTS = UP,DOWN,LEFT,RIGHT

SNAKE_COLOR = 0,100,150
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(240,240)]
        self.direction = random.choice(MOVEMENTS)
        self.color = SNAKE_COLOR
        self.SCORE = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (cur[0] + (x*GRIDSIZE)) % SCREEN_WIDTH , (cur[1] + (y*GRIDSIZE)) % SCREEN_HEIGHT
        if len(self.positions) > 2 and new in self.positions[2:]:
            # GAME OVER
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [(240,240)]
        self.direction = random.choice(MOVEMENTS)
        SCORE = 0

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect(p[0] +1, p[1] +1, GRIDSIZE - 1,GRIDSIZE -1)
            pygame.draw.rect(surface,self.color,r)
            #pygame.draw.rect(surface, (93,216,228), r,1)

    def handle_keys(self):
        for ev in pygame.event.get():
            type = ev.type
            if type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP:
                    self.turn(UP)
                elif ev.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif ev.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif ev.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

class Food:
    def __init__(self):
        self.position = 0,0
        self.color = (200,0,0)
        self.randomize_position()

    def randomize_position(self):
        r_x = random.randrange(0,SCREEN_WIDTH,GRIDSIZE)
        r_y = random.randrange(0,SCREEN_HEIGHT,GRIDSIZE)
        self.position = r_x,r_y

    def draw(self, surface):
        r = pygame.Rect(self.position[0], self.position[1],GRIDSIZE,GRIDSIZE)
        pygame.draw.rect(surface, self.color, r)



def drawGrid(surface , drawgrid = False):
    if drawgrid:
        for  y in range(0, int(GRIDHEIGHT) ):
            for x in range(0, int(GRIDWIDTH)) :
                if (x+y) % 2 == 0:
                    r = pygame.Rect(x*GRIDSIZE, y*GRIDSIZE,GRIDSIZE,GRIDSIZE)
                    pygame.draw.rect(surface,lightgrid, r)

                else :
                    rr = pygame.Rect(x*GRIDSIZE, y*GRIDSIZE,GRIDSIZE,GRIDSIZE)
                    pygame.draw.rect(surface, darkgrid, rr)
    else:
        surface.fill((200,200,200))
        pygame.draw.rect(surface, (0,0,0),pygame.Rect(0,480,480,530) ,0)

def text_to_gamer(  message, window, fontsize = 20, color = (200,200,200), font = 'consolas', position = (300,500)):
    #### _this function  writes  a message to the user
    pygame.font.init()
    mess_obj = pygame.font.SysFont(font, fontsize)
    mess_render = mess_obj.render(message, 20, color)
    window.blit(mess_render, position)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT+ 50))
    pygame.display.set_caption("SNAKE")
    surface = screen

    SCORE = 0
    snake = Snake()
    food = Food()
    while running:
        surface.fill((10,10,10))
        drawGrid(surface)
        text_to_gamer('SCORE :' + str(SCORE),screen )
        clock.tick(5)
        screen.blit(surface, (0,0))
        snake.move()
        snake.handle_keys()

        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()
            SCORE += 1

        snake.draw(surface)
        food.draw(surface)

        pygame.display.update()

main()
