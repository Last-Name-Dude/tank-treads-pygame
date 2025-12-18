#Silver Erm ja Priit Laidma
#Tank Treads pygame mäng, kus kaks kohaliku mängijat juhivad tanki ja püüavad võita

#Kasutatud ressursid:
#https://math.stackexchange.com/questions/190111/how-to-check-if-a-point-is-inside-a-rectangle
#https://github.com/kidscancode/pygame_tutorials/blob/master/examples/particle%20demo.py
#https://www.pygame.org/docs/

import pygame as pg
from math import *
import collision
import particles
from random import randint, uniform, choice

pg.init()


screen = pg.display.set_mode((0, 0), pg.FULLSCREEN) #ekraan
#screen = pg.display.set_mode((1400, 900))

screen_w = screen.get_width()
screen_h = screen.get_height()

bilt_layer = pg.Surface((screen_w,screen_h)) #kiht, kuhu joonistame asju. Seda selleks, et ekraani saaks hiljem väristada

green_tank_img = pg.transform.scale(pg.image.load("roheline_tank.png"),(1024,1024))
blu_tank_img = pg.transform.scale(pg.image.load("sinine_tank.png"),(1024,1024))

green_shooting_anim = []
blu_shooting_anim = []

for i in range(20):
    if i < 10:
        i = "0" + str(i)
    green_shooting_anim.append(pg.transform.scale(pg.image.load(f"green_shooting_anim/frame00{i}.png"),(1024,1024)))
    blu_shooting_anim.append(pg.transform.scale(pg.image.load(f"blu_shooting_anim/frame00{i}.png"),(1024,1024)))

def shooting_anim(nr):
    if nr == 1:
        anim = green_shooting_anim
    else:
        anim = blu_shooting_anim
    for i in range(40):
        i = i//2
        yield(anim[i])
    while True:
        yield(anim[-1])

# skooriloenduri font
try:
    font = pg.font.Font(None, 75)  
except pg.error:
    font = pg.font.SysFont("arial", 75)

# üritab default fonti kasutada, kui miskipärast default font puudub, siis
# proovib ariali peale panna, lootuses, et arial on olemas

tank_vector = pg.Vector2()
tank_angle = 0
clock = pg.time.Clock()
dt = 0
bullet_time = 80
bullet_speed = 400
bullet_r = 10
tank_speed = 300
s = 1
bullets = []

class Tank:
    """
    Kuna tahame, et ekraanil oleks mitu tanki loome tanki klassi
    pos on tanki asukoht
    angle on tanki nurk
    vector on tanki sihivektor
    binds on järjend, kus on sees tanki juhtimiseks vajalikud nupud nt: [key_w,key_a,key_s,key_d,key_space], kus viimane on tulistamiseks ja ülejäänud liikumiseks
    """
    delay = 0 #kui tank tulistab, on viivitus enne mida ta uuesti tulistada ei saa
    vel = pg.Vector2(0,0) #kiirus
    ang_vel = 0 #nurkkiirus
    def __init__(self,pos,angle,vector,binds,nr):
        self.pos = pos
        self.angle = angle
        self.vector = vector
        self.binds = binds
        self.points = collision.update_rect(90*s,100*s,self.angle,self.vel)
        self.hp = 2
        self.nr = nr

    def update(self, dt):
        self.points = collision.update_rect(90*s,100*s,self.ang_vel + self.angle,self.pos + self.vel)
        self.vector.xy = sin(self.angle/180*pi), cos(self.angle/180*pi)
        if self.delay > 0:
            self.delay -= 100*dt

    def check_input(self,dt,keys):
        """
        kontrollib sisendite vastavust määratud nuppudele ja tegutseb vastavalt
        """
        self.vel = pg.Vector2(0,0)
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
            kuuli_algpunkt = pg.Vector2(self.pos[:])
            kuuli_algvektor = pg.Vector2(self.vector[:])
            kuuli_algpunkt -= kuuli_algvektor*70*s #offset, et näeks välja nagu kuul tuleks torust
            bullets.append(bullet(kuuli_algpunkt,kuuli_algvektor,bullet_time,self)) #asukoht, sihivektor ja eluaeg ning kes tulistas
            self.delay = 125
            self.shooting_anim = shooting_anim(self.nr)

    def draw(self,surf, img):
        """Joonistab tanki ekraanile"""
        if self.delay > 0:
             transform_bilt_center(surf, next(self.shooting_anim), self.pos, self.angle, self.vector)
        else:
            transform_bilt_center(surf, img, self.pos, self.angle, self.vector)

class bullet:
    def __init__(self,pos,vec,time,owner): #asukoht, sihivektor ja eluaeg ning kes tulistas
        self.pos = pos
        self.vec = vec
        self.time = time
        self.radius = bullet_r*s
        self.owner = owner # seob kuuli ja tanki, mis ta välja tulistas

