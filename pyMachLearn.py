# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 11:43:02 2017

@author: Christian
"""

from sklearn import tree
features = [[140,1],[130,1],[150,0],[170,0]]
labels =[0,0,1,1]
clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, labels)
print(clf.predict([[160,0]]))