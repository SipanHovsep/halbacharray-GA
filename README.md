# Halbach Array Optimization using Island Model Genetic Algorithm

This repository contains a complete framework for optimizing Halbach magnet array configurations to generate homogeneous magnetic fields. The system uses an island model genetic algorithm to find optimal arrangements of permanent magnets for applications like MRI, NMR, and other scientific instruments requiring uniform magnetic fields.

## Overview

Halbach arrays are special arrangements of permanent magnets that can create strong, uniform magnetic fields. This code allows for the optimization of complex multi-ring Halbach configurations with various parameters (spacing, magnet size, ring positions, etc.) to achieve specific field characteristics.

### Key Features

- **Island Model Genetic Algorithm**: Uses parallel evolution with migration for efficient optimization
- **Comprehensive Halbach Ring Modeling**: Flexible configuration of magnet arrangements
- **Field Calculation Engine**: Accurate computation of magnetic field profiles
- **Resource Monitoring**: Built-in tools to track computational resources
- **Detailed Result Logging**: Extensive documentation of optimization results

## Requirements

- Python 3.7+
- NumPy
- Pandas
- SciPy
- DEAP (Distributed Evolutionary Algorithms in Python)
- Matplotlib (for visualization)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/halbach-array-optimization.git
   cd halbach-array-optimization
   ```

2. Install required packages:
   ```
   pip install numpy pandas scipy deap matplotlib
   ```

## Code Structure

- **CHPC_Island_Model_Main.py**: The main script orchestrating the optimization process
- **config.py**: Configuration parameters for ring dimensions, simulation settings, and genetic algorithm parameters
- **field_calculations.py**: Functions for calculating magnetic field characteristics
- **Genetic_Functions.py**: Implementation of the island model genetic algorithm
- **HallbachRing_Edit_2.py**: Class for creating and managing Halbach ring configurations
- **initialization.py**: Functions for generating Halbach configurations and initializing shared memory
- **halbachFields.py**: Magnetic field calculation engine
- **documentation.py**: Functions for saving and documenting results
- **pbs_monitor.py**: Resource monitoring for PBS-based cluster environments

## Usage

### Basic Usage

1. Modify the parameters in `config.py` to set up your desired optimization:
   - Ring dimensions (inner/outer diameter)
   - Magnet size and spacing
   - Number of rings and positions
   - Genetic algorithm parameters

2. Run the main script:
   ```
   python CHPC_Island_Model_Main.py
   ```

3. Results will be saved in the `GA_Results` folder, including:
   - Hallbach configurations (Excel file)
   - Comprehensive optimization results (CSV)
   - Hall of Fame containing best individuals
   - Logbook with generation-by-generation statistics
   - Duplicate statistics

### Configuration Options

#### Ring Parameters (in `config.py`)

```python
# Ring dimensions
InnerBoreDiameter = 160 * 1e-3  # Inner Diameter (meters)
OuterBoreDiameter = 220 * 1e-3  # Outer Diameter (meters)
magnetSize = 12 * 1e-3          # Magnet size (meters)

# Variable parameters
amountBand = np.array([1,2])    # Amount of bands within a ring
bandRadiiGap = np.linspace(0, 0.05, 60)  # Space between bands
magnetSpace = np.linspace(0, 0.05, 35)   # Space between magnets
bandSep = np.linspace(0.002, 0.05, 60)   # Space between bore and 1st band
```

#### Genetic Algorithm Parameters

```python
popSim = 1000000        # Total population size across all islands
CXPB, MUTPB = 0.6, 0.3  # Crossover and mutation probabilities
maxGeneration = 200     # Maximum generations
num_islands = 24        # Number of islands for parallel evolution
migration_interval = 15 # Generations between migrations
```

#### Optimization Target

The optimization targets can be adjusted in the `fieldError` function in `field_calculations.py`:

```python
def fieldError(shimVector, shared_data, T_target=0.05, homogeneity_weight=0.85, field_strength_weight=0.15):
    # ...
```

- `T_target`: Target field strength (Tesla)
- `homogeneity_weight`: Weight given to field homogeneity in fitness function
- `field_strength_weight`: Weight given to field strength in fitness function

## Running on a Cluster

The code includes PBS (Portable Batch System) integration for running on high-performance computing clusters:

1. Submit the job using a PBS script:
   ```bash
   #!/bin/bash
   #PBS -N halbach_opt
   #PBS -l select=1:ncpus=24:mem=64gb
   #PBS -l walltime=24:00:00
   
   cd $PBS_O_WORKDIR
   python CHPC_Island_Model_Main.py
   ```

2. The `pbs_monitor.py` module will automatically track resource usage.

## Understanding Results

The optimization produces several output files:

- **hallbach_configurations.xlsx**: All possible Halbach configurations with parameters
- **hof_individuals.csv**: Best individuals from the Hall of Fame
- **logbook.csv**: Generation-by-generation statistics
- **comprehensive_results.csv**: Detailed results for the best configuration
- **duplicate_statistics.csv**: Statistics on duplicate individuals during evolution

The best configuration is represented as a vector of indices, where each index corresponds to a specific Halbach ring configuration from the configuration set.

## Example Results

A successful optimization will produce a configuration with:
- High field homogeneity (low ppm value)
- Field strength close to the target value
- Practical configuration that fits within physical constraints

## Theory and Background

Halbach arrays are specialized arrangements of permanent magnets where the orientation of magnetization varies in a way that reinforces the field on one side while canceling it on the other. By optimizing the arrangement of these arrays, we can create magnetic fields with specific characteristics:

- High field strength
- Excellent homogeneity within a defined volume
- Compact design with efficient use of magnetic material

The optimization uses a genetic algorithm with an island model, which:
1. Maintains multiple isolated populations (islands)
2. Evolves each population independently
3. Periodically migrates individuals between islands
4. This approach helps maintain diversity and avoid local optima
