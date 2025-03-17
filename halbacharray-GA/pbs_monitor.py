"""
@author: tmachtelinckx
"""

import os
import time
import subprocess

def get_current_job_id():
    """Get the PBS job ID for the current script."""
    return os.environ.get('PBS_JOBID')

def monitor_pbs_resources(job_id, interval=600, output_file="pbs_resources.csv"):
    """
    Monitors PBS job resource usage over specified intervals and logs it to a CSV file.
    
    Parameters:
    - job_id (str): PBS job ID to monitor
    - interval (int): Time in seconds between recording values
    - output_file (str): Path to save resource usage data
    """
    with open(output_file, "w") as file:
        # Write the header for CSV
        file.write("Timestamp,CPU_Percent,CPU_Time,Memory_KB,NCPUs,Virtual_Memory_KB,Walltime\n")
        
        try:
            while True:
                # Get current timestamp
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Run qstat command to get resource usage
                try:
                    result = subprocess.run(["qstat", "-f", job_id], 
                                         capture_output=True, text=True)
                    
                    if result.returncode != 0:
                        print(f"Job {job_id} not found. It may have completed.")
                        break
                        
                    output = result.stdout
                    
                    # Extract resource values using simple string parsing
                    cpupercent = output.split('resources_used.cpupercent =')[1].split('\n')[0].strip()
                    cput = output.split('resources_used.cput =')[1].split('\n')[0].strip()
                    mem = output.split('resources_used.mem =')[1].split('\n')[0].strip()
                    ncpus = output.split('resources_used.ncpus =')[1].split('\n')[0].strip()
                    vmem = output.split('resources_used.vmem =')[1].split('\n')[0].strip()
                    walltime = output.split('resources_used.walltime =')[1].split('\n')[0].strip()
                    
                    # Write values to file
                    file.write(f"{timestamp},{cpupercent},{cput},{mem},"
                             f"{ncpus},{vmem},{walltime}\n")
                    file.flush()
                    
                except subprocess.SubprocessError as e:
                    print(f"Error running qstat: {e}")
                    break
                except IndexError as e:
                    print(f"Error parsing qstat output: {e}")
                    break
                    
                # Wait for next interval
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
        except Exception as e:
            print("Monitoring stopped:", e)