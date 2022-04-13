from sklearn.preprocessing import *
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split  # divise le dataset en train 80% et test 20%


tab= np.array( ['Chat 1','Chat 2', 'Chien', 'Oiseaux'])
print(tab)
# labelEncoder permet d'assigner un nombre à un string

label=LabelEncoder()

tabul=label.fit_transform(tab) #donne les valeurs , aux string, il faut l'affecter a une variable ici tabul

label=LabelBinarizer()
tabul=label.fit_transform(tabul)
print(tabul)


list1=np.array([['Chat','Poils'],
                ['Chien','Poils'],
                ['Chat','Poils'],
                ['Oiseaux','Plumes']])

encorder = OrdinalEncoder()
encorder.fit_transform(list1)
# premiere colonne 0 = chats, 1 = chien, 2 oiseaux, 2eme colonne, poils = 1, plumes =0

encoder = OneHotEncoder(sparse=False)
encoder.fit_transform(list1) # colonne 1 chat, colonne 2 chien, colone 3 oiseaux, colone 4 plumes et 5 poils

iris = load_iris()
X = iris.data

X_minmax = MinMaxScaler().fit_transform(X)

plt.scatter(X[:, 2], X[:, 3])
plt.scatter(X_minmax[:, 2], X_minmax[:, 3]) #plot les donnes iris

X_stdscl = StandardScaler().fit_transform(X) # sert à normaliser les donnees, change l'echelle
plt.scatter(X[:, 2], X[:, 3])
plt.scatter(X_stdscl[:, 2], X_stdscl[:, 3])

X = iris.data # variables sur lesquelles on se base pour
y = iris.target # données à prédire

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

model = make_pipeline(StandardScaler(), SGDClassifier())

model.fit(X_train, y_train)
model.score(X_test, y_test)

print(model.score(X_test,y_test))

#camis, pca, are clustering examples unsupervised learning