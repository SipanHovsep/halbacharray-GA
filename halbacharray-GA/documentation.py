"""
@author: tmachtelinckx
"""

import os
import pandas as pd
import numpy as np

def save_dataframe_to_excel(df, output_folder, InnerBoreDiameter, OuterBoreDiameter, magnetSize):
    """
    Save detailed DataFrame information to an Excel file.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame containing the Hallbach ring parameters
    output_folder (str): Folder path to save the Excel file
    """
    # Create a list to store the expanded data
    expanded_data = []
    
    # Iterate through the DataFrame and create detailed entries
    for index, row in df.iterrows():
        # Convert the arrays to lists if they aren't already
        band_radius = row['BandRadius'].tolist() if isinstance(row['BandRadius'], np.ndarray) else row['BandRadius']
        magnet_nr = row['MagnetNr'].tolist() if isinstance(row['MagnetNr'], np.ndarray) else row['MagnetNr']
        
        entry = {
            'Configuration_Number': index,
            'Band_Number': row['BandNumber'],
            'Band_Radii_Gap_mm': row['BandRadiiGap'] * 1000,  # Convert to mm
            'Magnet_Space_mm': row['MagnetSpace'] * 1000,     # Convert to mm
            'Band_Separation_mm': row['BandSeparation'] * 1000 # Convert to mm
        }
        
        # Add band radius and magnet number for each band
        for i in range(len(band_radius)):
            entry[f'Band_{i+1}_Radius_mm'] = band_radius[i] * 1000  # Convert to mm
            entry[f'Band_{i+1}_Magnet_Count'] = magnet_nr[i]
        
        expanded_data.append(entry)
    
    # Convert to DataFrame
    detailed_df = pd.DataFrame(expanded_data)
    
    # Create Excel writer object
    excel_path = os.path.join(output_folder, 'hallbach_configurations.xlsx')
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        # Write the main data
        detailed_df.to_excel(writer, sheet_name='Configurations', index=False)
        
        # Add a metadata sheet
        metadata = pd.DataFrame({
            'Parameter': [
                'Inner Bore Diameter',
                'Outer Bore Diameter',
                'Magnet Size',
                'Total Configurations',
                'Units'
            ],
            'Value': [
                f'{InnerBoreDiameter * 1000:.1f} mm',
                f'{OuterBoreDiameter * 1000:.1f} mm',
                f'{magnetSize * 1000:.1f} mm',
                len(df),
                'All dimensions in millimeters (mm)'
            ]
        })
        metadata.to_excel(writer, sheet_name='Metadata', index=False)
        
    return excel_path

def save_duplicate_statistics(duplicate_stats, results_folder):
    """Save the duplicate statistics to a CSV file."""
    duplicate_file = os.path.join(results_folder, "duplicate_statistics.csv")
    flat_stats = []
    for island_idx, island_stats in enumerate(duplicate_stats):
        for stat in island_stats:
            stat['island'] = island_idx
            flat_stats.append(stat)
    
    duplicate_df = pd.DataFrame(flat_stats)
    duplicate_df.to_csv(duplicate_file, index=False)
    return duplicate_file

def save_comprehensive_results(best_individual, mean_field, homogeneity, algorithm_time, total_execution_time, NGEN, results_folder):
    """Save the comprehensive results to a CSV file."""
    comprehensive_results_file = os.path.join(results_folder, "comprehensive_results.csv")
    results_dict = {
        'Generation': [NGEN],
        'Best_Individual': [','.join(map(str, best_individual))],
        'Fitness_Value': [best_individual.fitness.values[0]],
        'Mean_Field_Strength': [mean_field],
        'Homogeneity_PPM': [homogeneity],
        'Algorithm_Time_Seconds': [algorithm_time],
        'Total_Execution_Time_Seconds': [total_execution_time]
    }
    pd.DataFrame(results_dict).to_csv(comprehensive_results_file, index=False)
    return comprehensive_results_file

def save_hof_and_logbook(hof, logs, results_folder):
    """Save Hall of Fame and Logbook to CSV files."""
    hof_file = os.path.join(results_folder, "hof_individuals.csv")
    logbook_file = os.path.join(results_folder, "logbook.csv")
    
    with open(hof_file, "w") as hof_file_obj:
        for ind in hof:
            hof_file_obj.write(",".join(map(str, ind)) + "," + str(ind.fitness.values[0]) + "\n")
    
    logs.to_csv(logbook_file, index=False)
    return hof_file, logbook_file