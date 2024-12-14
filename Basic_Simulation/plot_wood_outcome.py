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
from plots import plotForestData
from conv_grow_trees_TS import ConvGrowTrees

# Simulation parameters
forest_size = 100  # Sides of the forest
p_growth = 0.005  # Growth probability
p_infection = 1/(forest_size ** 2 * 10) # Infection probability
p_spread = 0.04 # Spreading probability
#p_tree_1_growth = np.array([1.0, 1.0, 1.0]) # Probability of tree 1 growth for each forest
#p_tree_2_growth = 1 - p_tree_1_growth # Probability of tree 2 growth for each forest
#p_tree_1_conv_growth = np.array([0.005, 0.005, 0.005])
#p_tree_2_conv_growth = 0.01 - p_tree_1_conv_growth
infection_time = 10 # Number of steps an infection lasts
iterations = 300 # Amount of simulation loops
relative_growth = 0.6 # Relative growth of tree 2 to tree 1 for harvest
min_age_agriculture = 45 # Minimum age of tree 1 until harvest
min_age_immune = 80 # Minimum age of tree 2 tree until harvest

grow_trees = True
infect_trees = True
spread_disease = True
harvest_forest = True

plot_forest = True
iterations_to_plots = 500
plot_wood_outcome = True
plot_infected_amount = False
plot_sustainability = False
plot_tree_amount = False
plot_empty_areas = False

# Initialize lists for batch run.
batch_size = 300
wood_outcome = np.zeros((batch_size, iterations))
wood_outcome_avg = np.zeros((3, iterations))

def InitializeInfection(forest):
    infected = False
    while(not infected):
        x = np.random.randint(0, forest.shape[1])
        y = np.random.randint(0, forest.shape[0])
        
        if (forest[y, x] == -1):
            forest[y, x] = 1
            infected = True
    return forest

for forest_type in range(3):

    if forest_type == 0:
        p_tree_1_growth = 1
        p_tree_2_growth = 1 - p_tree_1_growth # Probability of tree 2 growth for each forest
        p_tree_1_conv_growth = 0.005
        p_tree_2_conv_growth = 0
    else:
        p_tree_1_growth = 0.75
        p_tree_2_growth = 1 - p_tree_1_growth # Probability of tree 2 growth for each forest
        p_tree_1_conv_growth = 0.005
        p_tree_2_conv_growth = 0.01 - p_tree_1_conv_growth

    for i in range(batch_size):
        forest = generate_forest(forest_type, forest_size)
        age_list = np.zeros([forest_size, forest_size]) # Initial ages
        infection_time_list = np.zeros([forest_size, forest_size]) # Initial infection times

        print("Forest type:",forest_type," Batch number:", i)

        for j in range(iterations):

            # Plot the forest
            if (plot_forest):
                if (iterations_to_plots > 0):
                    if (j % iterations_to_plots == 0):
                        plt.matshow(forest, vmin=-2, vmax=1)
                        plt.show()

            forest, age_list, infection_time_list = TreeDeath(forest, age_list, infection_time, infection_time_list)

            # Grow trees at empty areas
            if (grow_trees):
                forest = GrowTrees(forest, p_growth, p_tree_1_growth, p_tree_2_growth)
                forest = ConvGrowTrees(forest, p_tree_1_conv_growth, p_tree_2_conv_growth)

            # Infect trees at random with given probability
            if (infect_trees):
                if j == 0:
                    forest = InitializeInfection(forest)

                forest[(np.random.rand(forest_size, forest_size) < p_infection) & (forest == -1)] = 1

            # Spread disease from already infected trees
            if (spread_disease):
                forest = SpreadDisease(forest, age_list, infection_time, p_spread)

            # Get wood outcome from harvest
            if (harvest_forest):
                wood_outcome[i, j] = HarvestForest(forest, age_list, min_age_agriculture, min_age_immune, relative_growth)

            # Update age
            age_list, infection_time_list = AgeCounter(age_list, infection_time_list, forest)

    # Calculate averages.
    wood_outcome_avg[forest_type] = np.mean(wood_outcome, axis=0)

# Plot averages.
if (plot_wood_outcome):
    plt.plot(range(len(wood_outcome_avg[0])), wood_outcome_avg[0], label="Forest 0")
    plt.plot(range(len(wood_outcome_avg[0])), wood_outcome_avg[1], label="Forest 1")
    plt.plot(range(len(wood_outcome_avg[0])), wood_outcome_avg[2], label="Forest 2")
    plt.axvline(min_age_agriculture, linestyle="dashed")
    plt.axvline(min_age_immune, linestyle="dashed")
    plt.xlabel("Iterations")
    plt.ylabel(r"wood outcome $[m^3]$")
    plt.title("Average Wood Outcome for 300 batches")
    plt.legend()
    plt.savefig("batch_plot_wood_outcome.png", dpi=200)
    plt.show()
