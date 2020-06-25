import pyaudio
import numpy as np
import pygame

def detection():
    """
    Fonction détectant un imput utilisateur soit sonore (au dessus du seuil de décibles fixé) ou bien un click sur le boutton de l'interface.
    Elle permet également de détecter si un utilisateur souhaite fermer le programme
    """
    CHUNK = 1024
    RATE = 44100
    limite = 5000
    peak=0
    continuer = True
    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK)
    
    loop = True
    while peak<limite and loop:
        data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        peak=np.average(np.abs(data))
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: #Si l'utilisateur clique sur le boutton
                click_pos = pygame.mouse.get_pos()
                if 170 < click_pos[0] < 330 and 220 < click_pos[1] < 380:
                    loop = False
            if event.type == pygame.KEYDOWN: #Si l'utilisateur quitte le programme
                if event.key == pygame.K_ESCAPE:
                    loop = False
                    continuer = False
            if event.type == pygame.QUIT:
                loop = False
                continuer = False
        
    print("détecté")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    return continuer
