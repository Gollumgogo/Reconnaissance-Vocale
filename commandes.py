import os
import random
import pyautogui
import datetime
import pygame
import time

# need gTTS and mpg123
# pip install gTTS
from gtts import gTTS

########################################
# Différentes fonctions de l'assistant #
########################################


pygame.mixer.init(24000)#Initialisation du mixer audio de pygame

def lancer_la_calculatrice():
    os.system("C:/windows/system32/calc")

def donner_heure():
    date=datetime.datetime.now()
    h=str(date.hour)
    minute=str(date.minute)
    if len(minute)==1:
        minute="0"+minute
    heure=h+"h"+minute
    print("Il est",heure)
    gTTS("Il est {}".format(heure), lang='fr').save("ressources_des_commandes/text_to_speech/tts.mp3")#Crée un fichier son contenant la version audio du texte
    pygame.mixer.music.load("ressources_des_commandes/text_to_speech/tts.mp3")
    pygame.mixer.music.play()#Lance le fichier son sans avoir à ouvrir une nouvelle fenetre
    while pygame.mixer.music.get_busy(): #Attend qu'il ait fini de parler avant de continuer
        pygame.time.Clock().tick(10)
    pygame.mixer.music.load("ressources_des_commandes/void.wav")#Vu que pygame est infoutu de fermer un fichier audio correctement, on est obligé d'en ouvrir un vide pour qu'il libère tts.mp3 pour de futures utilisations

def prendre_un_screenshot():
    date=datetime.datetime.now()
    dates=[i for i in str(date)]
    dateheure=""
    i=0
    while i<19:
    
        if dates[i]=="-" or dates[i]==" " or dates[i]==":":
            dateheure+="_"
        else:
            dateheure+=dates[i]
        i+=1
    pyautogui.screenshot("ressources_des_commandes/screenshots/screenshot_"+dateheure+".png")
    print("Screenshot pris sous le nom de screenshot_"+dateheure+".png dans le dossier ressources_des_commandes/screenshots")

def lancer_la_musique(chemin_musique):

    morceaux=os.listdir(chemin_musique)
    aleatoire=random.randint(0,len(morceaux)-1)
    os.startfile(chemin_musique+"\\"+morceaux[aleatoire])

def lancer_la_presentation(chemin_presentation):
    os.startfile(chemin_presentation)

def pourquoi_la_vie():
    text = "Si la religion puis la philosophie se sont penchées sur cette même question, les réponses qui lui ont été données sont diverses. Jean-Paul Sartre voit en l'homme une « passion inutile », révélant le « néant » que nous sommes. Il rejoint en cela certaines orientations de la philosophie pour lesquelles les questions métaphysiques sont insolubles voire inutiles. Spinoza, lui, tout en évoquant également son impression que « les occurrences les plus fréquentes de la vie ordinaire sont vaines et futiles », se résout cependant à chercher l'existence d'« un Bien dont la découverte et la possession eussent pour fruit une éternité de joie continue et souveraine ». Entre la certitude du Néant et l'espérance d'un Bien souverain, les thèses les plus variées se sont exprimées. "
    gTTS(text, lang='fr').save("ressources_des_commandes/text_to_speech/tts.mp3")#Crée un fichier son contenant la version audio du texte
    pygame.mixer.music.load("ressources_des_commandes/text_to_speech/tts.mp3")
    pygame.mixer.music.play()#Lance le fichier son sans avoir à ouvrir une nouvelle fenetre
    loop = True
    while pygame.mixer.music.get_busy() and loop: #Attend qu'il ait fini de parler avant de continuer
        for event in pygame.event.get():#Possibilité de finir immédiatement le speech en faisant un click (parce que c'est long quand meme)
            if event.type == pygame.MOUSEBUTTONDOWN:
                loop = False
        pygame.time.Clock().tick(10)
    pygame.mixer.music.load("ressources_des_commandes/void.wav")#Vu que pygame est infoutu de fermer un fichier audio correctement, on est obligé d'en ouvrir un vide pour qu'il libère tts.mp3 pour de futures utilisations
    
def raconte_une_blague():
    with open("ressources_des_commandes/blagues.txt", "r") as fichier:#Ouvre le fchier de blagues et en fait une liste
        list_blagues = fichier.read().split("\n\n")
    gTTS(random.choice(list_blagues), lang='fr').save("ressources_des_commandes/text_to_speech/tts.mp3")#Crée un fichier son contenant la version audio d'une blague choisie aléatoirement
    pygame.mixer.music.load("ressources_des_commandes/text_to_speech/tts.mp3")
    pygame.mixer.music.play()#Lance le fichier son sans avoir à ouvrir une nouvelle fenetre
    while pygame.mixer.music.get_busy(): #Attend qu'il ait fini de parler avant de continuer
        pygame.time.Clock().tick(10)
    pygame.mixer.music.load("ressources_des_commandes/void.wav")#Vu que pygame est infoutu de fermer un fichier audio correctement, on est obligé d'en ouvrir un vide pour qu'il libère tts.mp3 pour de futures utilisations

def act(commande):
    """
    Fonction permettant d'éxécuter la fonction correspondant à la commande prédite par le modèle
    """
    if commande == "lance_ma_musique":
        lancer_la_musique("ressources_des_commandes\\musique")
    elif commande == "lance_la_calculatrice":
        lancer_la_calculatrice()
    elif commande == "lance_la_presentation":
        lancer_la_presentation("ressources_des_commandes\\presentation_assistant_commande_vocale.pptx")
    elif commande == "pourquoi_la_vie":
        pourquoi_la_vie()
    elif commande == "raconte_une_blague":
        raconte_une_blague()
    elif commande == "quelle_heure_est_il":
        donner_heure()
    elif commande == "prend_un_screenshot":
        prendre_un_screenshot()
    else:
        print("ERREUR: commande inexistante")
    return 0
