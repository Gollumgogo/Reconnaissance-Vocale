import pygame
import sounddevice as sd
from scipy.io.wavfile import write

from couleur import *
from graphics import *

# chemin du dossier contenant la musique que l'on veut jouer

chemin_musique=""

commandes={"lance_la_calculatrice":"Lance la calculatrice",
           "lance_la_presentation":"Lance la présentation",
           "lance_ma_musique":"Lance ma musique",
           "pourquoi_la_vie":"Pourquoi la vie",
           "prend_un_screenshot":"Prend un screenshot",
           "quelle_heure_est_il":"Quelle heure est-il",
           "raconte_une_blague":"Raconte une blague"}

couleur_fond=gris
couleur_texte=noir


###########################################
# Fonction qui permet d'afficher un texte #
###########################################

def affiche_texte(texte, rect, couleur_fond, couleur_texte, taille, screen):
    # dessin du fond coloré du bouton
    pygame.draw.rect(screen, couleur_fond, rect, 0)    
    # Initialisation de la fonte
    pygame.font.init()
    font = pygame.font.SysFont("verdana", taille, bold=False, italic=False)
    # Coordonnées du centre    
    centre = [rect[0]+rect[2]//2, rect[1]+rect[3]//2]
    # création de la surface contenant le texte
    text_area = font.render(texte, 1, couleur_texte)
    # taille de la surface contenant le texte
    text_size = font.size(texte)
    # position d'ancrage du coin en haut à gauche de la surface contenant 
    # le texte
    text_pos = [rect[0], centre[1]-text_size[1]//2]
    # ancrage de la surface contenant le texte dans la fenêtre
    screen.blit(text_area, text_pos)
    pygame.display.flip()  
    # desinitialisation de la fonte
    pygame.font.quit()
    
##################################################
# Fonction qui permet d'afficher un texte centré #
##################################################

def affiche_texte_centré(texte, rect, couleur_fond, couleur_texte ,taille, screen):
    # dessin du fond coloré du bouton
    pygame.draw.rect(screen, couleur_fond, rect, 0)    
    # Initialisation de la fonte
    pygame.font.init()
    font = pygame.font.SysFont("verdana", taille, bold=False, italic=False)
    # Coordonnées du centre    
    centre = [rect[0]+rect[2]//2, rect[1]+rect[3]//2]
    # création de la surface contenant le texte
    text_area = font.render(texte, 1, couleur_texte)
    # taille de la surface contenant le texte
    text_size = font.size(texte)
    # position d'ancrage du coin en haut à gauche de la surface contenant 
    # le texte
    text_pos = [centre[0]-text_size[0]//2, centre[1]-text_size[1]//2]
    # ancrage de la surface contenant le texte dans la fenêtre
    screen.blit(text_area, text_pos)
    pygame.display.flip()  
    # desinitialisation de la fonte
    pygame.font.quit()



#Affiche le statut du logiciel
def affichage_statut(statut, screen):
    zone_texte=[30, 500, 500, 150]
    affiche_texte("Statut : "+statut,zone_texte,couleur_fond,couleur_texte,20, screen)

#Affiche la commande détéctée
def affichage_commande(screen, commande):
    zone_texte=[30,30,500,30]
    affiche_texte("commande détéctée : " + commandes[commande],zone_texte,couleur_fond,couleur_texte,20, screen)
    dots=[30,60,20,20]
    affiche_texte("...",dots,couleur_fond,couleur_texte,20, screen)
    pygame.display.flip()

#Affiche le micro ou 3 points selon l'état de l'IA
def affichage_micro(etat, micro, screen):
    pygame.draw.rect(screen, couleur_fond, (150, 200, 200, 200))
    pygame.draw.circle(screen,couleur_fond,(250,300),80,0)
    pygame.draw.circle(screen,argent,(250,300),100,3)
    if etat==False:
        screen.blit(micro,(200,250))
        pygame.display.flip()
    else:
        pygame.draw.circle(screen,couleur_texte,(250,300),14,0)
        pygame.draw.circle(screen,couleur_texte,(200,300),14,0)
        pygame.draw.circle(screen,couleur_texte,(300,300),14,0)
        pygame.display.flip()

#Création de l'interface graphique
def affiche_ui():

    #Programme principale
    pygame.display.init()
    size = [500, 600]
    screen = pygame.display.set_mode(size)
    pygame.draw.rect(screen,couleur_fond,[0,0,500,600])
    pygame.display.flip()
    micro=pygame.image.load("icones/micro.png").convert_alpha()
    
    affichage_statut("en attente de commande vocale", screen)
    affichage_micro(False, micro, screen)
    
    return screen, micro

#Fait un enregistrement audio
def enregistrement_audio(fs, seconds):
    #ATTENTION!!! Avoir une sortie audio en cours simultanément donne un enregistrement audio de qualité bien trop mauvaise /!\
    #fs = 44100  # Sample rate
    #seconds = 3  # Durée de l'enregistrement
    print("début de l'enregistrement")
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Attend que l'enregistrement soit fini
    print("fin de l'enregistrement")
    write('ressources_des_commandes/enregistrements/enregistrement.wav', fs, myrecording)  # Enregistre dans un fichier .wav
    return 'ressources_des_commandes/enregistrements/enregistrement.wav'

#Appel des différentes fonctions
"""
lancer_la_calculatrice()
print()
donner_heure()
print()
prendre_un_screenshot()
lancer_la_musique(chemin_musique)
"""
