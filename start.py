import pygame
from math import *
import collision
from random import randint
#Silver Erm ja Priit Laidma

pygame.init()

# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_w = 1400
screen_h = 900
screen = pygame.display.set_mode((screen_w, screen_h))

tank_img = pygame.transform.scale(pygame.image.load("Tank.png"),(150,150))

tank_vector = pygame.Vector2()
tank_angle = 0
clock = pygame.time.Clock()
dt = 0
bullet_time = 80
bullet_speed = 400
bullet_r = 10
tank_speed = 300
s = 1
bullets = []

# ekraani_keskkoht = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

class tank:
    """
    Kuna tahame, et ekraanil oleks mitu tanki loome tanki klassi
    attributes:
    pos on tanki asukoht
    angle on tanki nurk
    vektor on tanki sihivektor
    binds on järjend, kus on sees tanki juhtimiseks vajalikud nupud nt: [key_w,key_a,key_s,key_d,key_space], kus viimane on tulistamiseks ja ülejäänud liikumiseks
    """
    delay = 0
    vel = pygame.Vector2(0,0) #kiirus
    ang_vel = 0 #nurkkiirus
    def __init__(self,pos,angle,vector,binds):
        self.pos = pos
        self.angle = angle
        self.vector = vector
        self.binds = binds
        self.points = collision.update_rect(80*s,100*s,self.ang_vel + self.angle,self.pos + self.vel)

    def update(self, dt):
        self.points = collision.update_rect(80*s,100*s,self.ang_vel + self.angle,self.pos + self.vel)
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
            self.vel.x = -scaled_tank_speed * dt * self.vector.x
            self.vel.y = -scaled_tank_speed * dt * self.vector.y
        if keys[self.binds[2]]:
            self.vel.x = scaled_tank_speed * 0.8 * dt * self.vector.x
            self.vel.y = scaled_tank_speed * 0.8 * dt * self.vector.y
        if keys[self.binds[1]]:
            self.ang_vel = 120 * dt
        if keys[self.binds[3]]:
            self.ang_vel = -120 * dt
        if keys[self.binds[4]] and self.delay <= 0:
            kuuli_algpunkt = pygame.Vector2(self.pos[:])
            kuuli_algvektor = pygame.Vector2(self.vector[:])
            kuuli_algpunkt -= kuuli_algvektor*80*s #offset, et näeks välja nagu kuul tuleks torust
            bullets.append(bullet(kuuli_algpunkt,kuuli_algvektor,bullet_time)) #asukoht, sihivektor ja eluaeg
            self.delay = 150

    def draw(self,screen, img):
        """Joonistab tanki ekraanile"""
        transform_bilt_center(screen, img, self.pos, self.angle, self.vector)

    # def update_bullets(self):
    #     for b in self.bullets:
    #         b.pos -= b.vec * dt * scaled_bullet_speed
    #         b.time -= dt * 10
    #         b.radius = bullet_r*0.2*b.time/bullet_time + 0.8*bullet_r
    #         if b.time <= 0:
    #             self.bullets.remove(b)

class bullet:
    def __init__(self,pos,vec,time):
        self.pos = pos
        self.vec = vec
        self.time = time
        self.radius = bullet_r*s

class wall:
    def __init__(self,lai,pikk,angle,pos):
        self.pos = pos
        self.points = collision.update_rect(lai,pikk,angle,pos)
        self.hp = 3

def transform_bilt_center(surf, img, pos, angle, vec): #selle funktsiooniga manipuleerime pilte nende nurga ja positsiooni põhjal, ilma neid moonutamata
    rotated = pygame.transform.rotate(pygame.transform.scale_by(img,s),angle)
    e = pygame.Vector2()
    e.x = pos.x - (rotated.get_rect()[3])/2 - vec.x * 30 * s
    e.y = pos.y - (rotated.get_rect()[2])/2 - vec.y * 30 * s
    surf.blit(rotated, e)

def map_generator(nr):
    ret_dobjects = [] #destructable objects. Seinad, mida saab lõhkuda.
    ret_objects = [] #objektide kogum. Olgu selleks kas seinad, teised tangid vms
    ret_spawnpoints = []
    with open("maps/map_0" + str(nr) +".txt") as f: gamemap = [i.strip() for i in f.readlines()]
    scale_w = screen_w/(len(list(gamemap[0])))
    scale_h = screen_h/(len(gamemap))
    ret_s = 8/max([len(list(gamemap[0]))/2,len(gamemap)]) #väga oluline muutuja. Skaleerib kõike mängus

    scale_w = screen_w/(len(list(gamemap[0]))/2+0.5)
    scale_h = screen_h/(len(gamemap)+1)

    for line,i in zip(gamemap,range(len(gamemap))):
        for item,j in zip(list(line),range(len(list(line)))):
            if item == "-":
                continue
            elif item == "s":
                ret_spawnpoints.append(pygame.Vector2(j*scale_w/2+scale_w/2,i*scale_h+scale_h))
            elif item == "b":
                if i%2 == 0:
                    ret_dobjects.append(wall(scale_w/10,scale_h*2,0,pygame.Vector2(j/2*scale_w+scale_w/2,i*scale_h+scale_h)))
                else:
                    ret_dobjects.append(wall(scale_w,scale_h/10,0,pygame.Vector2(j/2*scale_w+scale_w/2,i*scale_h+scale_h)))

    ret_objects.append(wall(screen_w,10,0,pygame.Vector2(screen_w/2,0)))
    ret_objects.append(wall(screen_w,10,0,pygame.Vector2(screen_w/2,screen_h)))
    ret_objects.append(wall(10,screen_h,0,pygame.Vector2(0,screen_h/2)))
    ret_objects.append(wall(10,screen_h,0,pygame.Vector2(screen_w,screen_h/2)))
    return(ret_objects,ret_dobjects,ret_spawnpoints,ret_s)

