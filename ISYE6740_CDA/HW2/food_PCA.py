# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse.linalg as ll
import os

path = os.path.dirname(__file__)
csv_path = os.path.join(path, 'food-consumption.csv')
food_data=pd.read_csv(csv_path)
data = np.array(food_data)

m, n = data.shape
data = data.T

# PCA
mu = np.mean(data, axis = 1)
data = data - mu
C = np.dot(data, data.T)/m
K = 2
S,W = ll.eigs(C, k = K)
S = S.real
W = W.real
dim1 = np.dot(W[:,0].T,data)/np.sqrt(S[0]) # extract the 1st principal component
dim2 = np.dot(W[:,1].T,data)/np.sqrt(S[1]) # extract the 2nd principal component




