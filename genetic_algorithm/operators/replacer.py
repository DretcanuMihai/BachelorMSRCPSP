from random import Random

from genetic_algorithm.general import Candidate


# replaces a population with a new one using an elitist approach
# let n be the size of offsprings
# the weakest n elements of the current population are replaced by the newly generated offspring
def replace_steady_state(current_candidates: list[Candidate], offspring_candidates: list[Candidate], random: Random,
                         problem_type, ) -> list[Candidate]:
    amount_kept = len(current_candidates) - len(offspring_candidates)
    return current_candidates[0:amount_kept] + offspring_candidates


# replaces a population with a new one using a generational approach
# the old population is entirely replaced by the offsprings
def generational_replace(current_candidates: list[Candidate], offspring_candidates: list[Candidate], random: Random,
                         problem_type) -> list[Candidate]:
    return offspring_candidates
