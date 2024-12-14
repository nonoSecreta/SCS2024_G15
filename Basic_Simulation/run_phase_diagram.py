# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 16:21:19 2024

@author: Bryanz
"""
import numpy as np
from phase_diagram import PhaseDiagram
from initialize_forest import generate_forest
from plots import plotPhaseDiagram

forest_size = 100  # Sides of the forest
p_growth = 0.005  # Growth probability
p_infection = 1/(forest_size ** 2 * 10) # Infection probability
infection_time = np.arange(0, 21, 1) # Number of steps an infection lasts
p_spread = np.linspace(0.0, 0.1, len(infection_time)) # Spreading probability
# p_tree_1_growth = 1.0 # Probability of tree 1 growth for each forest
# p_tree_2_growth = 1 - p_tree_1_growth # Probability of tree 2 growth for each forest
# p_tree_1_conv_growth = 0.005
# p_tree_2_conv_growth = 0.01 - p_tree_1_conv_growth
iterations = 81 # Amount of simulation loops
relative_growth = 0.6 # Relative growth of tree 2 to tree 1 for harvest
min_age_agriculture = 45 # Minimum age of tree 1 until harvest
min_age_immune = 80 # Minimum age of tree 2 tree until harvest

wood_outcome_combined_list = []
for n in range(2):
    wood_outcome_combined_list.append(np.zeros((iterations, len(infection_time), len(p_spread), 3)))
    for i in range(3):
        
        if i == 0:
            p_tree_1_growth = 1
            p_tree_2_growth = 1 - p_tree_1_growth # Probability of tree 2 growth for each forest
            p_tree_1_conv_growth = 0.005
            p_tree_2_conv_growth = 0
        else:
            p_tree_1_growth = 0.75
            p_tree_2_growth = 1 - p_tree_1_growth # Probability of tree 2 growth for each forest
            p_tree_1_conv_growth = 0.005
            p_tree_2_conv_growth = 0.01 - p_tree_1_conv_growth
            
        forest = generate_forest(i, forest_size)
        wood_outcome_combined_list[n][:,:,:,i] = PhaseDiagram(forest, iterations, infection_time, 
                          p_growth, p_tree_1_growth, p_tree_2_growth,
                         p_tree_1_conv_growth, p_tree_2_conv_growth, p_infection, p_spread, min_age_agriculture, min_age_immune, relative_growth )
        
        print(f"Forest {i} run complete")
    

wood_outcome_combined = (wood_outcome_combined_list[0] + wood_outcome_combined_list[1]) / 2
#%%

for i in range(iterations):
    max_wood_outcome = np.max(wood_outcome_combined[i], axis=2)
    max_wood_outcome = np.expand_dims(max_wood_outcome, 2)
    max_wood_outcome = np.repeat(max_wood_outcome, 3, axis=2)
    plot_wood_outcome = (max_wood_outcome == wood_outcome_combined[i]) * 1.0
    plotPhaseDiagram(plot_wood_outcome, "Iteration: " + str(i), p_spread, infection_time, "Spreading probability", "Infection time")