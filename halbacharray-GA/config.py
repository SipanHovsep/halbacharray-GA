import numpy as np


#------------------------------------RING DIMENSIONS------------------------------------#

# Define your parameters
InnerBoreDiameter = 160 * 1e-3  # Inner Diameter of the Ring
OuterBoreDiameter = 220 * 1e-3  # Outer Diameter of the Ring
magnetSize = 12 * 1e-3          # Length of cube (converted to meters)


#-------------------------------VARIABLE RING PARAMETERS--------------------------------#

amountBand = np.array([1,2])                 # Amount of bands within a ring
bandRadiiGap = np.linspace(0, 0.05, 60)    # Space between Bands
magnetSpace = np.linspace(0, 0.05, 35)     # Space Between Magnets
bandSep = np.linspace(0.002, 0.05, 60)     # Space between Bore and 1st band


#--------------------------------RING POSITIONS-----------------------------------------#

# Leave one section uncommented, 3 options to choose from depending on your design prefrence for determining ring positions


# Hard Coded Ring Seperation and Array length (ArrayLength may be subject to change)

arrayLength_0 = 240 * 1e-3
ringSep = 0.022
numRings_1 = arrayLength_0 / ringSep
numRings = int(numRings_1) + 1
arrayLength = ringSep * (numRings-1)
ringPositions = np.linspace(-arrayLength / 2, arrayLength / 2, numRings)


# Hard Coded Ring Number and Array Length 
"""
arrayLength_0 = 240 * 1e-3
numRings = 8
arrayLength = arrayLength_0
ringSep = arrayLength/(numRings-1)
ringPositions = np.linspace(-arrayLength / 2, arrayLength / 2, numRings)

"""


# Hard Coded Ring Number and Ring Seperation
"""

ringSep = 0.05
numRings = 22
arrayLength = ringSep * (numRings-1)
ringPositions = np.linspace(-arrayLength / 2, arrayLength / 2, numRings)

"""

#-----------------------------SIMULATION PARAMETERS-----------------------------------#

resolution = 2                      # Higher values result in lower precision (effective resolution = 1000 / resolution)
DSV = 0.7 * InnerBoreDiameter       # Diameter of the Spherical Volume, as a % of the inner bore diameter
simDimensions = (DSV, DSV, DSV)     # 3D dimensions of the simulation space, represented as (x, y, z)
# GA Parameters

popSim = 1000000                    # Total population size across all islands  
CXPB, MUTPB = 0.6, 0.3              # Crossover probability and mutation probability
maxGeneration = 200                 # Maximum number of generations for the genetic algorithm 
NGEN = maxGeneration                # Alias for maxGeneration (used for compatibility in function calls)
num_islands = 24                    # Number of islands (subpopulations) in the island model, depends on amount of cpus available
migration_interval = 15             # Number of generations between migrations of individuals between islands  
selected_algorithm = "eaSimple"     # Evolutionary algorithm to use ('eaSimple', 'eaMuPlusLambda', or 'eaMuCommaLambda')  