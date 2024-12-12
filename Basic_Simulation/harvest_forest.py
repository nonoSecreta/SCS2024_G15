# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 08:21:52 2024

@author: marike
"""

import numpy as np

def HarvestForest(forest, age_list, min_age_agriculture, min_age_immune=100, relative_growing=0, annual_growth=0.015):
    """
    Function to simulate the harvest of the forest.
    
    Parameters
    ==========
    forest : 2-dimensional array NxN of tree states
    ageList: 2-dimensional array NxN of time counter for states
    minAgeAgriculture: minimum age for harvest of agricultur species -1 
    minAgeImmune: minimum age for harvest of immune species -1 
    relativeGrowing: assume wood value of agriculture tree as 1 per age of tree
                     and set value of immune tree as relative growing
    annual_growth: set annual volume growth for linear approximation and single tree
                    with units m^3/year
    """

    age_of_healthy_trees = age_list[forest==-1]
    age_of_immune_trees  = age_list[forest==-2]

    wood_agriculture = annual_growth * np.sum(age_of_healthy_trees[age_of_healthy_trees>min_age_agriculture])

    if relative_growing!=0:
        wood_immune_tree = annual_growth* np.sum(age_of_immune_trees[age_of_immune_trees>min_age_immune])
        wood_immune_tree = relative_growing * wood_immune_tree
        wood_outcome = wood_agriculture + wood_immune_tree
    else:
        wood_outcome = wood_agriculture

    return wood_outcome

# inittialize variables for testing
# forest_size = 64  # Sides of the forest.
# relative_growth = 0.4
# min_age_agriculture = 25
# min_age_immune = 50
# forest = np.random.randint(-2,2,(forest_size,forest_size))
# ageList = np.random.randint(20,100,(forest_size,forest_size))

# wood_outcome = HarvestForest(forest, ageList, min_age_agriculture, min_age_immune, relative_growth)
# print(wood_outcome)
