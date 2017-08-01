import pygame
import random
import math

## Colours
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DARKBLUE = (0,0,128)
WHITE = (255,255,255)
BLACK = (0,0,0)
PINK = (255,200,200)

PI = math.pi

colours_list = [RED, GREEN, DARKBLUE,  BLUE, BLACK, PINK]

## Background
background_colour = WHITE
(WIDTH, HEIGHT) = (600, 480)


drag = 0.999
elasticity = 0.75
gravity = (PI, 0.005)


def findParticle(particles, x, y):
    for p in particles:
        if math.hypot(p.x-x, p.y-y) <= p.size:
            return p
    return None

def collide(p1, p2):

    """ The first thing the function has to do is to test whether 
        the two particles have collided. This is very simple as 
        the particles are circles """

    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * PI + tangent

        """ We need to exchange the speeds of the two particles 
           as they transfer their energy to on another """

        angle1 = 2*tangent - p1.angle
        angle2 = 2*tangent - p2.angle

        """ Rreduce the energy of both particles as a 
            result of the collision """

        speed1 = p2.speed*elasticity
        speed2 = p1.speed*elasticity

        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)

        """ Update values for new x,y and angles """

        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)

def addVectors((angle1, length1), (angle2, length2)):

    """
    Function takes two vectors (each an angle and a length), and returns single, combined a vector. 
    First we move along one vector, 
    then along the other to find the x,y coordinates for where the particle would end up 

    """

    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * PI - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

pygame.init()
# creamos la ventana y le indicamos un titulo:
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Player():
    
    def __init__(self, (x, y), size, speed, angle):
        self.x = x
        self.y = y
        self.size = size
        self.colour = random.choice(colours_list)
        self.thickness = 1
        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag

    def bounce(self):
        ## Bounce X (RIGHT)
        if self.x > WIDTH - self.size:
            self.x = 2*(WIDTH - self.size) - self.x
            self.angle = - self.angle

        ## Bounce X (LEFT)
        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle

        ## Bounce Y (BOTTON)
        if self.y > HEIGHT - self.size:
            self.y = 2*(HEIGHT - self.size) - self.y
            self.angle = PI - self.angle

        ## Bounce Y (CEILING)
        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = PI - self.angle



def main():


    pygame.display.set_caption('Tutorial 4')
    clock = pygame.time.Clock()

    size = 10
    x = 30
    y = 30
    speed = 0.05
    angle = PI
    player = Player((x, y), size, speed, angle)

    is_blue = True
    done = False

    while not done:

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            done = True

                    ## KEYDOWN es 'apretada'
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            is_blue = not is_blue

           
            screen.fill(background_colour)

            pressed = pygame.key.get_pressed()

            if pressed[pygame.K_UP]: 
                player.y -= 1
                player.angle = 0 
                player.speed = 0.5
                print 'up'
            if pressed[pygame.K_DOWN]: 
                player.y += 1
                player.angle = PI
                player.speed = 0.5
                print 'down'
            if pressed[pygame.K_LEFT]: 
                player.x -= 1
                player.angle = (5*PI/2) + PI/4
                player.speed = -0.5
                print 'left'
            if pressed[pygame.K_RIGHT]: 
                player.x += 1
                player.angle = PI/2 + (- PI/4)
                player.speed = 0.5
                print 'right'
                
            player.move()
            player.bounce()
            player.display() 
            print(player.x,player.y,player.angle,player.speed)          
            ## Update screen
            pygame.display.flip()
            clock.tick(60)




if __name__ == "__main__":
    main()

