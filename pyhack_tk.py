import random as rd
import os
from tkinter import *


class Map:

    def __init__(self, longueur, largeur):
        """
        Initialisation d'une map avec que des * puis des salles et des couloirs.
        Ensuite vient la génération du personage et la gestion de ses déplacements.
        Enfin l'affichage.
        """
        self.longueur = longueur
        self.largeur = largeur
        txt = open('pyhack', 'w')
        for _ in range(self.largeur):
            chaine=""
            for _ in range(self.longueur):
                chaine += "*"
            txt.write(chaine + "\n")
        txt.close()
        txt = open('pyhack','r')
        self.lignes = txt.readlines()
        txt.close()
        self.salle()
        if len(self.coin_salle) > 1:
            self.sorties_salles()
            self.couloirs()
        self.position_perso()

    def contours(self):
        for ligne in self.lignes:
            for e in ligne:
                if e == ".":
                    a=1

    def salle(self): #self.salle = [coin_haut_gauche, longueur, largeur]
        """
        génération de salles aléatoires
        """                                          #coin_haut_gauche = (lignes, colonne)

        def salle_valide(coin_haut_gauche, longueur_salle, largeur_salle): #attention pour les couloirs deux salles peuvent étre coller
            """
            vérification pas de superposition de salles
            """
            for i in range(coin_haut_gauche[0], coin_haut_gauche[0] + largeur_salle):
                for j in range(coin_haut_gauche[1], coin_haut_gauche[1] + longueur_salle):
                    if self.lignes[i][j] != '*':
                        return False
            return True

        self.coin_salle = []
        nb_salle = rd.randrange(1, 8)
        for _ in range(nb_salle):
            non_valide = True
            largeur_salle = rd.randrange(5, 10)
            longueur_salle = rd.randrange(5, 10)
            while non_valide:
                coin_haut_gauche = (rd.randrange(largeur_salle, self.largeur - largeur_salle), rd.randrange(longueur_salle, self.longueur-longueur_salle))
                if salle_valide(coin_haut_gauche, longueur_salle, largeur_salle):
                    non_valide = False
            for i in range(coin_haut_gauche[0], coin_haut_gauche[0] + largeur_salle):
                for j in range(coin_haut_gauche[1], coin_haut_gauche[1] + longueur_salle):
                    self.lignes[i] = self.lignes[i][:j] + "." + self.lignes[i][j+1:]
            self.coin_salle.append([coin_haut_gauche, longueur_salle, largeur_salle])

    def sorties_salles(self):
        """
        création de sorties associées à chaque salle
        """

        def contours(salles):
            contours = []
            for salle in salles:
                contour = []
                for i in range(salle[0][0], salle[0][0] + salle[2]):
                    if i == salle[0][0] or i == salle[0][0] + salle[2] - 1:
                        for j in range(salle[0][1], salle[0][1] + salle[1]):
                            contour.append((i, j))
                    else:
                        contour.append((i, salle[0][1]))
                        contour.append((i, salle[0][1] + salle[1] -1))
                contours.append(contour)
            return contours

        contours = contours(self.coin_salle)
        # for salle in contours:   #vérification contours
        #     for point in salle:
        #         i = point[0]
        #         j = point[1]
        #         self.lignes[i] = self.lignes[i][:j] + "/" + self.lignes[i][j+1:]
        self.sortie = []
        for i in range(len(self.coin_salle)):
            nb_sorties = rd.randrange(1, 2)
            for _ in range(nb_sorties):
                sortie = rd.choice(contours[i])
                j = rd.randrange(len(self.coin_salle))
                while j == i:
                    j = rd.randrange(len(self.coin_salle))
                entree = rd.choice(contours[j])
                self.sortie.append((sortie, entree))

        for entree in self.sortie:
            for point in entree:
                i = point[0]
                j = point[1]
                self.lignes[i] = self.lignes[i][:j] + "." + self.lignes[i][j+1:]

    def couloirs(self):
        """
        génération de couloirs
        """
        for entree, sortie in self.sortie:
            chemin = []
            if entree[0] == min(entree[0], sortie[0]):
                direction_verticale = "bas"
            else:
                direction_verticale = "haut"
            if entree[1] == min(entree[1], sortie[1]):
                direction_horizontale = "droite"
            else:
                direction_horizontale = "gauche"
            i, j = entree[0], entree[1]
            while i != sortie[0] or j != sortie[1]:
                a = rd.randrange(1,3)
                if direction_verticale == "bas" and direction_horizontale == "droite":
                    if a == 1 and i!= sortie[0]:  #on descend
                        self.lignes[i+1] = self.lignes[i+1][:j] + "." + self.lignes[i+1][j+1:]
                        i += 1
                    elif a == 2 and j!= sortie[1]: #on va a droite
                        self.lignes[i] = self.lignes[i][:j+1] + "." + self.lignes[i][j+2:]
                        j += 1
                elif direction_verticale == "bas" and direction_horizontale == "gauche":
                    if a == 1 and i!= sortie[0]:
                        self.lignes[i+1] = self.lignes[i+1][:j] + "." + self.lignes[i+1][j+1:]
                        i += 1
                    elif a == 2 and j!= sortie[1]:
                        self.lignes[i] = self.lignes[i][:j-1] + "." + self.lignes[i][j:]
                        j -= 1
                elif direction_verticale == "haut" and direction_horizontale == "droite":
                    if a == 1 and i!= sortie[0]:
                        self.lignes[i-1] = self.lignes[i-1][:j] + "." + self.lignes[i-1][j+1:]
                        i -= 1
                    elif a == 2 and j!= sortie[1]:
                        self.lignes[i] = self.lignes[i][:j+1] + "." + self.lignes[i][j+2:]
                        j += 1
                elif direction_verticale == "haut" and direction_horizontale == "gauche":
                    if a == 1 and i!= sortie[0]:
                        self.lignes[i-1] = self.lignes[i-1][:j] + "." + self.lignes[i-1][j+1:]
                        i -= 1
                    elif a == 2 and j!= sortie[1]:
                        self.lignes[i] = self.lignes[i][:j-1] + "." + self.lignes[i][j:]
                        j -= 1

    def position_perso(self):
        """
        initialise la position du personnage @
        """
        coord = []
        for i in range(len(self.lignes)):
            for j in range(len(self.lignes[0])):
                if self.lignes[i][j] == ".":
                    coord.append((i,j))
        self.position_perso = rd.choice(coord)
        i = self.position_perso[0]
        j = self.position_perso[1]
        self.lignes[i] = self.lignes[i][:j] + "@" + self.lignes[i][j+1:]

    def ini_affichage(self):
        self.fen = Tk()
        self.fen.title("Pyhack")
        self.text = Text(self.fen, bg="black", fg="white", height=len(self.lignes), width=len(self.lignes[0])-1)
        self.text.pack()
        self.affichage()

    def affichage(self):
        """
        génére l'affichage sur le terminal, attention aux notations différentes pour windows et linux
        """
        print(1)
        self.text.config(state=NORMAL)
        self.text.delete("1.0", "end")
        tx = ""
        for e in self.lignes:
            tx += e
        self.text.insert(INSERT, tx)
        self.text.config(state=DISABLED)
        self.fen.bind('<Up>', self.deplacement_haut)
        self.fen.bind('<Down>', self.deplacement_bas)
        self.fen.bind('<Right>', self.deplacement_droite)
        self.fen.bind('<Left>', self.deplacement_gauche)

    def deplacement_valide(self, i ,j):
        if self.lignes[i][j] == ".":
            return True
        else:
            return False

    def deplacement_haut(self, event):
        i = self.position_perso[0]
        j = self.position_perso[1]
        if self.deplacement_valide(i-1, j):
            self.lignes[i-1] = self.lignes[i-1][:j] + "@" + self.lignes[i-1][j+1:]
            self.lignes[i] = self.lignes[i][:j] + "." + self.lignes[i][j+1:]
            self.position_perso = (i-1, j)
            self.affichage()

    def deplacement_bas(self, event):
        i = self.position_perso[0]
        j = self.position_perso[1]
        if self.deplacement_valide(i+1, j):
            self.lignes[i+1] = self.lignes[i+1][:j] + "@" + self.lignes[i+1][j+1:]
            self.lignes[i] = self.lignes[i][:j] + "." + self.lignes[i][j+1:]
            self.position_perso = (i+1, j)
            self.affichage()

    def deplacement_droite(self, event):
        i = self.position_perso[0]
        j = self.position_perso[1]
        if self.deplacement_valide(i, j+1):
            self.lignes[i] = self.lignes[i][:j] + "." + "@" + self.lignes[i][j+2:]
            self.position_perso = (i, j+1)
            self.affichage()

    def deplacement_gauche(self, event):
        i = self.position_perso[0]
        j = self.position_perso[1]
        if self.deplacement_valide(i, j-1):
            self.lignes[i] = self.lignes[i][:j-1] + "@" + "." + self.lignes[i][j+1:]
            self.position_perso = (i, j-1)
            self.affichage()


jeux = Map(100, 30)
jeux.ini_affichage()
jeux.fen.mainloop()
