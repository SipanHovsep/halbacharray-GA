import numpy as np
from deap import algorithms, tools
import pandas as pd
import multiprocessing
from collections import Counter

def count_duplicates(population):
    """
    Count how many duplicate individuals exist in the population
    Returns both the count and percentage of duplicates
    """
    # Convert individuals to tuples for hashability
    tuple_population = [tuple(ind) for ind in population]
    
    counts = Counter(tuple_population)
    
    # Calculate duplicates
    duplicates = sum(count - 1 for count in counts.values() if count > 1)
    unique_individuals = len(counts)
    total_population = len(population)
    duplicate_percentage = (duplicates / total_population) * 100
    
    return {
        'total_population': total_population,
        'unique_individuals': unique_individuals,
        'duplicate_count': duplicates,
        'duplicate_percentage': duplicate_percentage
    }

def migrate_island(populations, migration_rate=0.3):
    """Migrate individuals between islands."""
    num_migrate = int(migration_rate * len(populations[0]))  # Number of individuals to migrate

    for i in range(len(populations)):
        source_island = populations[i]
        target_island = populations[(i + 1) % len(populations)]
        migrants = tools.selBest(source_island, num_migrate)
        immigrants = tools.selWorst(target_island, num_migrate)

        for j in range(num_migrate):
            target_island.remove(immigrants[j])
            target_island.append(migrants[j])

    return populations

def get_fitness(ind):
    return ind.fitness.values[0]

def create_stats():
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    return stats

def evolve_island(algorithm_type, pop, toolbox, cxpb, mutpb, ngen):
    """
    Runs a selected evolutionary algorithm on a population for a given number of generations.
    
    Tracks population statistics, including fitness metrics and duplicate counts, and updates 
    the Hall of Fame with the best individual found.

    Parameters:
        algorithm_type (str): The name of the evolutionary algorithm to use ('eaSimple', 'eaMuPlusLambda', or 'eaMuCommaLambda').
        pop (list): The population of individuals to evolve.
        toolbox (deap.base.Toolbox): The DEAP toolbox containing genetic operators.
        cxpb (float): Crossover probability.
        mutpb (float): Mutation probability.
        ngen (int): Number of generations to run the evolution.

    Returns:
        tuple: (final population, logbook of statistics, duplicate tracking data)
    """
    stats = create_stats()
    hof = tools.HallOfFame(1)
    
    # Initialize duplicate tracking
    duplicate_stats = []
    
    def collect_stats(pop, gen):
        duplicate_info = count_duplicates(pop)
        duplicate_info['generation'] = gen
        duplicate_stats.append(duplicate_info)
    
    # Collect initial stats
    collect_stats(pop, 0)
    
    if algorithm_type == "eaSimple":
        pop, log = algorithms.eaSimple(pop, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=ngen, 
                                     stats=stats, halloffame=hof, verbose=True)
    elif algorithm_type == "eaMuPlusLambda":
        pop, log = algorithms.eaMuPlusLambda(pop, toolbox, mu=5000, lambda_=3000, 
                                           cxpb=cxpb, mutpb=mutpb, ngen=ngen, 
                                           stats=stats, halloffame=hof, verbose=True)
    elif algorithm_type == "eaMuCommaLambda":
        pop, log = algorithms.eaMuCommaLambda(pop, toolbox, mu=5000, lambda_=5000, 
                                            cxpb=cxpb, mutpb=mutpb, ngen=ngen, 
                                            stats=stats, halloffame=hof, verbose=True)
    else:
        raise ValueError(f"Algorithm type '{algorithm_type}' not recognized")
    
    # Collect final stats
    collect_stats(pop, ngen)
    
    return pop, log, duplicate_stats

def evolve_island_wrapper(args):
    """
    Wrapper function for evolve_island to enable parallel execution with multiprocessing.
    Unpacks arguments and calls evolve_island, returning population, log, and duplicate statistics.
    """ 
    algorithm_type, pop, toolbox, cxpb, mutpb, ngen = args
    pop, log, duplicate_stats = evolve_island(algorithm_type, pop, toolbox, cxpb, mutpb, ngen)
    return pop, log, duplicate_stats

def island_model(toolbox, cxpb, mutpb, ngen, num_islands, num_generations, migration_interval, popSim, selected_algorithm):
    """
    Runs a parallelized island model with genetic algorithms, evolving populations across multiple islands.
    
    Tracks fitness metrics and duplicate statistics across all islands, and migrates individuals
    between islands at specified intervals. The best individual across all islands is updated in the
    Hall of Fame.

    Parameters:
        toolbox (deap.base.Toolbox): The DEAP toolbox containing genetic operators.
        cxpb (float): Crossover probability.
        mutpb (float): Mutation probability.
        ngen (int): Number of generations to run the evolution.
        num_islands (int): Number of islands (subpopulations) in the model.
        num_generations (int): Total number of generations to evolve.
        migration_interval (int): Interval at which individuals are migrated between islands.
        popSim (int): Population size.
        selected_algorithm (str): The evolutionary algorithm to use ('eaSimple', 'eaMuPlusLambda', or 'eaMuCommaLambda').

    Returns:
        tuple: (final populations, combined logbook of statistics, Hall of Fame with the best individual, 
               duplicate statistics across all islands)
    """
    populations = [toolbox.population(n=popSim // num_islands) for _ in range(num_islands)]
    logs = []
    all_duplicate_stats = []
    hof = tools.HallOfFame(1)

    for gen in range(0, num_generations, migration_interval):
        with multiprocessing.Pool(processes=num_islands) as pool:
            args = [(selected_algorithm, pop, toolbox, cxpb, mutpb, migration_interval) 
                   for pop in populations]
            results = pool.map(evolve_island_wrapper, args)

        populations = [pop for pop, _, _ in results]
        logs.extend([log for _, log, _ in results])
        all_duplicate_stats.extend([stats for _, _, stats in results])
        
        # Track duplicates after migration
        populations = migrate_island(populations)

    # Combine logs from all islands
    combined_log = pd.concat([pd.DataFrame(log) for log in logs])
    
    # Find the best individual across all islands
    best_individuals = [tools.selBest(pop, 1)[0] for pop in populations]
    best_individual = min(best_individuals, key=lambda ind: ind.fitness.values)
    hof.update([best_individual])

    return populations, combined_log, hof, all_duplicate_stats