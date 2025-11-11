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

def check_rect_rect(rp1,rp2):
    # print((rp1[0]-rp1[1]).dot(rp2[0]-rp2[1]))
