# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 12:38:40 2017

@author: Christian
"""
# Import and load the dataset
from sklearn import datasets
iris = datasets.load_iris()

# Set X = features, y = label
# Or X = collected data, y = what it is
X = iris.data
y = iris.target

# Split the collected data in half
# Create a training dataset and a test dataset from this
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .5)

# Create the DecisionTreeClassifier
from sklearn import tree
my_classifier = tree.DecisionTreeClassifier()
#from sklearn.neighbors import KNeighborsClassifier
#my_classifier = KNeighborsClassifier()

# Train the classifier with the training dataset
my_classifier.fit(X_train, y_train)

# Use the testing dataset along with the classifier to attempt to predict the
# label or what it is
predictions = my_classifier.predict(X_test)

# Get accuracy score of predictions
from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, predictions))
