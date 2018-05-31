import sys, random, math

# pygame
import pygame
import time
from pygame.locals import *
pygame.init()

#set a caption
pygame.display.set_caption("Earth Sun Orbiting")

# set color values
black = 0, 0, 0
white = 255, 255, 255
grey = 125, 125, 125
red = 255, 0, 0
blue = 0, 0, 255

#screen size
width = 600
height = 600

# set screen
screen = pygame.display.set_mode((width,height))
screen.fill(white)

# set clock
clock = pygame.time.Clock()

# font setup
font = pygame.font.Font(None, 15)

# rotate 2D point about the origin
def rotate2D(x,y,angle):
    # convert deg to rad
    angle = 0.0174532925*angle
    x_r = x*math.cos(angle) - y*math.sin(angle)
    y_r = x*math.sin(angle) + y*math.cos(angle)
    return (x_r, y_r)

# translate 2D point
def translate2D(x,y,tx,ty):
    x_t = x+tx
    y_t = y+ty
    return (x_t, y_t)


# display FPS on the lower right corner of the screen
def show_FPS():
    text = font.render('day = ' + '{:.2f}'.format(day) + ', ' + str(int(clock.get_fps())) + ' FPS', True, black, white)
    textRect = text.get_rect()
    textRect.bottomright = screen.get_rect().bottomright
    screen.blit(text, textRect)

#zoom in out	
zoom = 1

# define control points for the Earth, sun and moon
sun_radius = 70
earth_radius = 15
moon_radius = 10
ex = 0 # center of the Earth
ey = 0
mx=0 # center of the moon
my=0

sun2earth_dis = 200 # distance from the Earth to the sun
moon2earth_dis = 50 # distance from the moon to the Earth
sun2earth_orbit = 0 # angle of the Earth orbiting around the sun
moon2earth_orbit = 0 # angle of the moon orbiting around the Earth

day = 0
flag = 1
# Loop
while flag:
    # Set FPS
    clock.tick(3600) # FPS = 60

    # Process events
    for event in pygame.event.get():
        # QUIT
        if event.type == pygame.QUIT:
            flag = 0
        # exit with escape
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            flag = 0

    # process keyboard input
    pressed = pygame.key.get_pressed()
        
    # zooming operation

    if pressed[K_UP]:
        earth_radius += zoom
        moon_radius += zoom        
        sun_radius += zoom
        moon2earth_dis += 3*zoom
        sun2earth_dis += 3*zoom
        time.sleep(0.5)
    elif pressed[K_DOWN]:
        earth_radius -= zoom
        moon_radius -= zoom        
        sun_radius -= zoom
        moon2earth_dis -= 3*zoom
        sun2earth_dis -= 3*zoom
        time.sleep(0.5)
    
    # clear screen
    screen.fill(white)

    # recalculate parameters
    day = day+0.05 # uh, here we can control the time!
    sun_spin = -(day*360.0)/30 # the Earth orbits the sun (360 deg,CCW) once every 365 days	
    earth_spin = -(day*360.0)/1
    sun2earth_spin = -(day*360.0)/365 # the Earth orbits the sun (360 deg,CCW) once every 365 days
    moon2earth_spin = -(day*360.0)/27 # the moon orbits the Earth (360 deg,CCW) once every 27 days

    # orbit the Earth and the moon around the sun
    ex_, ey_ = translate2D(ex, ey, sun2earth_dis, 0) # Orbiting the Earth and the moon (the moon sticks to the Earth)
    ex_, ey_ = rotate2D(ex_, ey_, sun2earth_spin)
    ex_, ey_ = translate2D(ex_, ey_, width/2, height/2) # translate the Earth to the center of the screen

    # orbit the moon moves around the earth
    mx_, my_ = translate2D(mx, my, moon2earth_dis, 0) 
    mx_, my_ = rotate2D(mx_, my_, sun2earth_spin+moon2earth_spin)
    mx_, my_ = translate2D(mx_, my_, ex_, ey_)

    #sun moves his own axis
    ex_1, ey_1 = translate2D(ex, ey, sun_radius, 0)
    ex_1, ey_1 = rotate2D(ex_1, ey_1, sun_spin)
    ex_1, ey_1 = translate2D(ex_1, ey_1, width/2, height/2) 

    #earth moves his own axis
    ex_2, ey_2 = translate2D(ex, ey, earth_radius, 0) 
    ex_2, ey_2 = rotate2D(ex_2, ey_2, earth_spin)
    ex_2, ey_2 = translate2D(ex_2, ey_2, ex_, ey_) 


    #moon moves arround the earth
    ex_3, ey_3 = translate2D(mx, my, moon_radius, 0) 
    ex_3, ey_3 = translate2D(ex_3, ey_3, mx_, my_) 

    
	
    # draw the Earth, sun and moon
    pygame.draw.circle(screen, red, (int(width/2), int(height/2)), sun_radius) # Sun
    pygame.draw.circle(screen, blue, (int(ex_), int(ey_)), earth_radius) # Earth
    pygame.draw.circle(screen, black, (int(mx_), int(my_)), moon_radius) # moon

    #draw a line
    pygame.draw.line(screen, black,(int(width/2), int(height/2)),(int(ex_1), int(ey_1)), 2)# Sun
    pygame.draw.line(screen, black,(int(ex_), int(ey_)),(int(ex_2), int(ey_2)), 2)# Earth
    pygame.draw.line(screen, white,(int(mx_), int(my_)),(int(ex_3), int(ey_3)), 2)# moon


    
    # show FPS
    show_FPS()
    
    # update screen
    pygame.display.flip()

pygame.quit()
