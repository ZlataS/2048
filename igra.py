import random
import pygame as pg
import copy
clock = pg.time.Clock()
pozadina = (64, 64, 64)
boje = {0:(74, 74, 74),2:(255,224,153),4:(255,158,102),8:(255, 100, 71),16:(246, 189, 0),32:(100,60,10),64:(200,0,0),128:(111,53,70),256:(50,200,200),512:(125,75,199),1024:(144,10,40),2048:(255,255,180)}
tabla = []
prtabla = []
VelicinaTable = 4 #moze da se menja velicina table, sada je 4x4
(sirinapolja,visinapolja)=(60,60) #mogu da se menjaju dimenzije polja
margina = 10 #moze da se menja sirina margine
def prvaigra():
    global dimenzijeprozora
    global tabla
    global prozor
    global prtabla
    for i in range(VelicinaTable):
        tabla.append([])
        for j in range(VelicinaTable):
            tabla[i].append(0)
    dimenzijeprozora = [sirinapolja * VelicinaTable + margina * (VelicinaTable + 1),
                        visinapolja * VelicinaTable + margina * (VelicinaTable + 1)]
    prozor = pg.display.set_mode(dimenzijeprozora)
    slpolje()
    slpolje()
    prtabla = copy.deepcopy(tabla)
    CrtajTablu()
pg.init()
prozor = pg.display.set_mode([280,320])
pg.display.set_caption("2048")
prozor.fill(pozadina)
font = pg.font.SysFont('boulder', 40)
tekst = font.render("Izaberi tablu:", True, (255, 255, 255))
prozor.blit(tekst, (50, 20))
pg.draw.rect(prozor,(255,158,102),[20, 60, 110, 110])
pg.draw.rect(prozor,(255,158,102),[150, 60, 110, 110])
pg.draw.rect(prozor,(255,158,102),[20, 190, 110, 110])
pg.draw.rect(prozor,(255,158,102),[150, 190, 110, 110])
font = pg.font.SysFont('boulder', 40)
tekst = font.render("3x3", True, (255, 255, 255))
prozor.blit(tekst, (50, 100))
tekst = font.render("4x4", True, (255, 255, 255))
prozor.blit(tekst, (180, 100))
tekst = font.render("5x5", True, (255, 255, 255))
prozor.blit(tekst, (50, 230))
tekst = font.render("6x6", True, (255, 255, 255))
prozor.blit(tekst, (180, 230))
pg.display.update()
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
    for j in range (VelicinaTable): #maks broj pomeranja nadam se
        for i in range(VelicinaTable - 1):
            if red[i+1] == 0:
                red[i+1] = red[i]
                red[i] = 0
    for i in range(VelicinaTable - 1,0,-1):
            if red[i] == red[i - 1]:
                red[i] += red[i]
                red[i-1] = 0
    for j in range(VelicinaTable):
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
    #pg.display.update()
def CrtajTablu():
    prozor.fill(pozadina)# brisanje prethodne table
    for i in range(VelicinaTable):
        for j in range(VelicinaTable):
            boja = boje.get(tabla[i][j], [])
            pg.draw.rect(prozor, boja,[(margina + sirinapolja) * j + margina, (margina + visinapolja) * i + margina, sirinapolja,visinapolja])
            if tabla[i][j]!=0:
                crtajbroj(tabla[i][j],(margina + sirinapolja) * j + margina+sirinapolja//2, (margina + visinapolja) * i+margina+visinapolja//2)
    pg.display.flip()
izgubio_si = False
pobedio_si = False
font = pg.font.SysFont('boulder', 20)
tekst2 = font.render("pritisni SPACE da pokrenes novu partiju", True, (255, 255, 255))
done = False
while not done:
    if izgubio_si:
        font = pg.font.SysFont('boulder', 100)
        tekst = font.render("PORAZ", True, (255, 255, 255))
        prozor.fill(pozadina)
        prozor.blit(tekst, ((VelicinaTable - 4) * ((sirinapolja + margina) // 2) + 19, dimenzijeprozora[1] // 2 - 45))
        prozor.blit(tekst2, ((VelicinaTable - 4) * ((sirinapolja + margina) // 2) + 20, dimenzijeprozora[1] // 2 + 20))
        pg.display.update()
    elif pobedio_si:
        font = pg.font.SysFont('boulder', 100)
        tekst = font.render("POBEDA", True, (255, 255, 255))
        prozor.fill(pozadina)
        prozor.blit(tekst, ((VelicinaTable - 4) * ((sirinapolja + margina) // 2), dimenzijeprozora[1] // 2 - 45))
        prozor.blit(tekst2, ((VelicinaTable - 4) * ((sirinapolja + margina) // 2) + 20, dimenzijeprozora[1] // 2 + 20))
        pg.display.update()
    for dogadjaj in pg.event.get():
        if dogadjaj.type == pg.QUIT:
            done = True
        elif dogadjaj.type == pg.MOUSEBUTTONDOWN:
            (mis_x,mis_y) = pg.mouse.get_pos()
            if mis_x>=140 and mis_y>=180:
                VelicinaTable = 6
            elif mis_x>=140 and mis_y<180:
                VelicinaTable = 4
            elif mis_x<140 and mis_y<180:
                VelicinaTable = 3
            else: VelicinaTable = 5
            prvaigra()
            poceloje = True
        elif dogadjaj.type == pg.KEYDOWN:
            mogucpotez = True
            if dogadjaj.key == pg.K_SPACE:
                pobedio_si = False
                izgubio_si = False
                for i in range(VelicinaTable):
                    for j in range(VelicinaTable):
                        tabla[i][j] = 0
                slpolje()
                slpolje()
                CrtajTablu()

            else:
                if dogadjaj.key == pg.K_LEFT:
                    PotezLevo()
                elif dogadjaj.key == pg.K_RIGHT:
                    PotezDesno()
                elif dogadjaj.key == pg.K_DOWN:
                    PotezDole()
                elif dogadjaj.key == pg.K_UP:
                    PotezGore()
                else:
                    mogucpotez = False
                if prtabla == tabla:
                    mogucpotez = False
                if mogucpotez:
                    slpolje()
                    CrtajTablu()
                    prtabla = copy.deepcopy(tabla)
                if stanjeigre() == 2:
                    izgubio_si = True
                elif stanjeigre() == 0:
                    pobedio_si = True
    clock.tick(60)
pg.quit()