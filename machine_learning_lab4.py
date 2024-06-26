# -*- coding: utf-8 -*-
"""machine_learning_lab4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wfkrOTHKwhPsFlu8stzFx9dfLQDos7zd
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("/content/dataset2_l4.txt")
df.head()

print("{} записів, {} полів".format(*df.shape))

plt.bar(df['Class'].value_counts().index, df['Class'].value_counts())
plt.show()

from sklearn.model_selection import ShuffleSplit

ss = ShuffleSplit(n_splits=20, test_size=0.3, random_state=0)

splits = list(ss.split(df))

print("Дисбаланс вибірок:")

for i, split in enumerate(splits):
  counts = df.iloc[split[0]]['Class'].value_counts()
  proportions = counts/counts.sum()
  disbalance = proportions.max()-proportions.min()
  print(i, round(disbalance, 3))

train = df.iloc[splits[13][0]]
test = df.iloc[splits[13][1]]

X_train = train.drop(columns=['Class'])
y_train = train['Class']
X_test = test.drop(columns=['Class'])
y_test = test['Class']

# plt.bar(train['Class'].value_counts().index, df['Class'].value_counts())
# plt.show()

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score

# шукаємо найкращий параметр k

k_scores = []

for k in range(1, 20):
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X_train, y_train, cv=5, scoring='accuracy')
    print(f"k = {k}, avg_score = {round(scores.mean(), 3)}")

from sklearn.manifold import TSNE

tsne = TSNE(n_components=3, random_state=42)
X_3d = tsne.fit_transform(X_train)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
for label in y_train.unique():
    ax.scatter(X_3d[y_train == label][:, 0], X_3d[y_train == label][:, 1], X_3d[y_train == label][:, 2], label=label)
ax.set_title('3D Projection of Data using t-SNE')
ax.legend()
plt.show()

from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)

train_pred = knn.predict(X_train)
print("Classification Report for Training Data:")
print(classification_report(y_train, train_pred, zero_division=0))

test_pred = knn.predict(X_test)
print("Classification Report for Test Data:")
print(classification_report(y_test, test_pred, zero_division=0))

cm = confusion_matrix(y_test, test_pred)

plt.figure(figsize=(8, 6))
class_labels = y_train.unique()
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, xticklabels=class_labels, yticklabels=class_labels)
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()

leaf_sizes = np.arange(20, 201, 5)

train_scores = []
test_scores = []

for leaf_size in leaf_sizes:
    knn = KNeighborsClassifier(n_neighbors=5, algorithm='kd_tree', leaf_size=leaf_size)

    knn.fit(X_train, y_train)

    train_score = knn.score(X_train, y_train)
    test_score = knn.score(X_test, y_test)

    train_scores.append(train_score)
    test_scores.append(test_score)

plt.figure(figsize=(10, 6))
plt.plot(leaf_sizes, train_scores, label='Train Score')
plt.plot(leaf_sizes, test_scores, label='Test Score')
plt.xlabel('Leaf Size')
plt.ylabel('Accuracy')
plt.title('Impact of Leaf Size on Classification Accuracy')
plt.legend()
plt.grid(True)
plt.show()