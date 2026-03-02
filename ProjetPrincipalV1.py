from random import randint
from tkinter import *
import tkinter as tk
import tkinter.font as font
root = Tk()
canvas = Canvas(root, width=650, height=650, background="#cbf57d")
canvas.pack(side=LEFT, padx=5, pady=10)
root.title("Projet")
liste_couleur_tkinter = ["blue4","red","dark green","gold", "black", "purple" ]
buttonFont = font.Font(family='Calibri')

liste_point = []
liste_ensemble = []

def affichage():
    n = 12
    p = 11
    for i in range(1,n):
        for j in range(p):
            canvas.create_rectangle(j*50+50,i*50,(j+1)*50+50,(i+1)*50,fill="#cbf57d", outline="#000000")
            #canvas.create_rectangle(j*36,i*36,(j+1)*36,(i+1)*36,fill="#b5bdf5")
    for i in range(n,1,-1):
        canvas.create_text(25,i*50-50,text=(13-i)*50,font=('Calibri','13','bold'))
    for j in range(1,p+1):
        canvas.create_text(j*50+50,615,text=j*50,font=('Calibri','13','bold'))
    canvas.create_text(30,615,text=0,font=('Calibri','13','bold'))
    return
affichage()




def partitionner_liste(liste):
    liste_finale = [[]]
    for element in liste:
        sous_ens = []
        for x in liste_finale:
            sous_liste = x + [element]
            sous_ens.append(sous_liste)
        liste_finale+=(sous_ens)
    return liste_finale

def hash_tuple(couple) :
    return (couple[0] + couple[1]) % 100


class Ensemble:
    hashtable = {}

    def __init__(self, liste_element):
        self.hashtable = {}
        return

    def __str__(self):
        return str(self.hashtable)

    def appartient(self, e):
        mod = hash_tuple(e)
        if mod in self.hashtable:
            liste = self.hashtable[mod]
            return e in liste
        return False

    def ajout_element(self, e) :
        if not self.appartient(e):
            mod = hash_tuple(e)
            if mod in self.hashtable:
                self.hashtable[mod].append(e)
            else :
                self.hashtable[mod] = [e]

    def supprimer_element(self, e):
        if self.appartient(e):
            mod = hash(e) % 100
            self.hashtable[mod].remove(e)

    def union(self, ens) :
        res = Ensemble([])
        for val in self.hashtable.values():
            print(res)
            for elem in val :
                res.ajout_element(elem)
        
        for val in ens.hashtable.values():
            for elem in val :
                res.ajout_element(elem)
        
        return res

    def intersection(self, ens) :
        res = Ensemble([])
        for val in self.hashtable.values():
            for elem in val :
                if ens.appartient(elem):
                    res.ajout_element(elem)        
        return res
    
    def difference(self, ens) :
        res = Ensemble([])
        for val in (self.hashtable).values():
            for elem in val :
                if not ens.appartient(elem):
                    res.ajout_element(elem)

        for val in ens.hashtable.values():
            for elem in val :
                if not self.appartient(elem):
                    res.ajout_element(elem)             

        return res

    def egal(self, ens) :
        if len(self.difference(ens).hashtable) == 0 :
            return True
        return False

    def complementaire(self, reference) :
        return self.difference(reference)

    def inclus(self, reference) :
        res = Ensemble([])
        for val in (reference.hashtable).values():
            for elem in val :
                if not self.appartient(elem):
                    return False
        return True

    def parties(self) :
        liste = []
        ens = Ensemble ([])
        for val in (self.hashtable).values():
            for elem in val :
                liste.append(elem)
            
        liste = partitionner_liste(liste)

        for lis in liste :
            somme=0
            for elem in lis:
                somme+=elem
            if somme in ens.hashtable:
                ens.hashtable[somme].append(lis)
            else :
                ens.hashtable[somme] = [lis]
        
        return ens


"""ens1 = Ensemble ([])
ens2 = Ensemble ([])
ens1.ajout_element((0,0))
ens1.ajout_element((0,2))
ens1.ajout_element((0,3))
ens1.ajout_element((0,5))


ens1.ajout_element((1,0))
ens1.ajout_element((1,2))
ens1.ajout_element((1,3))
ens1.ajout_element((1,5))

print(ens1)
print(ens2)
print(ens2.union(ens1))"""






def coor_px_vers_ecr(x, y) :
    return x + 50 , 600 - y 


def coor_ecr_vers_px(x, y) :
    return x - 50 ,  600 - y 


def affiche_point(point, couleur) :
    x,y=point
    x,y = coor_px_vers_ecr(x,y)
    canvas.create_oval(
    x-0.5, 
    y-0.5,
    x+0.5, 
    y+0.5,
    fill=couleur
)


def afficher_ens(ens, couleur) :
    ens_dict = ens.hashtable
    for liste in ens_dict.values():
        for valeur in liste :
            affiche_point(valeur, couleur)


