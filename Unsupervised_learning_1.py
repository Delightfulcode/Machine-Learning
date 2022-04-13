import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import *
from sklearn.cluster import *
from sklearn.ensemble import IsolationForest


#K means clustering unsupervised
x,y = make_blobs(n_samples=100, centers=3, cluster_std=0.4, random_state=0)
plt.scatter (x[:,0],x[:,1])

plt.title('Training...')

plt.grid(True)

plt.show()
#points vont etre attribué au centre les plus proche, et recalcule les distance, jusqu'a atteindre un etat de stabilisation

model = KMeans(n_clusters=3)
model.fit(x)
model.predict(x)
plt.scatter(x[:,0], x[:,1], c=model.predict(x))
plt.scatter(model.cluster_centers_[:,0], model.cluster_centers_[:,1], c='r')
model.score(x)
plt.show()


X, Y = make_blobs(n_samples=50, centers=1, cluster_std=0.1, random_state=0)
X[-1,:] = np.array([2.25, 5])

plt.scatter(X[:,0], X[:, 1])

plt.show()

#outliners, detection d'anomalie
model=IsolationForest(contamination=0.01) #trains the model, isolate one part of the model and highlights it

model.fit(X)

plt.scatter(X[:,0], X[:, 1], c=model.predict(X))

plt.show()