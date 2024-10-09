import os
import json
import collections
from FlagEmbedding import FlagModel

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


model = FlagModel('./RAG-text-embedding-model', 
                  query_instruction_for_retrieval="为这个句子生成表示以用于检索相关文章：",
                  use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation

print(data)

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
for key, text in data.items():

    embedding = model.encode(text)
    embeddings_data[key] = embedding.tolist()
    embeddings_array.append(embedding)

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

import numpy as np
from sklearn.manifold import TSNE

X = np.array(embeddings_array)
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
plt.savefig('/home/pxu/codes/RATuner/results/embeddings/command_embedding_tsne.pdf')