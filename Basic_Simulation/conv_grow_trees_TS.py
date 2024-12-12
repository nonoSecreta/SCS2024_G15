# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 09:14:50 2024

@author: herman
"""

import numpy as np
from scipy.signal import convolve2d

def ConvGrowTrees(forest, p_prolif1, p_prolif2):
        
    def p_matrix(forest, index, p_prolif):
    
        # Find spots where index exists in forest.
        if index == 0:
            # Index where no proliferable trees are.
            i, j = np.where((forest == 0) & (forest == -1))
        else:
            i, j = np.where(forest == index)
        
        spread_scope = 1  # scope of proliferation
        bias = 1e-10 # bias to avoid log(0) problem
        
        location_matrix = np.zeros(forest.shape)
        location_matrix[i,j] = 1
        
        # Create periodic boundary conditions with padding.
        padded_location_matrix = \
            np.pad(location_matrix, spread_scope , mode='wrap')
        
        # Execute convolution.
        kernel = np.array([[1,1,1],[1,0,1],[1,1,1]])
        p_matrix = np.log(1 - padded_location_matrix*p_prolif + bias)
        p_matrix = convolve2d(p_matrix, kernel, mode='valid')
        
        # Final probabilities.
        p_matrix = 1 - np.exp(p_matrix)

        return p_matrix
    
    # Obtain probability matrices
    p_matrix1 = p_matrix(forest, -1, p_prolif1)
    p_matrix2 = p_matrix(forest, -2, p_prolif2)
    
    def TS(p_tree1, p_tree2):
        
        # Check which index actually spreads and assign fitness thereafter:    
        r1 = np.random.rand()
        if p_tree1 >= r1:
            fitness1 = p_tree1
        else:
            fitness1 = 0
        
        r2 = np.random.rand()
        if p_tree2 >= r2:
            fitness2 = p_tree2
        else:
            fitness2 = 0
            
        # If one or two fitnesses is equal to zero do:
        if fitness1 == 0 and fitness2 == 0:
            index = 0
        elif fitness1 != 0 and fitness2 == 0:
            index = -1
        elif fitness1 == 0 and fitness2 != 0:
            index = -2
        # If both fitnesses are nonzero do tournament selection.
        else:
            p_tour = 0.85
            r = np.random.rand()
            
            if fitness1 >= fitness2:
                #top_dog = fitness1
                top_dog_index = -1
                #underdog = fitness2
                underdog_index = -2
            else:
                #top_dog = fitness2
                top_dog_index = -2
                #underdog = fitness1
                underdog_index = -1
            
            if r <= p_tour:
                index = top_dog_index
            else:
                index = underdog_index
        
        return index
    
    new_trees = np.zeros(forest.shape)
    for i in range(forest.shape[0]):
        for j in range(forest.shape[1]):
            index = TS(p_matrix1[i,j], p_matrix2[i,j])
            new_trees[i,j] = index
    
    empty_spots_i, empty_spots_j = np.where(forest == 0)
    available_spots = np.zeros(forest.shape)
    available_spots[empty_spots_i,empty_spots_j] = 1
    new_trees = new_trees*available_spots
    
    forest = forest + new_trees
    
    return forest


# # %%
# N = 100
# p_prolif1 = 0.0075
# p_prolif2 = 0.0025
# # random forest with 10% of trees infected.
# forest = np.random.choice([-2, -1, 0, 1], size=(N, N), p=[0.1, 0.35, 0.5, 0.05])
# # plot the forest
# import matplotlib.pyplot as plt
# plt.imshow(forest, cmap='viridis')
# plt.colorbar()
# plt.show()

# # %%
# while True:
#     forest = GrowTrees(forest, p_prolif1, p_prolif2)
    
#     # plot the forest
#     plt.imshow(forest, cmap='viridis')
#     plt.colorbar()
#     plt.show()
#     if np.sum(forest == 0) == 0:
#         break
