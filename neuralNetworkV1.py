# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 22:35:19 2017

@author: Christian
"""

import numpy as np

# Sigmoid function - Turns a number into a probability

def nonlin(x, deriv=False):
    if(deriv==True):
        return (x*(1-x))
    
    return  1/(1+np.exp(-x))

# Input data
x = np.array([[0,0,1],
             [0,1,1],
             [1,0,1],
             [1,1,1]])

# Output data
y = np.array([[0], 
             [1], 
             [1], 
             [0]])
    
    
# Seed
np.random.seed(1)

# Create synapses (weights)
# 3x4 matrix with a bias=1
syn0 = 2*np.random.random((3,4)) - 1

# 4x1 matrix witha bias=1
syn1 = 2*np.random.random((4,1)) - 1

# Training
for j in range(60000):
    
    # Layers
    # .dot = matrix multiplication
    # .T = transpose or flip matrix
    l0 = x
    l1 = nonlin(np.dot(l0,syn0))
    l2 = nonlin(np.dot(l1,syn1))
    
    # Backpropagation
    l2_error = y - l2
    if(j % 10000) == 0:
        print('Error: ' + str(np.mean(np.abs(l2_error))) )
        
    l2_delta = l2_error*nonlin(l2, deriv=True)
    
    l1_error = l2_delta.dot(syn1.T)
    
    l1_delta = l1_error * nonlin(l1, deriv=True)
    
    # Update Synapses (Weights)
    
    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)
    
print("Output after training")
print(l2)