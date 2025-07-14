import numpy as np

#------------------------------------RING DIMENSIONS------------------------------------#

# Define your parameters
InnerBoreDiameter = 500 * 1e-3  # Inner Diameter of the Ring (m)
OuterBoreDiameter = 900 * 1e-3  # Outer Diameter of the Ring (m)
magnetSize = 12 * 1e-3          # Length of cube (mm)


#-------------------------------VARIABLE RING PARAMETERS--------------------------------#

amountBand = np.array([2,3])               # Amount of bands within a ring
bandRadiiGap = np.linspace(0, 0.2, 70)     # Space between Bands (mm)
magnetSpace = np.linspace(0, 0.1, 70)     # Space Between Magnets (mm)
bandSep = np.linspace(0.002, 0.1, 70)      # Space between Bore and 1st band (mm)


#--------------------------------RING POSITIONS-----------------------------------------#
# Values are in meters
# Leave one section uncommented, 3 options to choose from depending on your design prefrence for determining ring positions


# Hard Coded Ring Seperation and Array length (ArrayLength may be subject to change)
"""
arrayLength_0 = 240 * 1e-3                                 
ringSep = 0.022
numRings_1 = arrayLength_0 / ringSep
numRings = int(numRings_1) + 1
arrayLength = ringSep * (numRings-1)
ringPositions = np.linspace(-arrayLength / 2, arrayLength / 2, numRings)
"""

# Hard Coded Ring Number and Array Length 
"""
arrayLength_0 = 240 * 1e-3
numRings = 8
arrayLength = arrayLength_0
ringSep = arrayLength/(numRings-1)
ringPositions = np.linspace(-arrayLength / 2, arrayLength / 2, numRings)

"""

# Hard Coded Ring Number and Ring Seperation


ringSep = 0.022
numRings = 11
arrayLength = ringSep * (numRings-1)
ringPositions = np.linspace(-arrayLength / 2, arrayLength / 2, numRings)


#----------------------------- FIELD ERROR PARAMETERS --------------------------------#

# Ensure that homogeneity_weight + field_strength_weight = 1

T_target = 0.08                 # Target field strength in Tesla
homogeneity_weight = 0.8       # Weight for homogeneity error 
field_strength_weight = 0.2    # Weight for field strength error

#-----------------------------SIMULATION PARAMETERS-----------------------------------#

resolution = 50                     # Higher values result in lower precision (effective resolution = 1000 / resolution)
DSV = 0.5 * InnerBoreDiameter       # Diameter of the Spherical Volume, as a % of the inner bore diameter (mm)
simDimensions = (DSV, DSV, DSV)     # 3D dimensions of the simulation space, represented as (x, y, z)
# GA Parameters

popSim = 500000                     # Total population size across all islands  
CXPB, MUTPB = 0.6, 0.3              # Crossover probability and mutation probability
maxGeneration = 150                 # Maximum number of generations for the genetic algorithm 
NGEN = maxGeneration                # Alias for maxGeneration (used for compatibility in function calls)
num_islands = 24                    # Number of islands (subpopulations) in the island model, depends on amount of cpus available
migration_interval = 15             # Number of generations between migrations of individuals between islands  
selected_algorithm = "eaSimple"     # Evolutionary algorithm to use ('eaSimple', 'eaMuPlusLambda', or 'eaMuCommaLambda')  
