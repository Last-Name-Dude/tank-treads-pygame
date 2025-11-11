import pygame
from math import *
import collision

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


tank_img = pygame.transform.scale(pygame.image.load("Tank.png"),(150,150))

tank_vector = pygame.Vector2()
tank_angle = 0
clock = pygame.time.Clock()
dt = 0
kuuli_kiirus = 300
ekraani_keskkoht = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

all_bullets = []

def transform_bilt_center(surf, img, pos, angle, vec): #selle funktsiooniga manipuleerime pilte nende nurga ja positsiooni põhjal, ilma neid moonutamata
    rotated = pygame.transform.rotate(img,angle)
    e = pygame.Vector2()
    e.x = pos.x - (rotated.get_rect()[3])/2 - vec.x * 30
    e.y = pos.y - (rotated.get_rect()[2])/2 - vec.y * 30
    surf.blit(rotated, e)

running = True

class tank: #kuna tahame, et ekraanil oleks mitu tanki loome tanki klassi
    bullets = []
    delay = 0
    def __init__(self,pos,angle,vector,binds):
        self.pos = pos
        self.angle = angle
        self.vector = vector
        self.binds = binds

    def update(self, dt):
        self.vector.xy = sin(self.angle/180*pi), cos(self.angle/180*pi)
        if self.delay > 0:
            self.delay -= 100*dt

    def check_input(self,dt,keys):
        if keys[self.binds[0]]:
            self.pos.x -= 300 * dt * self.vector.x
            self.pos.y -= 300 * dt * self.vector.y
        if keys[self.binds[2]]:
            self.pos.x += 300 * dt * self.vector.x
            self.pos.y += 300 * dt * self.vector.y
        if keys[self.binds[1]]:
            self.angle += 90 * dt
        if keys[self.binds[3]]:
            self.angle -= 90 * dt
        if keys[self.binds[4]] and self.delay <= 0:
            kuuli_algpunkt = pygame.Vector2(self.pos[:])
            kuuli_algvektor = pygame.Vector2(self.vector[:])
            kuuli_algpunkt -= kuuli_algvektor*60 #offset, et näeks välja nagu kuul tuleks torust
            self.bullets.append([kuuli_algpunkt,kuuli_algvektor,10]) #asukoht, sihivektor ja eluaeg
            self.delay = 50

    def draw(self,screen, img):
        transform_bilt_center(screen, img, self.pos, self.angle, self.vector)

    def update_bullets(self):
        for bullet in self.bullets: #vaatab üle kõik kuulid järjendis ja liigutab neid ja vajadusel ka kustutab
            bullet[0].x -= bullet[1].x * dt * kuuli_kiirus
            bullet[0].y -= bullet[1].y * dt * kuuli_kiirus
            bullet[2] -= dt * 10
            if bullet[2] <= 0:
                self.bullets.remove(bullet)
        return(self.bullets)


tank1 = tank(pygame.Vector2(ekraani_keskkoht[:]),0,pygame.Vector2(),[pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_SPACE])
tank2 = tank(pygame.Vector2(ekraani_keskkoht[:]) + pygame.Vector2(200,0),0,pygame.Vector2(),[pygame.K_UP,pygame.K_LEFT,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_RCTRL])

while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    keys = pygame.key.get_pressed() #nupud

    tank1.update(dt)
    tank1.check_input(dt,keys)
    tank1.draw(screen,tank_img)

    tank2.update(dt)
    tank2.check_input(dt,keys)
    tank2.draw(screen,tank_img)

    hall = collision.update_rect(1000,100,15,pygame.Vector2(0,ekraani_keskkoht.y))
    tank1_kast = collision.update_rect(100,80,tank1.angle,tank1.pos)
    pygame.draw.polygon(screen, "gray", hall)
    pygame.draw.polygon(screen, "green", tank1_kast,3)

    collision.check_rect_rect(hall,tank1_kast)

    for bullet in tank1.update_bullets() + tank2.update_bullets():
        pygame.draw.circle(screen, "black", bullet[0], 7)
        if collision.check_circ_rect(bullet[0],7,collision.update_rect(100,80,tank1.angle,tank1.pos),tank1.pos) == True:
            print("Hit!")
            # pygame.quit() # see paneb praegu kinni kui kuuliga saad pihta

    pygame.display.flip()

    # piirab FPS 60
    dt = clock.tick(60) / 1000

pygame.quit()
