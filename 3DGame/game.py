import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Initialize Pygame
pygame.init()

# Set up the display window
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

# Set up the camera
gluPerspective(45, (width / height), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Car properties
car_pos = [0, 0, 0]
car_angle = 0

# Function to draw the car
def draw_car():
    glPushMatrix()
    glTranslatef(car_pos[0], car_pos[1], car_pos[2])
    glRotatef(car_angle, 0, 1, 0)
    
    # Car body (simple cube for the car)
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 1)
    # Top
    glVertex3f(-0.5, 0.3, -1)
    glVertex3f(0.5, 0.3, -1)
    glVertex3f(0.5, 0.3, 1)
    glVertex3f(-0.5, 0.3, 1)
    
    # Bottom
    glVertex3f(-0.5, -0.3, -1)
    glVertex3f(0.5, -0.3, -1)
    glVertex3f(0.5, -0.3, 1)
    glVertex3f(-0.5, -0.3, 1)
    
    # Front
    glVertex3f(-0.5, -0.3, 1)
    glVertex3f(0.5, -0.3, 1)
    glVertex3f(0.5, 0.3, 1)
    glVertex3f(-0.5, 0.3, 1)
    
    # Back
    glVertex3f(-0.5, -0.3, -1)
    glVertex3f(0.5, -0.3, -1)
    glVertex3f(0.5, 0.3, -1)
    glVertex3f(-0.5, 0.3, -1)
    
    # Left
    glVertex3f(-0.5, -0.3, -1)
    glVertex3f(-0.5, -0.3, 1)
    glVertex3f(-0.5, 0.3, 1)
    glVertex3f(-0.5, 0.3, -1)
    
    # Right
    glVertex3f(0.5, -0.3, -1)
    glVertex3f(0.5, -0.3, 1)
    glVertex3f(0.5, 0.3, 1)
    glVertex3f(0.5, 0.3, -1)
    glEnd()
    
    glPopMatrix()

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    keys = pygame.key.get_pressed()

    # Car movement
    if keys[K_LEFT]:
        car_angle += 2
    if keys[K_RIGHT]:
        car_angle -= 2
    if keys[K_UP]:
        car_pos[2] += math.cos(math.radians(car_angle)) * 0.1
        car_pos[0] += math.sin(math.radians(car_angle)) * 0.1
    if keys[K_DOWN]:
        car_pos[2] -= math.cos(math.radians(car_angle)) * 0.1
        car_pos[0] -= math.sin(math.radians(car_angle)) * 0.1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw the car
    draw_car()

    pygame.display.flip()

    # Frame rate
    clock.tick(60)
