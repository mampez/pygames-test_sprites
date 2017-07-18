#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Demo basada en http://razonartificial.com/tutoriales-pygame/
 
# Módulos
import sys, pygame
from pygame.locals import *
import random
 
# Constantes
WIDTH = 640
HEIGHT = 480

SPEED_X = 0.5
SPEED_Y = 0.5
K = 0.5

# ---------------------------------------------------------------------
 # Clases
# ---------------------------------------------------------------------
 
class ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) ## Inheritance: Call the parent class (Sprite) constructor
        self.image = load_image("images/ball.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = [SPEED_X, SPEED_Y]        ## x,y speed
 
    def update(self, time, racket_jug, racket_cpu, scores):

        """ We calculate the ball position based on  e = v*t  """
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time

        ## Check if the ball touch any side --> Puntuation and Restart ball
        if self.rect.left <= 0:
            scores[1] += 1
            self.rect.centerx = WIDTH / 2
            self.rect.centery = HEIGHT / 2
            self.speed = [SPEED_X + K * random.random(), SPEED_Y + K * random.random()]
            print self.speed
        if self.rect.right >= WIDTH:
            scores[0] += 1
            self.rect.centerx = WIDTH / 2
            self.rect.centery = HEIGHT / 2
            self.speed = [SPEED_X + K * random.random(), SPEED_Y + K * random.random()]
            print self.speed

        ## Collisions!

        ## Collision PARED
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
        ## Collision JUGADORES
        if pygame.sprite.collide_rect(self, racket_jug):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if pygame.sprite.collide_rect(self, racket_cpu):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time

        return scores
 
class racket(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)		## Inheritance: Call the parent class (Sprite) constructor
        self.image = load_image("images/racket.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT / 2
        self.speed = 1
 
    def mover(self, time, keys):
        if self.rect.top >= 0:
            if keys[K_UP]:
                self.rect.centery -= self.speed * time
        if self.rect.bottom <= HEIGHT:
            if keys[K_DOWN]:
                self.rect.centery += self.speed * time

    def ia(self, time, ball):
        if ball.speed[0] >= 0 and ball.rect.centerx >= WIDTH/2:
            if self.rect.centery < ball.rect.centery:
                self.rect.centery += self.speed * time
            if self.rect.centery > ball.rect.centery:
                self.rect.centery -= self.speed * time
 
# ---------------------------------------------------------------------
# Funciones
# ---------------------------------------------------------------------
 
def load_image(filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error, message:
            raise SystemExit, message
    image = image.convert()
    if transparent:
            color = image.get_at((0,0))
            image.set_colorkey(color, RLEACCEL)
    return image

def crear_texto(texto, posx, posy, color=(255, 255, 255)):
    fuente = pygame.font.Font("C:\Windows\Fonts\Arial.ttf", 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
 
# ---------------------------------------------------------------------
 
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pruebas Pygame")

    ##Puntuation
    scores = [0,0]
    
    ## Create background
    background_image = load_image('images/fondo_pong.png')

    ## Call objets: ball, player and ball
    ball = ball()
    racket_jug = racket(30)
    racket_cpu = racket(WIDTH - 30)
 
    clock = pygame.time.Clock()
 
    while True:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)
 
        ## Update ball position, player and enemy. It returns the score of both players!
        scores = ball.update(time, racket_jug, racket_cpu, scores)

        ## Update player position --> key
        racket_jug.mover(time, keys)

        ## Update cpu position --> ia
        racket_cpu.ia(time, ball)

        ## Print score
        p_jug, p_jug_rect = crear_texto(str(scores[0]), WIDTH/4, 40)
        p_cpu, p_cpu_rect = crear_texto(str(scores[1]), WIDTH-WIDTH/4, 40)

        ## Re-draw elements
        screen.blit(background_image, (0, 0))       	## Background
        screen.blit(p_jug, p_jug_rect)              	## Player puntuation
        screen.blit(p_cpu, p_cpu_rect)              	## CPU puntuations
        screen.blit(ball.image, ball.rect)          	## Ball
        screen.blit(racket_jug.image, racket_jug.rect)  ## racket
        screen.blit(racket_cpu.image, racket_cpu.rect)  ## CPU

        ## Update all changes
        pygame.display.flip()

    return 0
 
if __name__ == '__main__':
    pygame.init()
    main()
