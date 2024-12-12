# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 16:21:19 2024

@author: Bryanz
"""
from phase_diagram import PhaseDiagram
from initialize_forest import generate_forest
from plots import plotPhaseDiagram


forest_size = 50  #100 Sides of the forest
p_growth = 0.005  # Growth probability
p_infection = 1/(forest_size ** 2 * 20) # Infection probability
p_spread = [0.01, 0.02, 0.03, 0.005] # Spreading probability
p_tree_1_growth = 1.0 # Probability of tree 1 growth for each forest
p_tree_2_growth = 1 - p_tree_1_growth # Probability of tree 2 growth for each forest
p_tree_1_conv_growth = 0.005
p_tree_2_conv_growth = 0.01 - p_tree_1_conv_growth
infection_time = [10, 20, 30, 10] # Number of steps an infection lasts
iterations = 50 #300 Amount of simulation loops
relative_growth = 2 # Relative growth of tree 2 to tree 1 for harvest
min_age_agriculture = 45 # Minimum age of tree 1 until harvest
min_age_immune = 80 # Minimum age of tree 2 tree until harvest

forest = generate_forest(0, forest_size)

wood_outcome = PhaseDiagram(forest, iterations, infection_time, 
                  p_growth, p_tree_1_growth , p_tree_2_growth,
                 p_tree_1_conv_growth, p_tree_2_conv_growth, p_infection, p_spread, min_age_agriculture, min_age_immune, relative_growth )
    
plotPhaseDiagram(wood_outcome)