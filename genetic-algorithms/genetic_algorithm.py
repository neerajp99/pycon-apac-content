# Genetic Algorithm 
import random 

# Random population
def random_population(size, gene_size):
    """Random population of `size` number of individuals of `gene_size` length
    Args:
        size (int): Number of individuals in population
        gene_size (int): The length of each individual
    Returns:
        List[str]: Population of individuals
    """
    population = []
    for i in range(size):
        individual = []
        for j in range(gene_size):
            individual.append(chr(int(random.randrange(32, 126, 1))))
        population.append("".join(individual))
    return population

# Fitness function between two strings
def fitness_func(individual, target):
    """Calculate the fitness of an individual

    Args:
        individual (str): Individual chromosome
        target (str): Target string

    Returns:
        fitness: Fitness value
    """
    fitness = 0
    for index in range(12):
        fitness += abs(ord(individual[index]) - ord(target[index]))
    return fitness

# Calculate levenshtein distance 
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


# Parent selection 
def parent_selection(population, fitness, size):
    parents = []
    for i in range(size):
        max_fitness_index = fitness.index(max(fitness))
        parents.append(population[max_fitness_index])
        fitness[max_fitness_index] = -1
    return parents


# Crossover between two values 
def crossover(parent1, parent2):
    """Crossover between two parent individuals

    Args:
        parent1 (str): First parent
        parent2 (str): Second parent
    Returns:
        child1 (str): First child
        child2 (str): Second child
    """
    # Get random crossover point
    crossover_point = random.randrange(1, len(parent1))

    # Crossover parents
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]

    return child1, child2


def get_random_individual(fitness_list):
    """Get a random individual from fitness list
    
    Args:
        fitness_list (List[tuple]): List of tuples of fitness and individual
    Returns:
        individual (str): Random individual
    """
    fitness_sum = sum(fitness for individual, fitness in fitness_list)
    n = random.uniform(0, fitness_sum)
    for value, fitness in fitness_list:
        if n < fitness:
            return value
        else:
            n -= fitness
    return value


# Mutation
def mutation(individual, gene_size, mutation_rate):
    """Add mutation to individual

    Args:
        individual (str): Individual chromosome
        gene_size (int): The length of each individual
        mutation_rate (float): Mutation rate
    
    Returns:
        individual (str): Mutated individual
    """
    for index in range(len(individual)):
        if random.random() <  mutation_rate:
            individual = individual[:index] + chr(random.randint(32, 126)) + individual[index+1:]
    return individual

# Fit fitness values 
def fit_fitness(population, fitness_func, target):
    """Fitness calculation

    Args:
        population (List[str]): Population of individuals
        fitness_func (func): Fitness function
        target (str): Target string
    Returns:
        fitness_list (List[tuple]): List of tuples of fitness and individual
    """
    fitness_list = []
    for individual in population:
        fitness_val = fitness_func(individual, target)
        if fitness_val == 0:
            fitness_list.append((individual, 1.0))
        else:
            fitness_list.append((individual, 1.0 / fitness_val))
    return fitness_list

# Selection function 
def selection_mutation(population, fitness_func, size, fitness_list):
    """Selection and mutation

    Args:
        population (List[str]): Population of individuals
        fitness_func (func): Fitness function
        size (int): Size of population
        fitness_list (List[tuple]): List of tuples of fitness and individual

    Returns:
        population (List[str]): New population
    """
    # Select individuals
    population = []
    for index in range(size):
        parent1 = get_random_individual(fitness_list)
        parent2 = get_random_individual(fitness_list)

        # Crossover parents
        child1, child2 = crossover(parent1, parent2)

        # Apply mutation
        child1 = mutation(child1, 12, 0.05)
        child2 = mutation(child2, 12, 0.05)
        population.extend([child1, child2])
    return population

if __name__ == "__main__":
    target_string = 'jareenyednap'
    population = random_population(20, len(target_string))
    print(population)
    for i in range(4000):
        # print('Generation {}: {}'.format(i, population[0]))
        fitness_list = fit_fitness(population, fitness_func, target_string)
        population = selection_mutation(population, fitness_func, int(len(population) / 2), fitness_list)

    threshold_fitness = fitness_func(population[0], target_string)
    print(population)
    for individual in population:
        individual_fitness = fitness_func(individual, target_string)
        if individual_fitness <= threshold_fitness:
            fittest_string = individual
            threshold_fitness = individual_fitness
    print('Fittest string: ', fittest_string)