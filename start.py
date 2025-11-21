import pygame
from math import *
import collision
#Silver Erm ja Priit Laidma

pygame.init()

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen = pygame.display.set_mode((1200, 900))

tank_img = pygame.transform.scale(pygame.image.load("Tank.png"),(150,150))

tank_vector = pygame.Vector2()
tank_angle = 0
clock = pygame.time.Clock()
dt = 0
kuuli_kiirus = 300
ekraani_keskkoht = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

all_bullets = []
objects = [] #objektide kogum. Olgu selleks kas seinad, teised tangid vms

def transform_bilt_center(surf, img, pos, angle, vec): #selle funktsiooniga manipuleerime pilte nende nurga ja positsiooni põhjal, ilma neid moonutamata
    rotated = pygame.transform.rotate(img,angle)
    e = pygame.Vector2()
    e.x = pos.x - (rotated.get_rect()[3])/2 - vec.x * 30
    e.y = pos.y - (rotated.get_rect()[2])/2 - vec.y * 30
    surf.blit(rotated, e)

running = True

class tank:
    """
    Kuna tahame, et ekraanil oleks mitu tanki loome tanki klassi
    attributes:
    pos on tanki asukoht
    angle on tanki nurk
    vektor on tanki sihivektor
    binds on järjend, kus on sees tanki juhtimiseks vajalikud nupud nt: [key_w,key_a,key_s,key_d,key_space], kus viimane on tulistamiseks ja ülejäänud liikumiseks
    bullets on järjend, kus on sees kõik selle tanki välja tulistatud kuulid
    """
    bullets = []
    delay = 0
    vel = pygame.Vector2(0,0) #kiirus
    ang_vel = 0 #nurkkiirus
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
        """
        kontrollib sisendite vastavust määratud nuppudele ja tegutseb vastavalt
        """
        self.vel = pygame.Vector2(0,0)
        self.ang_vel = 0
        if keys[self.binds[0]]:
            self.vel.x = -300 * dt * self.vector.x
            self.vel.y = -300 * dt * self.vector.y
        if keys[self.binds[2]]:
            self.vel.x = 250 * dt * self.vector.x
            self.vel.y = 250 * dt * self.vector.y
        if keys[self.binds[1]]:
            self.ang_vel = 120 * dt
        if keys[self.binds[3]]:
            self.ang_vel = -120 * dt
        if keys[self.binds[4]] and self.delay <= 0:
            kuuli_algpunkt = pygame.Vector2(self.pos[:])
            kuuli_algvektor = pygame.Vector2(self.vector[:])
            kuuli_algpunkt -= kuuli_algvektor*60 #offset, et näeks välja nagu kuul tuleks torust
            self.bullets.append([kuuli_algpunkt,kuuli_algvektor,10]) #asukoht, sihivektor ja eluaeg
            self.delay = 50

    def draw(self,screen, img):
        """Joonistab tanki ekraanile"""
        transform_bilt_center(screen, img, self.pos, self.angle, self.vector)

    def update_bullets(self):
        """
        vaatab üle kõik kuulid järjendis ja liigutab neid ja vajadusel ka kustutab
        """
        for bullet in self.bullets:
            bullet[0].x -= bullet[1].x * dt * kuuli_kiirus
            bullet[0].y -= bullet[1].y * dt * kuuli_kiirus
            bullet[2] -= dt * 10
            if bullet[2] <= 0:
                self.bullets.remove(bullet)
        return(self.bullets)


tank1 = tank(pygame.Vector2(ekraani_keskkoht[:]),0,pygame.Vector2(),[pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_SPACE])
tank2 = tank(pygame.Vector2(ekraani_keskkoht[:]) + pygame.Vector2(200,0),0,pygame.Vector2(),[pygame.K_UP,pygame.K_LEFT,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_RCTRL])

objects.append(collision.update_rect(200,50,40,pygame.Vector2(400,500)))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #kirjutab kogu ekraani üle
    screen.fill("#7c6e44")

    keys = pygame.key.get_pressed() #nupud

    #Kutsume välja igale tankile vastavad funktsioonid
    tank1.update(dt)
    tank1.check_input(dt,keys)
    tank1.draw(screen,tank_img)

    tank2.update(dt)
    tank2.check_input(dt,keys)
    tank2.draw(screen,tank_img)

    tank_collision = [collision.update_rect(100,80,tank.ang_vel + tank.angle,tank.pos + tank.vel) for tank in [tank1,tank2]]
    bool_collision = False
    for tank,col in zip([tank1,tank2],tank_collision):
        for obj in objects + tank_collision:
            if obj == col:
                continue
            if collision.check_rect_rect(obj,col):
                bool_collision = True
                break
        if not bool_collision:
            tank.pos += tank.vel
            tank.angle += tank.ang_vel

        pygame.draw.polygon(screen, "green", col,3) #joonistame tangi collision kasti debugimiseks

    for obj in objects:
        pygame.draw.polygon(screen, "gray", obj)


    for bullet in tank1.update_bullets():
        pygame.draw.circle(screen, "black", bullet[0], 7)
        for obj in objects:
            coll_info = collision.check_circ_rect(bullet[0],7,obj)
            if coll_info[0]:
                bullet[1] = bullet[1].reflect(coll_info[1])

        if collision.check_circ_rect(bullet[0],7,collision.update_rect(100,80,tank1.angle,tank1.pos))[0] == True:
            print("Hit!")
            # pygame.quit() # see paneb praegu kinni kui kuuliga saad pihta

    pygame.display.flip()

    # piirab FPS 60
    dt = clock.tick(60) / 1000

pygame.quit()
