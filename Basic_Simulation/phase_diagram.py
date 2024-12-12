import numpy as np
import matplotlib.pyplot as plt
from grow_trees import GrowTrees
from conv_disease_spread import SpreadDisease
from harvest_forest import HarvestForest
from update_age import AgeCounter
from initialize_forest import generate_forest
from tree_death import TreeDeath
from sustainability_check import SustainabilityCheck
from plots import plotForestData
from conv_grow_trees_TS import ConvGrowTrees

def PhaseDiagram(forest, iterations, infection_time, 
                  p_growth, p_tree_1_growth , p_tree_2_growth,
                 p_tree_1_conv_growth, p_tree_2_conv_growth, p_infection, p_spread, min_age_agriculture, min_age_immune, relative_growth ):
    
    
    age_list = np.zeros(forest.shape)
    infection_time_list = np.zeros(forest.shape)
    wood_outcome = np.zeros((len(infection_time), len(p_spread)))
            
    
    for i in range(len(infection_time)):
        
        for j in range(len(p_spread)):
            temp_p_spread = p_spread[j]
            temp_infection_time = infection_time[i]
                        
            
            for k in range(iterations):
                   
                forest, age_list, infection_time_list = TreeDeath(forest, age_list, temp_infection_time, infection_time_list)
                
                # Grow trees at empty areas
                forest = GrowTrees(forest, p_growth, p_tree_1_growth, p_tree_2_growth)
                forest = ConvGrowTrees(forest, p_tree_1_conv_growth, p_tree_2_conv_growth)
                
                # Infect trees at random with given probability
                
                forest[(np.random.rand(forest.shape[0], forest.shape[1] ) < p_infection) & (forest == -1)] = 1
                
                # Spread disease from already infected trees
                
                forest = SpreadDisease(forest, age_list, temp_infection_time, temp_p_spread)
                              
                # Update age
                age_list, infection_time_list = AgeCounter(age_list, infection_time_list, forest)
                
            wood_outcome[i, j] = HarvestForest(forest, age_list, min_age_agriculture, min_age_immune, relative_growth)
    
    return wood_outcome
