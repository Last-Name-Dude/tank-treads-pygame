from math import *
from pygame import Vector2

def update_rect(pikk,lai,nurk,pos):
    j = Vector2(sin(nurk/180*pi), cos(nurk/180*pi))
    i = j.rotate(90)
    return([i*lai/2 + j*pikk/2 + pos,
            -i*lai/2 + j*pikk/2 + pos,
            -i*lai/2 - j*pikk/2 + pos,
            i*lai/2 - j*pikk/2 + pos])

def check_point_rect(p,rectpoints):
    return(0 < (p-rectpoints[1]).dot(rectpoints[0]-rectpoints[1]) < (rectpoints[0]-rectpoints[1]).dot(rectpoints[0]-rectpoints[1]) and
           0 < (p-rectpoints[2]).dot(rectpoints[1]-rectpoints[2]) < (rectpoints[1]-rectpoints[2]).dot(rectpoints[1]-rectpoints[2]))
    #https://math.stackexchange.com/questions/190111/how-to-check-if-a-point-is-inside-a-rectangle

def check_circ_rect(p,r,rectpoints,pos):
    return(check_point_rect(p.move_towards(pos,r),rectpoints))

def check_rect_rect(rp1,rp2): #pean tunnistama et see on natuke maagits aga vähemalt ma sain selle lõpuks tööle
    s = (rp1[0]-rp1[1]).normalize() #ühikvektor, mis on küljega paralleelne (sihivektor)
    x = []
    for p in rp2:
        x.append((p.dot(s)*s).length_squared()) #arvutame teise ristküliku esimese vektor projektsiooni teise ristküliku küljele
    parem = (rp1[0].dot(s)*s).length_squared()
    vasak = (rp1[1].dot(s)*s).length_squared()
    tingimus1 = max(x) > parem and min(x) < vasak

    s = (rp1[0]-rp1[-1]).normalize() #ühikvektor, mis on küljega paralleelne (sihivektor)
    x = []
    for p in rp2:
        x.append((p.dot(s)*s).length_squared()) #arvutame teise ristküliku teise vektor projektsiooni teise ristküliku küljele
    parem = (rp1[0].dot(s)*s).length_squared()
    vasak = (rp1[-1].dot(s)*s).length_squared()
    tingimus2 = max(x) > vasak and min(x) < parem

    return(tingimus1 and tingimus2)
