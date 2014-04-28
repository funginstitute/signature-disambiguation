import pandas as pd
import pylab as pl

from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.decomposition import PCA

d = pd.read_csv('signatures.csv',delimiter='\t',header=None)

estimator = KMeans(init='k-means++',n_clusters=2)
estimator.fit(d.values)
print pd.Series(estimator.labels_).value_counts()

reduced_data = PCA(n_components=2).fit_transform(d.values)
estimator = KMeans(init='k-means++',n_clusters=2)
estimator.fit(reduced_data)
print pd.Series(estimator.labels_).value_counts()

group1 = []
group2 = []
for i, label in enumerate(estimator.labels_):
    if label == 0:
        group1.append(reduced_data[i])
    else:
        group2.append(reduced_data[i])

pl.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
pl.savefig('kmeans.png')

