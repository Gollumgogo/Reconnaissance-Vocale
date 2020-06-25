#/!\ Si le code ne se lance pas, l'executer en mode administrateur /!\

from classifier import *
from commandes import *
from ui import *
from detection import *

#################################
#IMPORTATION DES NEURAL NETWORKS#
#################################

NN_names = ["Models/1/Model_val_acc-90.79%_shape-[64, 64, 64]_inptshape-1587_date-2020-06-12 1591987802",
		"Models/1/Model_val_acc-90.79%_shape-[64, 64, 64]_inptshape-1587_date-2020-06-12 1591987802",
		"Models/2/Model_val_acc-95.93%_shape-[64, 64, 64]_inptshape-875_date-2020-06-12 1591989034",
		"Models/3/Model_val_acc-90.0%_shape-[64, 64, 64]_inptshape-634_date-2020-06-12 1591989485",
		"Models/4/Model_val_acc-79.5%_shape-[96, 64, 64, 48]_inptshape-990_date-2020-06-12 1591992522",
		"Models/5/Model_val_acc-97.22%_shape-[64, 64, 64]_inptshape-549_date-2020-06-12 1591992724",
		"Models/6/Model_val_acc-96.69%_shape-[64, 64, 64]_inptshape-574_date-2020-06-12 1591992863"]#Modèles constituant l'arbre de neural networks

PCA_names = ["PCA_model_1_1587-components.joblib",
			"PCA_model_2_875-components.joblib",
			"PCA_model_3_634-components.joblib",
			"PCA_model_4_990-components.joblib",
			"PCA_model_5_549-components.joblib",
			"PCA_model_6_574-components.joblib"]#Modèles de PCA nécessaire au prétraitement des données
			
models = import_NN(NN_names)#Importation de l'ensemble des réseaux de neurones
list_PCA_models = load_PCA_models("Dataset/json/PCA models", PCA_names)#Importation des modeles de PCA

######################################
#AFFICHAGE DE L'INTERFACE UTILISATEUR#
######################################

screen, micro = affiche_ui()

###################
#BOUCLE PRINCIPALE#
###################

print("Pour lancez l'IA, dites un mot fort ou cliquez sur le micro, puis vous aurez 4 secondes pour donner votre commande à l'oral (tant que le micro est remplacé par des points)")
print("Commandes possibles:\nLance la calculatrice,\nLance la présentation,\nLance ma musique,\nPourquoi la vie?,\nPrend un screenshot,\nQuelle heure est-il?,\nRaconte une blague.")

loop = True

while loop:
	affichage_statut("en attente de commande vocale", screen) #Affiche le statut de l'IA
	loop = detection()#Detecte si il y a un pic de décibels ou un click sur le bouton
	if loop:
		time.sleep(0.75)
		affichage_micro(True, micro, screen)#Update l'etat du micro (devient trois petits points)
		affichage_statut("Ecoute", screen)#Update le status
		print("Input détécté")
		file_name = enregistrement_audio(44100, 4)#Enregistre pendant 4s le son de l'utilisateur et l'enregistre dans un fichier (ressources_des_commandes\enregistrements\enregistrement.wav)
		affichage_micro(False, micro, screen)#Remet le micro dans son etat normal
		affichage_statut("Classification de la commande...", screen)#Update le status
		fichier = import_sound(file_name)#Ouvre le fichier audio enregistré et fait une partie du prétraitement
		predicted_command = class_sound(fichier, models, list_PCA_models)#Classe la commande enregistrée dans une catégorie (tout en finissant le prétraitement)
		affichage_commande(screen, predicted_command)#Affiche la commande détéctée
		affichage_statut("Execution de la commande...", screen)#Update le status
		print(predicted_command)
		act(predicted_command)#Execute la commande détéctée
	
		for event in pygame.event.get(): #Détecte si l'utilisateur as fermé la fenetre pour terminer le programme proprement
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					loop = False
			if event.type == pygame.QUIT:
				loop = False

pygame.mixer.quit()
pygame.quit()
