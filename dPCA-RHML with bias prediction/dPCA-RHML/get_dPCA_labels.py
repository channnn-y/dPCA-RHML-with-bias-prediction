#you can run this script in jupyter notebook
from pensa import *
import numpy as np
import mdtraj as md
import sys
import numpy as np
import matplotlib.pyplot as plt
import pyemma
from pyemma.util.contexts import settings
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import find_cent


# get get-dPCA
rec_cos = get_structure_features('./your_struct.pdb','./your_traj.nc',cossin=True)
rec_cos_feat, rec_cos_data = rec_cos
#print(len(rec_cos_data['bb-torsions']))
#
bb_torsion_pca = calculate_pca(rec_cos_data['bb-torsions']) 


#get the first 3PCs and save as *.dat file
name = '3PC'
pca_PC3 = []
for i in range(3):
    pca = project_on_pc(rec_cos_data['bb-torsions'],i,pca=bb_torsion_pca)
    if pca_PC3 == []:
        pca_PC3 = pca
    else:
        pca_PC3 = np.column_stack((pca_PC3,pca))
print(pca_PC3.shape)
#print(pca_PC30:2,:])
np.savetxt(name+".dat",pca_PC3)


name = '3PC'
pca_PC3 = np.loadtxt(name+".dat")
Y1 =[]
Y2 =[]
Y3 = []
for i in range(2,10):
    n=str(i)
    kmeans_all = KMeans(n_clusters=i,random_state=0).fit(pca_PC3)
    kmeans_all_labels = kmeans_all.labels_
    centroids = kmeans_all.cluster_centers_
    #write centers and labels
    y_pred_all = kmeans_all.predict(pca_PC3)
    np.save(name+'/Kmeans_'+name+'_cluster'+n,y_pred_all)
    cents_all = find_cent.find_c(centroids,pca_PC3)
    #np.savetxt(name + '/Kmeans_' + name + '_cluster' + n + '.txt', cents_all)
    data_to_save = []
    for cent in cents_all:
        index = np.where((pca_PC3 == cent).all(axis=1))[0]
        cent_label = y_pred_all[index]
        values = pca_PC3[index]

        # to string
        for j in range(len(index)):
            line = f"label: {cent_label[j]}, index: {index[j]}, PCS: {values[j]}"
            data_to_save.append(line)

    # save labels
    new_file_path = name + '/Kmeans_' + name + '_cluster' + n + '.txt'
    with open(new_file_path, 'w') as file:
        for line in data_to_save:
            file.write(line + '\n')
    #silhouette_avg = silhouette_score(pca_PC3,kmeans_all_labels)
    dbi = davies_bouldin_score(pca_PC3,kmeans_all_labels)
    calinski_harabasz_scores = calinski_harabasz_score(pca_PC3,kmeans_all_labels)
    overall_mean = np.mean(pca_PC3,axis=0)
    SST = np.sum((pca_PC3-overall_mean)**2)
    SSR = np.sum([len(pca_PC3[kmeans_all_labels==l])*np.sum((centroids[l]-overall_mean)**2) for l in range(centroids.shape[0])])
    SSRSSTratio = SSR/ SST if SST !=0 else 0
    Y1.append(dbi)
    Y2.append(calinski_harabasz_scores) 
    Y3.append(SSRSSTratio)

all_list = [Y1 , Y2 ,Y3]
print(all_list)
df = pd.DataFrame(all_list,index=['DBI','pSF','SSR/SST'])
df.to_csv('clsuter_indices_'+name+'.csv')