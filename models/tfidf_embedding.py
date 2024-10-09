import os
import json
import collections
import numpy as np
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pdb


if __name__ == "__main__":
    with open(os.path.join("/home/pxu/codes/RATuner/results/command_texts/", "command_texts.json"), 'r') as file:
        data = json.load(file)

    with open(os.path.join("/home/pxu/codes/RATuner/results/command_texts/", "synthesis_command_texts.json"), 'r') as file:
        sys_data = json.load(file)

    with open(os.path.join("/home/pxu/codes/RATuner/results/command_texts/", "floorplan_command_texts.json"), 'r') as file:
        floorplan_data = json.load(file)

    with open(os.path.join("/home/pxu/codes/RATuner/results/command_texts/", "placement_command_texts.json"), 'r') as file:
        place_data = json.load(file)

    with open(os.path.join("/home/pxu/codes/RATuner/results/command_texts/", "routing_command_texts.json"), 'r') as file:
        routing_data = json.load(file)

    corpus = [v for v in data.values()]

    tv = TfidfVectorizer()

    tv_target = tv.fit_transform(corpus)
    tv_query = tv.transform(corpus)

    print(tv_target.shape)
    print(tv_query.shape)

    embeddings_data  = collections.OrderedDict()
    embeddings_array = []

    indexes = [[], [], [], []]

    predefined_colors = ['#9dc3e7', '#5f97d2', '#9394e7', '#b1ce46', '#f1d77e', '#934b43', '#d76364']
    colors = []
    labels = []
    labels.append("Synthesis")
    labels.append("Floorplan")
    labels.append("Placement")
    labels.append("Routing")

    markers = ["o", "^", "x", "P"]
    count = 0

    for i, key in enumerate(data.keys()):
        embedding = tv_query[i, :].todense()
        embeddings_data[key] = embedding.tolist()
        embeddings_array.append(embedding.tolist())

        if key in sys_data:
            colors.append(predefined_colors[0])
            indexes[0].append(count)
        elif key in floorplan_data:
            colors.append(predefined_colors[1])
            indexes[1].append(count)
        elif key in place_data:
            colors.append(predefined_colors[2])
            indexes[2].append(count)
        else:
            colors.append(predefined_colors[3])
            indexes[3].append(count)

        count += 1

    with open('/home/pxu/codes/RATuner/results/tfidf-embeddings/command_embedding.json', 'w') as json_file:
        json.dump(embeddings_data, json_file, indent=4)

    import numpy as np
    from sklearn.manifold import TSNE

    X = np.array(tv_query.todense())
    print(X.shape)


    def find_optimal_clusters(data, max_k):
        iters = range(2, max_k+1, 2)
        
        sse = []
        for k in iters:
            sse.append(MiniBatchKMeans(n_clusters=k, init_size=1024, batch_size=2048, random_state=20).fit(data).inertia_)
            print('Fit {} clusters'.format(k))
            
        f, ax = plt.subplots(1, 1)
        ax.plot(iters, sse, marker='o')
        ax.set_xlabel('Cluster Centers')
        ax.set_xticks(iters)
        ax.set_xticklabels(iters)
        ax.set_ylabel('SSE')
        ax.set_title('SSE by Cluster Center Plot')

    find_optimal_clusters(text, 20)



    pdb.set_trace()

    tsne_model = TSNE(n_components=2, random_state=0)
    tsne_model.fit_transform(X)
    Y = tsne_model.fit_transform(X)

    print(colors)

    import matplotlib.pyplot as plt
    plt.rc('font', family='serif')
    plt.xticks([])
    plt.yticks([])

    for i in range(4):
        plt.scatter(Y[indexes[i], 0], Y[indexes[i], 1], label=labels[i], c=predefined_colors[i], marker=markers[i], cmap=plt.cm.Spectral,s=50)


    plt.legend(loc="upper right")
    plt.savefig('/home/pxu/codes/RATuner/results/tfidf-embeddings/command_embedding_tsne.pdf')

    sim_matrix = cosine_similarity(tv_query, tv_target)