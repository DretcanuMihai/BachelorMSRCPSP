from random import Random

from genetic_algorithm.general import Candidate


def create_tournament_selector_function(amount_to_select: int, tournament_size: int, probability: float = 1):
    """
    generates a function that does tournament selections
    :param amount_to_select: the amount to be selected (returned)
    :param tournament_size: how many individuals participate in a tournament
    :param probability: the probability of the stronger candidate to win
    more exactly, if we have candidates [c1,c2,...,cn], c1 has a probability of p to win
    c2 has a probability of p(1-p) to win, c3 p(1-p)^2 etc.
    :return: a function that applies a tournament selection routine
    """

    def select(candidates: list[Candidate], random: Random, problem_type) -> list[Candidate]:
        selected = []
        available_indices = [i for i in range(0, len(candidates))]
        for _ in range(amount_to_select):
            # generate the tournament participants
            tournament_participants = sorted(random.sample(available_indices, tournament_size))
            # do the tournament and choose a winner
            winner_index = 0
            while winner_index < tournament_size - 1:
                if random.random() < probability:
                    break
                winner_index += 1
            winner_index = tournament_participants[winner_index]
            # now that someone is chosen, he's not available anymore
            available_indices.remove(winner_index)
            selected.append(winner_index)
        return [candidates[elem] for elem in selected]

    return select
