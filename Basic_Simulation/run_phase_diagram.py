# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 16:21:19 2024

@author: Bryanz
"""
import numpy as np
from phase_diagram import PhaseDiagram
from initialize_forest import generate_forest
from plots import plotPhaseDiagram

forest_size = 100  #100 Sides of the forest
p_growth = 0.005  # Growth probability
p_infection = 1/(forest_size ** 2 * 20) # Infection probability
p_spread = np.linspace(0.0, 1.0, 20) # Spreading probability
p_tree_1_growth = 1.0 # Probability of tree 1 growth for each forest
p_tree_2_growth = 1 - p_tree_1_growth # Probability of tree 2 growth for each forest
p_tree_1_conv_growth = 0.005
p_tree_2_conv_growth = 0.01 - p_tree_1_conv_growth
iterations = 81 #300 Amount of simulation loops
infection_time = np.linspace(1, iterations, 20) # Number of steps an infection lasts
relative_growth = 2 # Relative growth of tree 2 to tree 1 for harvest
min_age_agriculture = 45 # Minimum age of tree 1 until harvest
min_age_immune = 80 # Minimum age of tree 2 tree until harvest

wood_outcome_combined = np.zeros((len(infection_time), len(p_spread), 3))

for i in range(3):
    forest = generate_forest(i, forest_size)
    wood_outcome_combined[:,:,i] = PhaseDiagram(forest, iterations, infection_time, 
                      p_growth, p_tree_1_growth , p_tree_2_growth,
                     p_tree_1_conv_growth, p_tree_2_conv_growth, p_infection, p_spread, min_age_agriculture, min_age_immune, relative_growth )
    
    print(f"Forest {i} run complete")

maxing = np.max(wood_outcome_combined, axis=2)
maxing = np.expand_dims(maxing, 2)
maxing = np.repeat(maxing, 3, axis=2)

plot_wood_outcome = (maxing == wood_outcome_combined) * wood_outcome_combined
plot_wood_outcome /= np.max(plot_wood_outcome)
#%%
plotPhaseDiagram(wood_outcome_combined[:, :, 0], p_spread, infection_time, "Spreading probability", "Infection time", 0, 1)
plotPhaseDiagram(wood_outcome_combined[:, :, 1], p_spread, infection_time, "Spreading probability", "Infection time", 0, 1)
plotPhaseDiagram(wood_outcome_combined[:, :, 2], p_spread, infection_time, "Spreading probability", "Infection time", 0, 1)
plotPhaseDiagram(plot_wood_outcome, p_spread, infection_time, "Spreading probability", "Infection time", 0, 1)
