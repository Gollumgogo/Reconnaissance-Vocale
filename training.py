
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
import datetime
import time

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras import backend
from keras import callbacks

##############################################
#IMPORTATION ET TRAITEMENT DES FICHIERS AUDIO#
##############################################

def load_data(dataset_path):
	"""
	Fonction chargeant les données préalablement traitées et placées dans des fichiers json
	"""
	print("Loading data...")
	input_data = []
	target_data = []
	with open("{}/{}.json".format(dataset_path, "dataset_6_bis_574-components"), "r") as fp:#Mettre le nom du dataset correspondant au NN que l'on souhaite entrainer
		data = json.load(fp)
	input_data += data["input_data"]
	target_data += data["target_data"]
	
	#Transforme les données en array numpy pour etre utilisées dans l'entrainement
	input_data = np.array(input_data)
	target_data = np.array(target_data)
	print("Input_data.shape : {}\nTraget_data.shape : {}".format(input_data.shape, target_data.shape))
	return input_data, target_data
	
################################
#CONSTRUCTION DU NEURAL NETWORK#
################################

def create_nn(input_data_shape):
	print("Construction du neural network")

	num_labels = 2 #Le nombre de catégories de commandes
	nbr_layers = int(input("(Recommande : 3 layers de 64 neurones chacunes)\nNbr layers : "))#Recommandé : 3 layers de 64 neurones chacunes
	layers = [int(input("Layer {} : ".format(i))) for i in range(nbr_layers)]
	# build model
	model = Sequential()#Création du neural network
	model.add(Dense(layers[0], input_shape=(input_data_shape,)))#Ajoute une couche de neurones
	model.add(Activation('relu')) #La fonction d'activation ReLU remplace juste les valeurs négatives par 0
	
	#64, 64, 64 fonctionne bien
	for x in layers[1:]:
		model.add(Dense(x))
		model.add(Activation('relu'))
		
	model.add(Dropout(0.5))#Evite/limite le surentrainement : "Dropout consists in randomly setting a fraction of input units to 0 at each update during training time, which helps prevent overfitting."
	model.add(Dense(num_labels))
	model.add(Activation('softmax'))#Softmax donne une répartition de probabilités entre chaque sortie possible
	backend.set_epsilon(1e-7)#Permet d'éviter des divisions par 0 (qui rendent un modèle instantanément inutilisable) en mettant une valeur minimale pour les calculs effectué pour obtenir le loss (déja compris dans l'optimizer)
	
	model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
	#'metrics=['accuracy']' est la facon selon laquelle on mesure l'efficacité du NN
	#L'optimizer adam permet de mettre des valeurs par défault de plein de paramètres connues pour bien fonctionner. Ca évite de se tromper en mettant de mauvaises valeurs manuellement

	print("Construction finie")
	return model, layers

####################
#ENTRAINEMENT DU NN#
####################

commandes = ["lance_la_calculatrice", "lance_la_presentation", "lance_ma_musique", "pourquoi_la_vie", "prend_un_screenshot", "quelle_heure_est_il", "raconte_une_blague"]
fichier = "Dataset"

input_data, target_data = load_data("Dataset/json")#Charge les données préalablement enregistrées sous forme de fichiers json

inpt = "y"
numero_du_nn = 6#Place du neural network dans l'arbre qui constitue l'IA finale. Chaque neural network sépare les données qui lui ont été données en deux groupes:
#Numéro | Groupe 0																	| Groupe 1
#1		|["lance_la_calculatrice", "lance_la_presentation", "lance_ma_musique"], 	["pourquoi_la_vie", "prend_un_screenshot", "quelle_heure_est_il", "raconte_une_blague"]
#2		|["lance_ma_musique"], 														["lance_la_calculatrice", "lance_la_presentation"]
#3		|["lance_la_calculatrice"], 												["lance_la_presentation"]
#4		|["pourquoi_la_vie", "raconte_une_blague"], 								["prend_un_screenshot", "quelle_heure_est_il"]
#5		|["pourquoi_la_vie"], 														["raconte_une_blague"]
#6		|["quelle_heure_est_il"], 													["prend_un_screenshot"]

while inpt == "y":

	model, layers = create_nn(input_data.shape[1])#Crée le modèle

	print("Entrainement du réseau...")

	batch_size = int(input("(Recommande : 16) Batch_size : "))#taille de chaque batch d'entrainement
	epochs = int(input("(Recommande : 100) Epochs : ")) #Nombre d'itérations d'entrainement
	verbose = 1 #Affichage de l'avancement de l'entrainement; 0 = rien, 1 = barre de chargement, 2 = une ligne par batch
	validation_split = float(input("Val split : ")) #Part des données utiliser pour tester les capacités du NN, pas utilisées lors de l'entrainement
	time_ = time.time()
	my_callbacks = [callbacks.EarlyStopping(monitor="val_acc", patience=15, min_delta = 0, mode="max", restore_best_weights = True),#Arrete l'entrainemet si val_loss ne s'améliore pas après 15 epochs
					callbacks.ModelCheckpoint("Models/{}/Model_{}".format(numero_du_nn, time_), monitor='val_acc', verbose=1, save_best_only=True, mode='max')] #Enregistre la version de l'IA avec le plus haut pourcentage de réussite sur des valeurs jamais rencontrées
	
	H = model.fit(input_data, target_data, batch_size=batch_size, epochs = epochs, verbose = verbose, validation_split = validation_split, callbacks = my_callbacks)#Entrainement 
	
	print("Entrainement terminé")
	
	#Affichage d'un graphique montrant l'évolution des valeurs. Loss et val loss doivent tendre vers 0, tandis que acc et val_acc doivent tendre vers 1
	N = np.arange(0, len(H.history["loss"]))
	plt.style.use("ggplot")
	plt.plot(N, H.history["loss"], label="train_loss")
	plt.plot(N, H.history["val_loss"], label="val_loss")
	plt.plot(N, H.history["acc"], label="train_acc")
	plt.plot(N, H.history["val_acc"], label="val_acc")
	plt.title("Training Loss and Accuracy (Simple NN)")
	plt.xlabel("Epoch #")
	plt.ylabel("Loss/Accuracy")
	plt.legend()
	plt.show()
	
	#Donne un nom contenant toutes les informations nescessaires au sujet du Neural Network pour pouvoir ensuite choisir le meilleur et le réutiliser
	os.rename(r"Models/{}/Model_{}".format(numero_du_nn, time_), r"Models/{}/Model_val_acc-{}%_shape-{}_inptshape-{}_date-{} {}".format(numero_du_nn, round(max(H.history["val_acc"])*100, 2), layers, input_data.shape[1], datetime.date.today(), round(time.time())))
	
	inpt = input("Continuer? (y/n) : ")
	backend.clear_session()#Nettoie les données enregistrées par keras pour pouvoir créer le prochain réseau de neurones à partir de 0