tank1 = tank(pygame.Vector2(0,0),0,pygame.Vector2(),[pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_SPACE])
tank2 = tank(pygame.Vector2(0,0),0,pygame.Vector2(),[pygame.K_UP,pygame.K_LEFT,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_RCTRL])

running = True
timeout = False
reset = True

timeout_time = 0

while running:
    if timeout:
        timeout_time -= 1*dt
        if timeout_time <= 0:
            reset = True
    if reset:
        bullets = []
        objects,dobjects,spawnpoints,s = map_generator(randint(1,3))
        spawn_choice = randint(0,1)
        tank1 = tank(spawnpoints[spawn_choice],0,pygame.Vector2(),[pygame.K_w,pygame.K_a,pygame.K_s,pygame.K_d,pygame.K_SPACE])
        tank2 = tank(spawnpoints[spawn_choice-1],0,pygame.Vector2(),[pygame.K_UP,pygame.K_LEFT,pygame.K_DOWN,pygame.K_RIGHT,pygame.K_RCTRL])
        tanklist = [tank1,tank2]
        scaled_bullet_speed = bullet_speed*s
        scaled_tank_speed = tank_speed*s
        reset = False
        timeout = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #kirjutab kogu ekraani üle
    screen.fill("#587270")

    keys = pygame.key.get_pressed() #nupud

    #Kutsume välja igale tankile vastavad funktsioonid
    if tank1 is not None:
        tank1.update(dt)
        tank1.check_input(dt,keys)
        tank1.draw(screen,tank_img)
    if tank2 is not None:
        tank2.update(dt)
        tank2.check_input(dt,keys)
        tank2.draw(screen,tank_img)

    #tank_collision = [collision.update_rect(80*s,100*s,tank.ang_vel + tank.angle,tank.pos + tank.vel) for tank in [tank1,tank2]]

    for t in tanklist:
        pygame.draw.polygon(screen, "green", t.points,3) #joonistame tangi collision kasti debugimiseks
        bool_collision = False
        for obj in dobjects + objects + tanklist:
            if obj == t:
                continue
            if collision.check_rect_rect(obj.points,t.points):
                bool_collision = True
                break
        if not bool_collision:
            t.pos += t.vel
            t.angle += t.ang_vel

        for b in bullets:
            if collision.check_circ_rect(b.pos,b.radius,collision.update_rect(100,80,t.angle,t.pos))[0] == True:
                print("Hit!")
                timeout_time = 3
                timeout = True
                tanklist[tanklist.index(t)] = None
                tanklist.remove(None)

    for obj in objects:
        pygame.draw.polygon(screen, "#262625", obj.points)

    for obj in dobjects:
        if obj.hp == 3:
            pygame.draw.polygon(screen, "#dfe0d9", obj.points)
        if obj.hp == 2:
            pygame.draw.polygon(screen, "#999b82", obj.points)
        if obj.hp == 1:
            pygame.draw.polygon(screen, "#874a29", obj.points)

    for b in bullets:
        pygame.draw.circle(screen, "black", b.pos, b.radius)
        for obj in objects:
            coll_info = collision.check_circ_rect(b.pos-b.vec*bullet_speed*dt,b.radius,obj.points)
            if coll_info[0]:
                b.vec = b.vec.reflect(coll_info[1])

        for obj in dobjects:
            coll_info = collision.check_circ_rect(b.pos-b.vec*bullet_speed*dt,b.radius,obj.points)
            if coll_info[0]:
                b.vec = b.vec.reflect(coll_info[1])
                obj.hp -= 1
                if obj.hp == 0:
                    dobjects.remove(obj)

        b.pos -= b.vec * dt * scaled_bullet_speed
        b.time -= dt * 10
        b.radius = (bullet_r*0.2*b.time/bullet_time + 0.8*bullet_r)*s
        if b.time <= 0:
            bullets.remove(b)

    pygame.display.flip()

    # piirab FPS 120
    dt = clock.tick(120) / 1000

pygame.quit()
