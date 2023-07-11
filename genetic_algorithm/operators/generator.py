from random import Random


# creates a function that when called, generates a permutation of [0,1,...,n-1]
def create_permutations_generator_function(n):
    def generate(random: Random, context=None) -> list[int]:
        return nc_generate_permutation(random, n)

    return generate


# generates a permutation of [0,1,...,n-1]
def nc_generate_permutation(random: Random, n) -> list[int]:
    permutation = [elem for elem in range(0, n)]
    random.shuffle(permutation)
    return permutation
