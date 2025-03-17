
"""
@author: tmachtelinckx
"""

import numpy as np
import config

def fieldError(shimVector, shared_data):
    """
    Calculate the homogeneity and field strength error values for a given shim configuration.

    Parameters:
    - shimVector (array-like): The indices representing the chosen shim configuration.
    - shared_data (numpy array): A 3D array containing precomputed field data.
    - T_target (float, optional): The target field strength (default: 0.05).
    - homogeneity_weight (float, optional): The weight given to homogeneity error (default: 0.85).
    - field_strength_weight (float, optional): The weight given to field strength error (default: 0.15).

    Returns:
    - tuple: A single-value tuple containing the total error score, which combines homogeneity 
      and field strength errors based on the given weights.
    """
    field = np.zeros(np.size(shared_data, 0))

    for idx1 in range(np.size(shimVector)):
        field += shared_data[:, idx1, shimVector[idx1]]

    # Homogeneity error
    homogeneity_error = ((np.max(field) - np.min(field)) / np.mean(field)) * 1e6

    # Field strength error
    mean_field_strength = np.mean(field)
    field_strength_error = np.abs(mean_field_strength - config.T_target) * 1e6

    # Combine the two errors into a single fitness score, prioritizing according to weighting
    total_error = (config.homogeneity_weight * homogeneity_error) + (config.field_strength_weight * field_strength_error)

    return (total_error,)

def calculate_field_characteristics(individual, shared_data):
    """
    Calculate the magnetic field strength and homogeneity for a given individual
    
    Returns:
    - mean_field: Average field strength
    - homogeneity: Field homogeneity in ppm
    """
    field = np.zeros(np.size(shared_data, 0))
    
    for idx1 in range(np.size(individual)):
        field += shared_data[:, idx1, individual[idx1]]
    
    mean_field = np.mean(field)
    homogeneity = ((np.max(field) - np.min(field)) / mean_field) * 1e6  # in ppm
    
    return mean_field, homogeneity

