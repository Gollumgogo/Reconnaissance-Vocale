##############
#IMPORTATIONS#
##############

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras import backend
from keras.models import load_model
import json
import numpy as np
import librosa
import sklearn
from joblib import dump, load

#########################
#IMPORTATION DES MODELES#
#########################

def load_PCA_models(path, PCA_names):
	list_models = [0]
	for x in PCA_names:
		list_models.append(load("{}/{}".format(path, x)))
	return list_models
	
def import_NN(NN_names):
	models = []
	for x in NN_names:
		models.append(load_model(x))
		models[-1].summary()
	return models


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
		
		log_spectrogram = librosa.amplitude_to_db(spectrogram)
		return log_spectrogram
	else:
		print("Taille pas conforme")
		return False

def class_sound(sound, models, list_PCA_models):
	"""
	Fonction classant les sons dans la catégorie que les réseaux de neurones pensent qu'ils correspondent.
	C'est un enchainement de if/else formant un arbre de décision, avec un neural network dirigeant l'enregistrement à chaque noeud jusqu'à trouver une catégorie.
	"""
	result = ""
	sound_1 = list_PCA_models[1].transform([sound.flatten()])
	print(np.array(sound).shape)
	
	predicted_value = models[1].predict_classes(sound_1)
	print(predicted_value)
	if predicted_value == 0:
		sound_2 = list_PCA_models[2].transform([sound.flatten()])
		print(np.array(sound).shape)
	
		predicted_value = models[2].predict_classes(sound_2)
		print(predicted_value)
		
		if predicted_value == 0:
			result = "lance_ma_musique"
		else:
			sound_3 = list_PCA_models[3].transform([sound.flatten()])
			print(np.array(sound).shape)
			
			predicted_value = models[3].predict_classes(sound_3)
			print(predicted_value)
			if predicted_value == 0:
				result = "lance_la_calculatrice"
			else:
				result = "lance_la_presentation"
	else:
		sound_4 = list_PCA_models[4].transform([sound.flatten()])
		print(np.array(sound).shape)
		
		predicted_value = models[4].predict_classes(sound_4)
		print(predicted_value)
		
		if predicted_value == 0:
			sound_5 = list_PCA_models[5].transform([sound.flatten()])
			print(np.array(sound).shape)
			
			predicted_value = models[5].predict_classes(sound_5)
			print(predicted_value)
			if predicted_value == 0:
				result = "pourquoi_la_vie"
			else:
				result = "raconte_une_blague"
		else:
			sound_6 = list_PCA_models[6].transform([sound.flatten()])
			print(np.array(sound).shape)
			
			predicted_value = models[6].predict_classes(sound_6)
			print(predicted_value)
			if predicted_value == 0:
				result = "quelle_heure_est_il"
			else:
				result = "prend_un_screenshot"
		
	return result
