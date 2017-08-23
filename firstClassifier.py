# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 13:31:29 2017

@author: Christian
"""
from scipy.spatial import distance
from sklearn.metrics import accuracy_score
from sklearn import datasets
from sklearn.model_selection import train_test_split

# Use euclidean algorithm to calculate distance between two points
def euc(a,b):
    return distance.euclidean(a,b)

# Create the Classifier class using the K Nearest Neighbors approach
# Only using K as 1 in this
class KNearestNeighborClassifier():
    # Fit function that sets the train data for the class
    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train
    
    # Predict function that actually does the predictions based on the set
    # training data from the fit function
    def predict(self, X_test):
        predictions = []
        for row in X_test:
            label = self.closest(row)
            predictions.append(label)
        return predictions
    
    # Calculate the closest "point" and save and return the type of object
    # Predict the testing point has the same label as the closest training point
    def closest(self, row):
        best_dist = euc(row, self.X_train[0])
        best_index = 0
        for i in range(1, len(self.X_train)):
            dist = euc(row, self.X_train[i])
            if dist < best_dist:
                best_dist = dist
                best_index = i
                return self.y_train[best_index]
            
class Main(): 
    #Load the dataset
    iris = datasets.load_iris()
    
    # Set X = features, y = label
    # Or X = collected data, y = what it is
    X = iris.data
    y = iris.target
    
    # Split the collected data in half
    # Create a training dataset and a test dataset from this
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .5)
    
    # Create the Classifier
    my_classifier = KNearestNeighborClassifier()
    
    # Train the classifier with the training dataset
    my_classifier.fit(X_train, y_train)
    
    # Use the testing dataset along with the classifier to attempt to predict the
    # label or what it is
    predictions = my_classifier.predict(X_test)
    
    # Get accuracy score of predictions
    accuracy = accuracy_score(y_test, predictions)

    print (accuracy)

# Call Main
Main()