class Wall:
    def __init__(self,lai,pikk,angle,pos,color):
        self.pos = pos
        self.points = collision.update_rect(lai,pikk,angle,pos)
        self.hp = 3
        self.color = color

def offset(count, size,time, dt):
    """
    Tagastab mingi suvalise vectori. Kasutatakse ekraani väristamiseks
    """
    while count > 0:
        count -= dt * time
        yield (uniform(0,1)*size*count**2, uniform(0,1)*size*count**2)
    while True:
        yield (0, 0)


def transform_bilt_center(surf, img, pos, angle, vec):
    """selle funktsiooniga manipuleerime pilte nende nurga ja positsiooni põhjal, ilma neid moonutamata"""
    rotated = pg.transform.rotozoom(img,angle,s/7)
    e = pg.Vector2()
    e.x = pos.x - (rotated.get_rect()[3])/2 - vec.x * 18 * s
    e.y = pos.y - (rotated.get_rect()[2])/2 - vec.y * 18 * s
    surf.blit(rotated, e)

def map_generator(nr):
    """see funktsioon loeb maps kaustast suvalise tekstifaili ja selle põhjal konstrueerib kaardi, mille peal mängitakse"""
    ret_dobjects = [] #destructable objects. Seinad, mida saab lõhkuda.
    ret_objects = [] #objektide kogum. Olgu selleks välisääre seinad
    ret_spawnpoints = []
    with open("maps/map_0" + str(nr) +".txt") as f: gamemap = [i.strip() for i in f.readlines()]

    ret_s = 8/max([len(list(gamemap[0]))/2,len(gamemap)])*screen_w/1400 #väga oluline muutuja. Skaleerib kõike mängus

    scale_w = screen_w/(len(list(gamemap[0]))/2+0.5)
    scale_h = screen_h/(len(gamemap)+1)

    #Allpool olev tsükel lisab vastavalt tähemärgile objektide järjendisse seina, kui täht on b, ja tanki potentsiaalse tekkekoha, kui on s
    for line,i in zip(gamemap,range(len(gamemap))):
        for item,j in zip(list(line),range(len(list(line)))):
            if item == "-":
                continue
            elif item == "s":
                ret_spawnpoints.append(pg.Vector2(j*scale_w/2+scale_w/2,i*scale_h+scale_h))
            elif item == "b":
                if i%2 == 0:
                    ret_dobjects.append(Wall(scale_w/10,scale_h*2,0,pg.Vector2(j/2*scale_w+scale_w/2,i*scale_h+scale_h),"#dfe0d9"))
                else:
                    ret_dobjects.append(Wall(scale_w,scale_h/10,0,pg.Vector2(j/2*scale_w+scale_w/2,i*scale_h+scale_h),"#dfe0d9"))

    #Välised seinad, mida lõhkuda ei saa
    ret_objects.append(Wall(screen_w,10,0,pg.Vector2(screen_w/2,0),"#514f51"))
    ret_objects.append(Wall(screen_w,10,0,pg.Vector2(screen_w/2,screen_h),"#514f51"))
    ret_objects.append(Wall(10,screen_h,0,pg.Vector2(0,screen_h/2),"#514f51"))
    ret_objects.append(Wall(10,screen_h,0,pg.Vector2(screen_w,screen_h/2),"#514f51"))
    return(ret_objects,ret_dobjects,ret_spawnpoints,ret_s)

tank1 = Tank(pg.Vector2(0, 0), 0, pg.Vector2(), [pg.K_w, pg.K_a, pg.K_s, pg.K_d, pg.K_SPACE], 1)
tank2 = Tank(pg.Vector2(0, 0), 0, pg.Vector2(), [pg.K_UP, pg.K_LEFT, pg.K_DOWN, pg.K_RIGHT, pg.K_RCTRL], 2)

global tank1_skoor, tank2_skoor
tank1_skoor = 0
tank2_skoor = 0 # mängu alguses mõlemal 0 punkti

shake = offset(0,10, 10,dt)
running = True
timeout = False
reset = True

r_toggle = False

timeout_time = 0

particuls = particles.particles_initalize()

