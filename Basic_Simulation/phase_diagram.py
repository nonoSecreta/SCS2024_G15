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
    
    
    wood_outcome = np.zeros((len(infection_time), len(p_spread)))
    
    for i in range(len(infection_time)):
        
        for j in range(len(p_spread)):
            print("infection_time: ", i, "p_spread", j)
            temp_p_spread = p_spread[j]
            temp_infection_time = infection_time[i]
            
            temp_forest = np.copy(forest)
            age_list = np.zeros(forest.shape)
            infection_time_list = np.zeros(forest.shape)
            
            for k in range(iterations):
                   
                temp_forest, age_list, infection_time_list = TreeDeath(temp_forest, age_list, temp_infection_time, infection_time_list)
                
                # Grow trees at empty areas
                temp_forest = GrowTrees(temp_forest, p_growth, p_tree_1_growth, p_tree_2_growth)
                temp_forest = ConvGrowTrees(temp_forest, p_tree_1_conv_growth, p_tree_2_conv_growth)
                
                # Infect trees at random with given probability
                
                temp_forest[(np.random.rand(temp_forest.shape[0], temp_forest.shape[1] ) < p_infection) & (temp_forest == -1)] = 1
                
                # Spread disease from already infected trees
                temp_forest = SpreadDisease(temp_forest, age_list, temp_infection_time, temp_p_spread)
                
                # Update age
                age_list, infection_time_list = AgeCounter(age_list, infection_time_list, temp_forest)
                
            wood_outcome[i, j] = HarvestForest(temp_forest, age_list, min_age_agriculture, min_age_immune, relative_growth)
    
    return wood_outcome