def tracer_droite(equation, color):
    a, b = equation
    if a == 0:  # Cas pour une droite verticale
        x = b
        y1 = 0
        y2 = 550
        x1, y1 = coor_px_vers_ecr(x, y1)
        x2, y2 = coor_px_vers_ecr(x, y2)
    else:
        x1, y1 = coor_px_vers_ecr(0, b)
        x2, y2 = coor_px_vers_ecr(550, a * 550 + b)
    canvas.create_line(x1, y1, x2, y2, fill=color, width=2)



def equ_droite(point1, point2):
    if point1[0] == point2[0]:  # Cas pour une droite verticale
        return 0, point1[0]
    else:
        a = (point2[1] - point1[1]) / (point2[0] - point1[0])
        b = point1[1] - a * point1[0]
        return a, b

def comparer_sup (point, equ) :
    return point[1] >= (equ[0] * point[0] + equ[1])

def comparer_inf (point,equ) :
    return point[1] <= (equ[0] * point[0] + equ[1])

def creer_ens(equ, comp) :
    ens = Ensemble ([])
    for x in range(0,550, 2):
        for y in range(0,550,2):
            point = (x,y)
            if comp(point, equ):
                ens.ajout_element(point)
    print("Ensemble créé")
    return ens

def verifie_cote(point, equ) :
    if comparer_sup(point, equ):
        return comparer_sup # cote sup
    return comparer_inf # cote inf

def creer_triangle(point1, point2, point3, couleur) :
    ens = Ensemble ([])
    ens12 = Ensemble ([])
    ens13 = Ensemble ([])
    ens23 = Ensemble ([])
    equ12 = equ_droite(point1, point2)
    equ13 = equ_droite(point1, point3)
    equ23 = equ_droite(point2, point3)

    ens12 = creer_ens(equ12, verifie_cote(point3, equ12))
    ens13 = creer_ens(equ13, verifie_cote(point2, equ13))
    ens23 = creer_ens(equ23, verifie_cote(point1, equ23))

    print(point1,point2,point3)
    
    ens = ens12.intersection(ens13)
    ens = ens.intersection(ens23)
    print("done")

    tracer_droite(equ12,"blue")
    tracer_droite(equ13,"red")
    tracer_droite(equ23,"green")

    liste_ensemble.append(ens)
    afficher_ens(ens, couleur)

def generer_point():
    return (randint(0,550),randint(0,550))

def generer_triangle() :
    point1 = generer_point()
    point2 = generer_point()
    point3 = generer_point()
    creer_triangle(point1, point2, point3, liste_couleur_tkinter[randint(0,5)])

"""point1 = (150, 150)
point2 = (200, 200)
point3 = (250, 100)
couleur = 'gold'
creer_triangle(point1, point2, point3, couleur)"""

def faireIntersection() :
    affichage()
    while (1<len(liste_ensemble)) :
        ens1 = liste_ensemble.pop()
        ens2 = liste_ensemble.pop()
        ensInt = ens1.intersection(ens2)
        liste_ensemble.append(ensInt)
    if (len(liste_ensemble) == 1) :
        afficher_ens(liste_ensemble[0],liste_couleur_tkinter[randint(0,5)])

def faireUnion() :
    affichage()
    while (1<len(liste_ensemble)) :
        ens1 = liste_ensemble.pop()
        ens2 = liste_ensemble.pop()
        ensInt = ens1.union(ens2)
        liste_ensemble.append(ensInt)
    if (len(liste_ensemble) == 1) :
        afficher_ens(liste_ensemble[0],liste_couleur_tkinter[randint(0,5)])

#generer_triangle()
#generer_triangle()


def enregistrer_clic(event):
    global liste_point
    x, y = event.x, event.y
    if len(liste_point)<2:
        liste_point.append(coor_ecr_vers_px(x,y))
        print(x,y)
        print(coor_ecr_vers_px(x,y))
    else :
        liste_point.append(coor_ecr_vers_px(x,y))
        creer_triangle(liste_point[0], liste_point[1], liste_point[2], liste_couleur_tkinter[randint(0,5)])
        liste_point=[]



def nettoyage() :
    global liste_ensemble
    affichage()
    liste_ensemble = []





bouttonGenerer = Button(root,text="Generer Triangle", width=20, command=generer_triangle, bg='#485e1a',font=buttonFont)
bouttonGenerer.pack(side=TOP, padx=3, pady=5)

bouttonGenerer = Button(root,text="Faire intersection", width=20, command=faireIntersection, bg='#485e1a',font=buttonFont)
bouttonGenerer.pack(side=TOP, padx=3, pady=5)

bouttonGenerer = Button(root,text="Faire Union", width=20, command=faireUnion, bg='#485e1a',font=buttonFont)
bouttonGenerer.pack(side=TOP, padx=3, pady=5)

bouttonGenerer = Button(root,text="Affichage", width=20, command=affichage, bg='#485e1a',font=buttonFont)
bouttonGenerer.pack(side=TOP, padx=3, pady=5)

'''bouttonGenerer = Button(root,text="afficherCont", width=20, command=afficherCont, bg='#485e1a',font=buttonFont)
bouttonGenerer.pack(side=TOP, padx=3, pady=5)'''

canvas.bind("<Button-1>", enregistrer_clic)

root.mainloop()