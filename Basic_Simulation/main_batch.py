#%%
import numpy as np
import matplotlib.pyplot as plt
from grow_trees import GrowTrees
from conv_disease_spread import SpreadDisease
from harvest_forest import HarvestForest
from update_age import AgeCounter
from initialize_forest import generate_forest
from tree_death import TreeDeath
from sustainability_check import SustainabilityCheck
from plots import plotForestBatchData
from conv_grow_trees_TS import ConvGrowTrees

# Simulation parameters
forest_size = 100  # Sides of the forest
p_growth = 0.005  # Growth probability
p_infection = 1/(forest_size ** 2 * 20) # Infection probability
p_spread = 0.01 # Spreading probability
p_tree_1_growth = np.array([1.0, 1.0, 1.0]) # Probability of tree 1 growth for each forest
p_tree_2_growth = 1 - p_tree_1_growth # Probability of tree 2 growth for each forest
p_tree_1_conv_growth = np.array([0.005, 0.005, 0.005])
p_tree_2_conv_growth = 0.01 - p_tree_1_conv_growth
infection_time = 10 # Number of steps an infection lasts
iterations = 300 # Amount of simulation loops
relative_growth = 2 # Relative growth of tree 2 to tree 1 for harvest
min_age_agriculture = 45 # Minimum age of tree 1 until harvest
min_age_immune = 80 # Minimum age of tree 2 tree until harvest

grow_trees = True
infect_trees = True
spread_disease = True
harvest_forest = True

plot_forest = True
iterations_to_plots = 5
plot_wood_outcome = True
plot_infected_amount = True
plot_sustainability = True
plot_tree_amount = True
plot_empty_areas = True

# Initialize lists for batch run.
batch_size = 5 
wood_outcome = np.zeros((batch_size, iterations))
infected_amount = np.zeros((batch_size, iterations))
sustainability = np.zeros((batch_size, iterations))
amount_tree_agriculture = np.zeros((batch_size, iterations))
amount_tree_immune = np.zeros((batch_size, iterations))
amount_empty_areas = np.zeros((batch_size, iterations))

# Choose forest to be generated: 0, 1 or 2.
forest_type = 0
for i in range(batch_size):
    forest = generate_forest(forest_type, forest_size)
    age_list = np.zeros([forest_size, forest_size]) # Initial ages
    infection_time_list = np.zeros([forest_size, forest_size]) # Initial infection times
    
    print("Batch number:", i, "initializes with", np.sum(forest == -1), "type 1 trees and", np.sum(forest == -2), "type 2 trees.", np.sum(forest == -2) / (forest_size ** 2))
    
    
    for j in range(iterations):
        
        # Plot the forest
        if (plot_forest):
            if (iterations_to_plots > 0):
                if (j % iterations_to_plots == 0):
                    plt.matshow(forest, vmin=-2, vmax=1)
                    plt.show()
        
        amount_tree_agriculture[i, j] = np.sum(forest == -1)
        amount_tree_immune[i, j] = np.sum(forest == -2)
        amount_empty_areas[i, j] = np.sum(forest == 0) / np.sum(forest == -1)
        infected_amount[i, j] = np.sum(forest == 1) / (np.sum(forest == -1) + np.sum(forest == 1))
        
        forest, age_list, infection_time_list = TreeDeath(forest, age_list, infection_time, infection_time_list)
        
        # Grow trees at empty areas
        if (grow_trees):
            forest = GrowTrees(forest, p_growth, p_tree_1_growth[i], p_tree_2_growth[i])
            forest = ConvGrowTrees(forest, p_tree_1_conv_growth[i], p_tree_2_conv_growth[i])
        
        # Infect trees at random with given probability
        if (infect_trees):
            forest[(np.random.rand(forest_size, forest_size) < p_infection) & (forest == -1)] = 1
        
        # Spread disease from already infected trees
        if (spread_disease):
            forest = SpreadDisease(forest, age_list, infection_time, p_spread)
        
        # Get wood outcome from harvest
        if (harvest_forest):
            wood_outcome[i, j] = HarvestForest(forest, age_list, min_age_agriculture, min_age_immune, relative_growth)
            sustainability[i, j] = SustainabilityCheck(forest, age_list, min_age_agriculture, min_age_immune)
        
        # Update age
        age_list, infection_time_list = AgeCounter(age_list, infection_time_list, forest)

# Plot raw data.
if (plot_wood_outcome):
    plotForestBatchData(wood_outcome, "Iterations", "Wood outcome", [min_age_agriculture, min_age_immune], None, ["Min age agriculture", "Min age immune"], "Wood Outcome")

if (plot_infected_amount):
    plotForestBatchData(infected_amount, "Iterations", "Amount of infected trees", "Infected Amount")

if (plot_empty_areas):
    plotForestBatchData(amount_empty_areas, "Iterations", "Amount of empty areas", "Amount of Empty Areas")

if (plot_sustainability):
    plotForestBatchData(sustainability, "Iterations", "Non harvestable trees / total amount of trees", "Sustainablility")

if (plot_tree_amount):
    plotForestBatchData(amount_tree_agriculture, "Iterations", "Amount of agricultural trees", "Amount of Agriculture Trees")
    plotForestBatchData(amount_tree_immune, "Iterations", "Amount of immune trees", "Amount of Immune Trees")
    
# Calculate averages.
wood_outcome_avg = np.mean(wood_outcome, axis=0)
infected_amount_avg = np.mean(infected_amount, axis=0)
amount_empty_areas_avg = np.mean(amount_empty_areas, axis=0)
sustainability_avg = np.mean(sustainability, axis=0)
amount_tree_agriculture_avg = np.mean(amount_tree_agriculture, axis=0)
amount_tree_immune_avg = np.mean(amount_tree_immune, axis=0)

# Plot averages.
if (plot_wood_outcome):
    plotForestBatchData(wood_outcome_avg, "Iterations", "Wood outcome", [min_age_agriculture, min_age_immune], None, ["Min age agriculture", "Min age immune"], "Wood Outcome")

if (plot_infected_amount):
    plotForestBatchData(infected_amount_avg, "Iterations", "Amount of infected trees", "Infected Amount")

if (plot_empty_areas):
    plotForestBatchData(amount_empty_areas_avg, "Iterations", "Amount of empty areas", "Amount of Empty Areas")

if (plot_sustainability):
    plotForestBatchData(sustainability_avg, "Iterations", "Non harvestable trees / total amount of trees", "Sustainablility")

if (plot_tree_amount):
    plotForestBatchData(amount_tree_agriculture_avg, "Iterations", "Amount of agricultural trees", "Amount of Agriculture Trees")
    plotForestBatchData(amount_tree_immune_avg, "Iterations", "Amount of immune trees", "Amount of Immune Trees")

