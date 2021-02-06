import pygame
import random
import os
from network import Network

os.environ['SDL_VIDEO_CENTERED'] = '1'

SCR_WIDTH = 900
SCR_HEIGHT = 600
BG_COLOUR = (30, 30, 40)
PLAYER_COLOR = (154, 223, 252)

pygame.init()
screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption("Pong!")
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 20)

def window(screen, p1, p2, b):#, p1_score, p2_score):
    screen.fill(BG_COLOUR)
    pygame.draw.aaline(screen, (0,0,0), (SCR_WIDTH//2, 0), (SCR_WIDTH//2, SCR_HEIGHT))
    p1.draw(screen)
    p2.draw(screen)
    b.draw(screen)
    p1_score = font.render(f"{p1.score}", True, (255, 255, 255))
    p2_score = font.render(f"{p2.score}", True, (255, 255, 255))
    screen.blit(p1_score, ((SCR_WIDTH // 2) + 5, (SCR_HEIGHT // 2) - 10))
    screen.blit(p2_score, ((SCR_WIDTH // 2) - 15, (SCR_HEIGHT // 2) - 10))
    
class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 5
        self.score = 0
        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y > self.vel:
            self.y -= self.vel

        if keys[pygame.K_DOWN] and self.y < SCR_HEIGHT - self.height - self.vel:
            self.y += self.vel

        self.update()
            
    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

class Ball():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.x_vel = 4 * random.choice((-1, 1))
        self.y_vel = 4 * random.choice((-1, 1))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 255, 255), self.rect)

    def move(self, p1, p2):
        self.x += self.x_vel 
        self.y += self.y_vel 

        if self.rect.top <= 0:
            self.y_vel = 4

        if self.rect.bottom >= SCR_HEIGHT:
            self.y_vel = -4

        if self.rect.left <= 0: 
            p1.score += 1
            self.ball_start()

        if self.rect.right >= SCR_WIDTH:
            p2.score += 1
            self.ball_start()

        self.update()

    def collision(self, p1, p2):
        if self.rect.colliderect(p1.rect) or self.rect.colliderect(p2.rect):
            self.x_vel *= -1

        self.update()

    def ball_start(self):
        self.x = SCR_WIDTH//2 - 8
        self.y = SCR_HEIGHT//2 - 8
        self.x_vel = 4 * random.choice((-1, 1))
        self.y_vel = 4 * random.choice((-1, 1))
        #pygame.time.delay(2000)

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

def readPos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def makePos(tup):
    return str(tup[0]) + "," + str(tup[1])

n = Network()
startPos = readPos(n.getPos())

p1 = Player(startPos[0], startPos[1], 10, 80, PLAYER_COLOR)
p2 = Player(0, 0, 10, 80, PLAYER_COLOR)
b = Ball(SCR_WIDTH//2 - 8, SCR_HEIGHT//2 - 8, 16, 16)

run = True
while run:
    #p1_score = font.render(f"{p1.score}", True, (255, 255, 255))
    #p2_score = font.render(f"{p2.score}", True, (255, 255, 255))

    p2Pos = readPos(n.send_and_recv(makePos((p1.x, p1.y))))
    p2.x = p2Pos[0]
    p2.y = p2Pos[1]
    
    window(screen, p1, p2, b)#, p1_score, p2_score)
    p1.move()
    p2.update()
    b.move(p1, p2)
    b.collision(p1, p2)

    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()