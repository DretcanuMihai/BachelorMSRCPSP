from random import Random


# creates a mutation function that interchanges two values of a permutation
def mutate_permutations_by_interchange(p: list, random: Random, context=None) -> list:
    p = p[:]  # we create a copy of p such that we don't modify the original
    n = len(p)
    k1 = random.randint(0, n - 1)
    k2 = random.randint(0, n - 1)
    while k2 == k1:
        k2 = random.randint(0, n - 1)
    p[k1], p[k2] = p[k2], p[k1]
    return p


# creates a function that applies a mutation with a given probability
def create_probabilistic_mutator_function(mutator_function, mutation_probability: float):
    def mutate(candidate, random: Random, context):
        if random.random() < mutation_probability:
            return mutator_function(candidate, random, context)
        return candidate

    return mutate
