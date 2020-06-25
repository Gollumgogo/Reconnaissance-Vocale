#/!\    Ce code ne fonctionne que si il est lancé en mode administrateur    /!\#
#/!\Sinon librosa ne s'importe pas et bloque le code dans une boucle infinie/!\#

##############
#IMPORTATIONS#
##############

import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import json
import sklearn
from joblib import dump, load

def import_all_sounds(commandes, fichier, json_path):
	"""
	Permet d'importer tous les sons prétraités dans un seul fichier .json
	Cette fonction n'est plus utilisée dans les dernières versions, et n'est utile que dans le cas d'un seul et unique
	réseau de neurones différenciant toutes les commandes. Cette solution a démontré son inneficacité.
	"""
	print("Importation des fichiers d'entrainement...")
	
	dico_link_commande_label = {}
	for x in range(len(commandes)):
		dico_link_commande_label[commandes[x]] = [0 if x != i else 1 for i in range(len(commandes))]
	
	
	#dictionnaire pour storer les données
	ml_data = {	
	"input_data" : [],
	"target_data" : []}
	
	for x in commandes:
		fichiers = os.listdir("{}/{}".format(fichier, x))#Liste les fichiers du dossier mis en paramètre
		print("\n" + x + "\n")
		
		for y in fichiers:
			data, sampling_rate = librosa.load('{}/{}/{}'.format(fichier, x, y), sr = 22050)
			trimmed, index = librosa.effects.trim(data, top_db=30, frame_length=512, hop_length=64)# Coupe les parties silencieuses (inutiles)
			
			if len(trimmed) < 22050 * 4:
				trimmed = np.concatenate((trimmed, np.zeros(22050*4-len(trimmed))))
				
			if len(trimmed) == 22050 *4:
				n_fft = 2048
				hop_length = 4096
				n_mfcc = 13
				
				stft = librosa.core.stft(trimmed, hop_length = hop_length, n_fft = n_fft)
				spectrogram = np.abs(stft)
				
				log_spectrogram = librosa.amplitude_to_db(spectrogram)
				print(log_spectrogram.shape)
				
				ml_data["input_data"].append(log_spectrogram.flatten().tolist())
				ml_data["target_data"].append(dico_link_commande_label[x])
				print(y)
				
				#break
			else:
				print("Taille pas conforme")
				
	model = sklearn.decomposition.PCA(n_components=0.99)
	ml_data["input_data"] = model.fit_transform(ml_data["input_data"]).tolist()
	plt.plot(np.cumsum(model.explained_variance_ratio_))
	print(model.n_components_)
	print("Composants : {}".format(model.n_components_))
	print((len(ml_data["input_data"]), len(ml_data["input_data"][0])))
		
	with open("{}/dataset_0_{}-components.json".format(json_path, model.n_components_), "w") as fp:
		json.dump(ml_data, fp, indent = 4)
	
	return 0





def import_subgroup_sounds(commandes_1, commandes_2, fichier, json_path, num_dataset):
	"""
	Fonction important les données correspondant aux commandes qui lui sont données en deux groupes distincts
	pour pouvoir ensuite etre utilisées pou rl'entrainement du réseau de neurones correspondant
	"""
	print("Importation des fichiers d'entrainement en deux groupes...")
	
	#dictionnaire pour storer les données
	ml_data = {	
	"input_data" : [],
	"target_data" : []}
	
	ml_data = subgroup_preprocess(commandes_1, 0, ml_data, fichier)#Préprocessing du premier groupe
	ml_data = subgroup_preprocess(commandes_2, 1, ml_data, fichier)#Préprocessing du second groupe
	
	print("\nAnalyse en Composantes Principales...")
	model = sklearn.decomposition.PCA(n_components=0.99)#Création d'un modèle d'analyse en composantes principales permettant de réduire drastiquement le nombre de données tout en gardant une variance élevée (99%)
	ml_data["input_data"] = model.fit_transform(ml_data["input_data"]).tolist()#Réduction de dimensions du dataset
	
	plt.plot(np.cumsum(model.explained_variance_ratio_))
	print(model.n_components_)
	print("Composants : {}".format(model.n_components_))
	print((len(ml_data["input_data"]), len(ml_data["input_data"][0])))
	
	print("\nCreating json file...")
	with open("{}/dataset_{}_bis_{}-components.json".format(json_path, num_dataset, model.n_components_), "w") as fp:#Création d'un fichier json contenant les données traitées
		json.dump(ml_data, fp, indent = 4)
	print("File created")
	
	print("\nCreating PCA model file...")
	dump(model, "{}/PCA models/PCA_model_{}_{}-components.joblib".format(json_path, num_dataset, model.n_components_))#Création d'un fichier contenant le modèle de PCA pour pouvoir le réutiliser sur les données obtenues lors du fonctionnement en live
	return 0

