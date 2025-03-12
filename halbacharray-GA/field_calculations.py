import numpy as np

def fieldError(shimVector, shared_data, T_target=0.05, homogeneity_weight=0.85, field_strength_weight=0.15):
    """
    Calculate the Homogeneity and Field strength error values

    """
    field = np.zeros(np.size(shared_data, 0))

    for idx1 in range(np.size(shimVector)):
        field += shared_data[:, idx1, shimVector[idx1]]

    # Homogeneity error
    homogeneity_error = ((np.max(field) - np.min(field)) / np.mean(field)) * 1e6

    # Field strength error
    mean_field_strength = np.mean(field)
    field_strength_error = np.abs(mean_field_strength - T_target) * 1e6

    # Combine the two errors into a single fitness score, prioritizing according to weighting
    total_error = (homogeneity_weight * homogeneity_error) + (field_strength_weight * field_strength_error)

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

