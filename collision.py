from math import *
from pygame import Vector2

def update_rect(pikk,lai,nurk,pos):
    """
    Tagastab parameetritele vastava ristküliku nurkade punktid
    """
    j = Vector2(sin(nurk/180*pi), cos(nurk/180*pi))
    i = j.rotate(90)
    return([i*lai/2 + j*pikk/2 + pos,
            -i*lai/2 + j*pikk/2 + pos,
            -i*lai/2 - j*pikk/2 + pos,
            i*lai/2 - j*pikk/2 + pos])

def seperate_and_check_axis(sidep1,sidep2,rect):
    """p1 ja p2 on selle külje kakas otsapunkti, millest konkstrueerime telje, kuhju projekteerime
    nelinurga rect punktid. (siin on arvutuslikult lihtsam, kui moodustame ühiksihivektori kui telje, aga "telg" annab asjast parema ettekujutuse)
    """
    s = (sidep1-sidep2).normalize() #ühikvektor, mis on küljega paralleelne (sihivektor)
    x = [] #ristküliku projekteeritud punktid
    y = [] #külje projekteeritud punktid
    for p in rect:
        x.append(p.dot(s)) #arvutame teise ristküliku esimese vektor projektsiooni teise ristküliku küljele
    y.append(sidep1.dot(s))
    y.append(sidep2.dot(s))
    return(max(x) > min(y) and min(x) < max(y))

def check_point_rect(p,rectpoints):
    """
    See funktsioon kontrollib, kas punkt asub ristküliku sees.
    rectpoints on järjend ristküliku punktidega.
    p on punkt, mille asumist ristkülikus tahetakse teada.
    """
    return(0 < (p-rectpoints[1]).dot(rectpoints[0]-rectpoints[1]) < (rectpoints[0]-rectpoints[1]).dot(rectpoints[0]-rectpoints[1]) and
           0 < (p-rectpoints[2]).dot(rectpoints[1]-rectpoints[2]) < (rectpoints[1]-rectpoints[2]).dot(rectpoints[1]-rectpoints[2]))
    #https://math.stackexchange.com/questions/190111/how-to-check-if-a-point-is-inside-a-rectangle

def check_circ_rect(p,r,rectpoints):
    """
    kontrollib kas ring kattub ristkülikuga
    Väga sarnane check_point_rect funktsiooniga, aga lisaks pärib:
    r, mis on ringi raadius
    pos, mis on ristküliku keskpunkti asukoht
    tagastab tõe väärtuse ja ka kokkupuutepinna normaali
    """
    normal = (0,0)
    overlap = []
    s = [] #ühikvektorid, mis on küljega paralleelsed (sihivektor)
    for i in range(2):
        s.append((rectpoints[0+i]-rectpoints[1+i]).normalize())
        x = [] #ristküliku projekteeritud punktid
        y = [] #külje projekteeritud punktid
        x.append(p.dot(s[i])-r)
        x.append(p.dot(s[i])+r)
        y.append(rectpoints[0+i].dot(s[i]))
        y.append(rectpoints[1+i].dot(s[i]))
        overlap.append(min([abs(max(x)-min(y)),abs(min(x)-max(y))]))
        if not (max(x) > min(y) and min(x) < max(y)):
            return(False,normal)
    if overlap[0] > overlap[1]:
        normal = s[0].rotate(90)
    else:
        normal = s[1].rotate(90)

    return(True,normal)

def check_rect_rect(rp1,rp2): #pean tunnistama et see on natuke kehvake aga vähemalt ma sain selle lõpuks tööle
    """
    Kontrollib kas kaks ristkülikut kattuvad omavahel
    Kasutame selleks SAT-i (Separating Axis Theorem)
    rp1 on järjend kõikedest ristküliku punktidest
    rp2 on järjend kõikidest teise ristküliku punktidest

    Siia funktsiooni tuleks veel lisada kokkupuute pinna normaalvektori.
    """
    #kontrollime iga erineva külje kohta, kas ülekatte on või ei ole.
    #Kui avastame kuskil et ülekatet ei ole, ei ole vaja rohkem kontrollida ja kutsume return False
    tulem1 = seperate_and_check_axis(rp1[0],rp1[1],rp2)
    if not tulem1: return(False)
    tulem2 = seperate_and_check_axis(rp1[1],rp1[2],rp2)
    if not tulem2: return(False)
    tulem3 = seperate_and_check_axis(rp2[0],rp2[1],rp1)
    if not tulem3: return(False)
    tulem4 = seperate_and_check_axis(rp2[1],rp2[2],rp1)
    if not tulem4: return(False)

    return(True)
