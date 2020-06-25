# -*- coding: utf-8 -*-

# importation du module graphique 2D pygame et system
import pygame
import sys

""" ***************************************************************************
    Fonction qui attend un appui sur la touche escape ou le bouton de 
    fermeture de la fenêtre
*************************************************************************** """

def wait_escape():
    encore = 1
    while encore == 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    encore = 0
            if event.type == pygame.QUIT:
                encore = 0
    return encore
            
""" ***************************************************************************
    Fonction qui attend un clic utilisateur avec la souris. Tant que 
    l'utilisateur ne clique pas, on attend le clic !
*************************************************************************** """

def wait_clic():
    encore = 1
    while encore == 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                clic = pygame.mouse.get_pos()
                #print(clic)
                return clic
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    encore = 0
                    pygame.quit()
                    sys.exit(0)
            if event.type == pygame.QUIT:
                encore = 0
                pygame.quit()
                sys.exit(0)