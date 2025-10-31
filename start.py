# Example file showing a circle moving on screen
import pygame
from math import *

# pygame setup
pygame.init()

screen = pygame.display.set_mode((1280, 720))
tank_img = pygame.transform.scale(pygame.image.load("Tank.png"),(200,200))

tank_vector = pygame.Vector2()
tank_angle = 0
clock = pygame.time.Clock()
dt = 0

delay = 0
bullet_list = []


player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def transform_bilt_center(surf, img, pos, angle, vec):
    rotated = pygame.transform.rotate(img,angle)
    e = pygame.Vector2()
    e.x = pos.x - (rotated.get_rect()[3])/2 - vec.x * 30
    e.y = pos.y - (rotated.get_rect()[2])/2 - vec.y * 30
    surf.blit(rotated, e)

running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    tank_vector.xy = sin(tank_angle/180*pi), cos(tank_angle/180*pi) # tanki suunaline ühikvektor

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.x -= 300 * dt * tank_vector.x
        player_pos.y -= 300 * dt * tank_vector.y
    if keys[pygame.K_s]:
        player_pos.x += 300 * dt * tank_vector.x
        player_pos.y += 300 * dt * tank_vector.y
    if keys[pygame.K_a]:
        tank_angle += 90 * dt
    if keys[pygame.K_d]:
        tank_angle -= 90 * dt

    if keys[pygame.K_SPACE] and delay == 0:
        bullet_list.append([pygame.Vector2(player_pos[:]),pygame.Vector2(tank_vector[:]),10]) #asukoht, sihivektor ja eluaeg
        delay = 10

    if delay > 0:
        delay -= 1

    for bullet in bullet_list:
        bullet[0].x -= bullet[1].x *10
        bullet[0].y -= bullet[1].y *10
        pygame.draw.circle(screen, "black", bullet[0], 10)
        bullet[2] -= dt * 10
        if bullet[2] <= 0:
            bullet_list.remove(bullet)

    transform_bilt_center(screen, tank_img, player_pos, tank_angle, tank_vector)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