while running:
    if timeout:
        #Kui tank ära sureb, on ~3 sekundiline ajavahemik, mil vastastank peab elus püsima, et punkti saada
        timeout_time -= 1*dt
        if timeout_time <= 0:
            reset = True

    if reset:
        #Toimub mängu alguses ja siis, kui mõlemad tankid ära kärvavad
        if tank2.hp == 0 and tank1.hp == 0:
            pass
        elif tank2.hp == 0:
            tank1_skoor += 1
        elif tank1.hp == 0:
            tank2_skoor += 1
        print(f"Tank 1 skoor (roheline) : {tank1_skoor} | Tank 2 skoor (sinine): {tank2_skoor}")
        bullets = []
        objects,dobjects,spawnpoints,s = map_generator(randint(1,5))

        spawn_choice = choice(spawnpoints) #võimalikest tekkekohtadest valitakse üks
        tank1 = Tank(spawn_choice, choice([i*60 for i in range(6)]), pg.Vector2(), [pg.K_w, pg.K_a, pg.K_s, pg.K_d, pg.K_SPACE],1)
        spawnpoints.remove(spawn_choice) #et tankid üksteise otsa ei tekiks
        tank2 = Tank(choice(spawnpoints), choice([i*60 for i in range(6)]), pg.Vector2(), [pg.K_UP, pg.K_LEFT, pg.K_DOWN, pg.K_RIGHT, pg.K_RCTRL],2)

        tanklist = [tank1,tank2]
        scaled_bullet_speed = bullet_speed*s
        scaled_tank_speed = tank_speed*s
        reset = False
        timeout = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False


    #kirjutab kogu ekraani üle
    bilt_layer.fill("#576b72")

    keys = pg.key.get_pressed() #nupud

    if keys[pg.K_r] and keys[pg.K_LCTRL]: #Vajutades klahvikombinatsiooni saab uuesti mängu laadida
        if r_toggle:
            reset = True
            r_toggle = False
    else:
        r_toggle = True


    #Kutsume välja igale tankile vastavad funktsioonid
    if tank1 is not None:
        tank1.update(dt)
        tank1.check_input(dt,keys)
        tank1.draw(bilt_layer,green_tank_img)
    if tank2 is not None:
        tank2.update(dt)
        tank2.check_input(dt,keys)
        tank2.draw(bilt_layer,blu_tank_img)

    for t in tanklist:
        #pg.draw.polygon(bilt_layer, "green", t.points, 3) # tanki collision kast debugimiseks
        #allpool kontrollitakse, kas tanki järgmine positsioon kattub ühegi seinaga või mitte. Kui kattub, ei lase tankil edasi liikuda
        bool_collision = False
        other_tanks = [other_t for other_t in tanklist if other_t != t]
        all_collision_objects = dobjects + objects + other_tanks
        
        for obj in all_collision_objects:
            if collision.check_rect_rect(obj.points,t.points):
                bool_collision = True
                break

        if not bool_collision:
            t.pos += t.vel
            t.angle += t.ang_vel

    for obj in objects + dobjects:
        pg.draw.polygon(bilt_layer, obj.color, obj.points)

    for b in bullets:
        #Kuulidega seotud kokkupõrgete kontrollimine
        pg.draw.circle(bilt_layer, "black", b.pos, b.radius)
        for obj in objects:
            coll_info = collision.check_circ_rect(b.pos-b.vec*bullet_speed*dt,b.radius,obj.points)
            if coll_info[0]:
                b.vec = b.vec.reflect(coll_info[1])

        #Lõhutavad seinad
        #Seina värv muutub vastavalt tema lõhutavuse tasemele
        for obj in dobjects:
            coll_info = collision.check_circ_rect(b.pos-b.vec*bullet_speed*dt,b.radius,obj.points)
            if coll_info[0]:
                b.vec = b.vec.reflect(coll_info[1])
                obj.hp -= 1
                if obj.hp == 3:
                    obj.color = "#dfe0d9"
                elif obj.hp == 2:
                    obj.color = "#999b82"
                elif obj.hp == 1:
                    obj.color = "#874a29"
                elif obj.hp == 0:
                    dobjects.remove(obj)

        for t in tanklist:
            if collision.check_circ_rect(b.pos, b.radius, t.points)[0]:
                print("Hit!")
                particles.fat_puff(bilt_layer, t.pos, s*0.5, 3) #Kui tank pihta saab tekitab suitsupilve
                shake = offset(1,20, 1, dt)
                t.hp -= 1
                timeout_time = 3 #Iga kord kui keegi pihta saab siis timeout-i taimer alustab otsast
                if t.hp <= 0:
                    timeout = True
                    tanklist.remove(t)
                bullets.remove(b)
                break

        b.pos -= b.vec * dt * scaled_bullet_speed
        b.time -= dt * 10
        b.radius = (bullet_r*0.2*b.time/bullet_time + 0.8*bullet_r)*s #kuuli raadius kahane aja jooksul
        if b.time <= 0:
            bullets.remove(b)
            particles.puff(bilt_layer, b.pos, s*0.4)

    particuls.update(dt)
    particuls.draw(bilt_layer)

    score_text = font.render(f"Roheline: {tank1_skoor} | Sinine: {tank2_skoor}", True, (0, 0, 0))
    score_rect = score_text.get_rect(center=(screen_w // 2, 30))
    bilt_layer.blit(score_text, score_rect)

    #Ekraani väristamiseks
    screen.blit(bilt_layer, next(shake))

    screen.blit(pg.font.Font(None, 30).render(f"FPS: {round(1/dt,0)}" if dt != 0 else f"FPS: 0" , True, (0,0,0)),(20,20))
    pg.display.flip()

    # piirab FPS 60
    dt = clock.tick(60) / 1000

pg.quit()
