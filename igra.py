import random
import pygame as pg
import copy
import time
import msvcrt
import sys
class keyboardDisable():

    def start(self):
        self.on = True

    def stop(self):
        self.on = False

    def __call__(self):
        while self.on:
            msvcrt.getwch()


    def __init__(self):
        self.on = False
clock = pg.time.Clock()
pozadina = (64, 64, 64)
boje = {0:(74, 74, 74),2:(255,224,153),4:(255,158,102),8:(255, 100, 71),16:(246, 189, 0),32:(100,60,10),64:(200,0,0),128:(111,53,70),256:(50,200,200),512:(125,75,199),1024:(144,10,40),2048:(255,255,180)}
tabla = []
prtabla = []
pomerajdesno=[]
pomerajdole=[]
VelicinaTable = 4 #moze da se menja velicina table, sada je 4x4
for i in range (VelicinaTable):
    tabla.append([])
    pomerajdesno.append([])
    pomerajdole.append([])
    for j in range(VelicinaTable):
        tabla[i].append(0)
        pomerajdesno[i].append(0)
        pomerajdole[i].append(0)
(sirinapolja,visinapolja)=(60,60) #mogu da se menjaju dimenzije polja
margina = 10 #moze da se menja sirina margine
dimenzijeprozora = [sirinapolja*VelicinaTable+margina*(VelicinaTable+1), visinapolja*VelicinaTable+margina*(VelicinaTable+1)]
pg.init()
prozor = pg.display.set_mode(dimenzijeprozora)
pg.display.set_caption("2048")

sledecepolje = [2,2,2,4] #posto u igrici mogu da se pojave i dvojke i cetvorke, ali redje cetvorke?
def slpolje():
    global tabla
    a=random.randint(0,VelicinaTable-1)
    b=random.randint(0,VelicinaTable-1)
    while tabla[a][b]!=0:
        a = random.randint(0, VelicinaTable-1)
        b = random.randint(0, VelicinaTable-1)
    tabla[a][b] = sledecepolje[random.randint(0,3)]
def stanjeigre():
    for i in range(VelicinaTable):
        for j in range(VelicinaTable):
            if tabla[i][j]==2048:
                return 0 #poooobeedaa
    for i in range(VelicinaTable):
        for j in range(VelicinaTable):
            if tabla[i][j]==0:
                return 1 #moze daljeee
    for i in range (VelicinaTable):
        for j in range(VelicinaTable-1):
            if tabla[i][j]==tabla[i][j+1]:
                return 1 #mozeeee
    for i in range(VelicinaTable-1):
        for j in range(VelicinaTable):
            if tabla[i][j]==tabla[i+1][j]:
                return 1 #opet mozee
    return 2 #porazz :'(
def prevrnimatricu(tabla): #transpozicija matrice
    rez = [[tabla[j][i] for j in range(len(tabla))] for i in range(len(tabla[0]))]
    return rez
def SpojiRedDesno(red):
    for j in range (VelicinaTable-1): #maks broj pomeranja nadam se
        for i in range(VelicinaTable - 1):
            if red[i+1] == 0:
                red[i+1] = red[i]
                red[i] = 0
    for i in range(VelicinaTable - 1,0,-1):
            if red[i] == red[i - 1]:
                red[i] += red[i]
                red[i-1] = 0
    for j in range(VelicinaTable - 1):
        for i in range(VelicinaTable - 1):
            if red[i+1] == 0:
                red[i+1] = red[i]
                red[i] = 0
        return red
def SpojiRedLevo(red):
    red.reverse()
    red = SpojiRedDesno(red)
    red.reverse()
    return red
def PotezDesno():
    global tabla
    for i in range(VelicinaTable):
        tabla[i] = SpojiRedDesno(tabla[i])
def PotezLevo():
    global tabla
    for i in range(VelicinaTable):
        tabla[i] = SpojiRedLevo(tabla[i])
def PotezGore():
    global tabla
    tabla = prevrnimatricu(tabla)
    for i in range(VelicinaTable):
        tabla[i] = SpojiRedLevo(tabla[i])
    tabla = prevrnimatricu(tabla)
def PotezDole():
    global tabla
    tabla = prevrnimatricu(tabla)
    for i in range(VelicinaTable):
        tabla[i] = SpojiRedDesno(tabla[i])
    tabla = prevrnimatricu(tabla)
def crtajbroj(broj, x, y):
    font = pg.font.SysFont('boulder', 35)
    tekst = font.render(str(broj), True, (255, 255, 255))
    (xbroja, ybroja) = (14, 20)
    y-=ybroja//2
    if broj<10:
        x-=xbroja//2
    elif broj<100:
        x-=xbroja
    elif broj<1000:
        x-=xbroja//2*3
    else:
        x-=2*xbroja
    prozor.blit(tekst, (x,y))
    pg.display.update()
def CrtajTablu():
    prozor.fill(pozadina)# brisanje prethodne table
    for i in range(VelicinaTable):
        for j in range(VelicinaTable):
            boja = boje.get(0, [])
            pg.draw.rect(prozor, boja,
                         [(margina + sirinapolja) * j + margina, (margina + visinapolja) * i + margina, sirinapolja,
                          visinapolja])

    for i in range(VelicinaTable):
        for j in range(VelicinaTable):
            boja = boje.get(tabla[i][j], [])
            pg.draw.rect(prozor, boja,[(margina + sirinapolja) * j + margina, (margina + visinapolja) * i + margina, sirinapolja,visinapolja])
            if tabla[i][j]!=0:
                crtajbroj(tabla[i][j],(margina + sirinapolja) * j + margina+sirinapolja//2, (margina + visinapolja) * i+margina+visinapolja//2)
def izgubiosi():
    font = pg.font.SysFont('boulder', 100)
    tekst = font.render("PORAZ", True, (255, 255, 255))
    prozor.fill(pozadina)
    prozor.blit(tekst, (19, 100))
    pg.display.update()
def pobediosi():
    font = pg.font.SysFont('boulder', 100)
    tekst = font.render("POBEDA", True, (255, 255, 255))
    prozor.fill(pozadina)
    prozor.blit(tekst, (10, 100))
    pg.display.update()
slpolje()
slpolje()
prtabla = copy.deepcopy(tabla)
CrtajTablu()
done = False
while not done:
    for dogadjaj in pg.event.get():
        if stanjeigre()==0 or stanjeigre()==2:
            for i in range(VelicinaTable):
                for j in range(VelicinaTable):
                    tabla[i][j] = 0
                    pomerajdesno[i][j] = 0
                    pomerajdole[i][j] = 0
            slpolje()
            slpolje()
            CrtajTablu()
        if dogadjaj.type == pg.QUIT:
            done = True
        elif dogadjaj.type == pg.KEYDOWN and stanjeigre()!=2:
            mogucpotez = True
            if dogadjaj.key == pg.K_LEFT:
                PotezLevo()
                CrtajTablu()
            elif dogadjaj.key == pg.K_RIGHT:
                PotezDesno()
                CrtajTablu()
            elif dogadjaj.key == pg.K_DOWN:
                PotezDole()
                CrtajTablu()
            elif dogadjaj.key == pg.K_UP:
                PotezGore()
                CrtajTablu()
            else: mogucpotez = False
            if prtabla == tabla: mogucpotez = False
            if mogucpotez:
                slpolje()
                prtabla = copy.deepcopy(tabla)
            if stanjeigre() == 2:
                izgubiosi()
            elif stanjeigre() == 0:
                pg.event.set_blocked()
                pobediosi()
    clock.tick(60)
    pg.display.flip()
pg.quit()