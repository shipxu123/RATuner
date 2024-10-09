import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

with open('/home/pxu/codes/RATuner/results/rag-embeddings/command_embedding.json', 'r') as json_file:
    data = json.load(json_file)

# Print the data
print(data.keys())

def find_optimal_clusters(data, max_k):
    iters = range(2, max_k+1, 2)
    
    sse = []
    for k in iters:
        sse.append(MiniBatchKMeans(n_clusters=k, init_size=128, batch_size=128, random_state=20).fit(data).inertia_)
        print('Fit {} clusters'.format(k))
        
    f, ax = plt.subplots(1, 1)
    ax.plot(iters, sse, marker='o')
    ax.set_xlabel('Cluster Centers')
    ax.set_xticks(iters)
    ax.set_xticklabels(iters)
    ax.set_ylabel('SSE')
    ax.set_title('SSE by Cluster Center Plot')

    plt.legend(loc="upper right")
    plt.savefig('/home/pxu/codes/RATuner/results/rag-embeddings/k-Means-plotting.pdf')

N = len(data.keys())
print(N)


text = np.array([v for v in data.values()])
text = text.reshape(N, -1)

import pdb
pdb.set_trace()

find_optimal_clusters(text, 20)
clusters = MiniBatchKMeans(n_clusters=10, init_size=N, batch_size=128, random_state=20).fit_predict(text)

def plot_tsne_pca(data, labels):
    max_label = max(labels)
    max_items = np.random.choice(range(data.shape[0]), size=N, replace=False)

    pca = PCA(n_components=2).fit_transform(data[max_items,:])
    tsne = TSNE().fit_transform(PCA(n_components=50).fit_transform(data[max_items,:]))

    idx = np.random.choice(range(pca.shape[0]), size=N, replace=False)
    label_subset = labels[max_items]
    label_subset = [cm.hsv(i/max_label) for i in label_subset[idx]]
    
    f, ax = plt.subplots(1, 2, figsize=(14, 6))
    
    ax[0].scatter(pca[idx, 0], pca[idx, 1], c=label_subset)
    ax[0].set_title('PCA Cluster Plot')
    
    ax[1].scatter(tsne[idx, 0], tsne[idx, 1], c=label_subset)
    ax[1].set_title('TSNE Cluster Plot')
    # plt.legend(loc="upper right")
    plt.savefig('/home/pxu/codes/RATuner/results/rag-embeddings/k-Means-clustering.pdf')

plot_tsne_pca(text, clusters)

cluster_data = {}

for k, c in zip(data.keys(), clusters):
    print(k, c)
    cluster_data[k] = int(c)

print(clusters)
with open('/home/pxu/codes/RATuner/results/rag-embeddings/cluster.json', 'w') as json_file:
    json.dump(cluster_data, json_file, indent=4)