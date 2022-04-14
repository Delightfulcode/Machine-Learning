import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn
from sklearn.linear_model import *
from sklearn.neighbors import KNeighborsClassifier

"First part linear regression"
#predict a line that goes through majority of points

m = 100
x = np.linspace(0,10,100)
x = x.reshape(100,1)  # 100 lignes et 1 colonnes
print (x)

y = x+np.random.rand(100,1)
plt.scatter(x,y, color='red')
#plt.show()

#Creer un instance

model= LinearRegression().fit(x,y) # proper syntax, learns the fit with y
score = model.score(x,y) # put the score of the learned model

print(score)

plt.plot(x,model.predict(x), color='blue') # create the fitting line, that has been predicted

#plt.show()

"Second part Classification problems, K Clustering"

df = pd.read_excel('titanic.xls')

df.head()

df1= df[['pclass','survived','sex','age']]

df1['sex'].replace(['female','male'],[0,1], inplace=True) # pas d'affectation df1=df1['sex'].....

model = KNeighborsClassifier()
df1.dropna(axis=0, inplace=True)

y1=df1['survived']
x1=df1.drop('survived',axis=1)

model.fit(x1, y1)
model.score(x1, y1) # impossible to plot with scatter or plot because too many variables

# Here we're trying to predict the survival rate by selecting variables
def survie(model, pclass=1, sex=0, age=34):
    x = np.array([pclass, sex, age]).reshape(1, 3) # 1 ligne , 3 colonne
    print(model.predict(x)) # predicts whether survived or not
    print(model.predict_proba(x)) # probability of surviving
survie(model)

#[[Dying, survivin]]