def subgroup_preprocess(commandes, num, ml_data, fichier):
	"""
	Fonction s'occupant du préprocessing des données
	"""
	print("\n Group {} \n".format(num))
	for x in commandes:
		fichiers = os.listdir("{}/{}".format(fichier, x))#Liste les fichiers du dossier mis en paramètre
		print("\n" + x + "\n")
		
		for y in fichiers:
			data, sampling_rate = librosa.load('{}/{}/{}'.format(fichier, x, y), sr = 22050)
			trimmed, index = librosa.effects.trim(data, top_db=30, frame_length=512, hop_length=64)# Coupe les parties silencieuses (inutiles)
			
			if len(trimmed) < 22050 * 4:
				trimmed = np.concatenate((trimmed, np.zeros(22050*4-len(trimmed))))#Normalise la longueur des fichiers (ils doivent tous avoir le meme nombre de données, donc on ajoute des zéros pour normaliser la longueur. C'est pas très beau mais ca fonctionne bien)
				
			if len(trimmed) == 22050 *4:
				n_fft = 2048
				hop_length = 4096
				n_mfcc = 13
				stft = librosa.core.stft(trimmed, hop_length = hop_length, n_fft = n_fft) #Transformation de fourrier à cours therme, réalisant des transformations de fourrier sur des petits morceaux de l'enregistrement de taille hop_length pour obtenir une évolution des fréquences présentes dans l'enregistrement en fonction du temps
				spectrogram = np.abs(stft)#Crée un spectrogramme de ces fréquences
				
				log_spectrogram = librosa.amplitude_to_db(spectrogram)#Passe sur une échelle logarithmique semblable au fonctionnement de l'ouïe humaine
				print(log_spectrogram.shape)
				ml_data["input_data"].append(log_spectrogram.flatten().tolist())
				a = [0, 0]
				a[num] = 1
				ml_data["target_data"].append(a)#Groupe auquel appartiennent les données
				print(y)
			else:
				print("Taille pas conforme")
	return ml_data

def import_sound(file):
	"""
	Fonction important un seul fichier son spécifique et réalisant un prétraitement dessus (PCA exclue)
	pour pouvoir ensuite prédire à quelle commande il correspond grace aux réseaux de neurones.
	"""
	data, sampling_rate = librosa.load(file, sr = 22050)
	trimmed, index = librosa.effects.trim(data, top_db=30, frame_length=512, hop_length=64)# Coupe les parties silencieuses (inutiles)
	
	if len(trimmed) < 22050 * 4:
		trimmed = np.concatenate((trimmed, np.zeros(22050*4-len(trimmed))))
		
	if len(trimmed) == 22050 *4:
		n_fft = 2048
		hop_length = 4096
		n_mfcc = 13
		stft = librosa.core.stft(trimmed, hop_length = hop_length, n_fft = n_fft)
		spectrogram = np.abs(stft)
		
		log_spectrogram = librosa.amplitude_to_db(spectrogram).flatten().tolist()
		return log_spectrogram
	else:
		print("Taille pas conforme")
		return False

commandes = ["lance_la_calculatrice", "lance_la_presentation", "lance_ma_musique", "pourquoi_la_vie", "prend_un_screenshot", "quelle_heure_est_il", "raconte_une_blague"]
commandes_1 = ["pourquoi_la_vie", "raconte_une_blague"]
commandes_2 = ["quelle_heure_est_il", "prend_un_screenshot"]
fichier = "Dataset"

#Création de l'ensemble des fichiers contenant les sons prétraités ainsi que les modèles de PCA correspondant
import_subgroup_sounds(["lance_la_calculatrice", "lance_la_presentation", "lance_ma_musique"], ["pourquoi_la_vie", "prend_un_screenshot", "quelle_heure_est_il", "raconte_une_blague"], fichier, "Dataset/json", 1)
import_subgroup_sounds(["lance_ma_musique"], ["lance_la_calculatrice", "lance_la_presentation"], fichier, "Dataset/json", 2)
import_subgroup_sounds(["lance_la_calculatrice"], ["lance_la_presentation"], fichier, "Dataset/json", 3)
import_subgroup_sounds(["pourquoi_la_vie", "raconte_une_blague"], ["prend_un_screenshot", "quelle_heure_est_il"], fichier, "Dataset/json", 4)
import_subgroup_sounds(["pourquoi_la_vie"], ["raconte_une_blague"], fichier, "Dataset/json", 5)
import_subgroup_sounds(["quelle_heure_est_il"], ["prend_un_screenshot"], fichier, "Dataset/json", 6)

#import_all_sounds(commandes, fichier, "Dataset/json")
