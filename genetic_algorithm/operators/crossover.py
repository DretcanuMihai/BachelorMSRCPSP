from random import Random


def cross_permutations_one_point(permutations_pair: list[list], random: Random, context=None) -> list[list]:
    p1, p2 = permutations_pair[0], permutations_pair[1]
    n = len(p1)
    k = random.randint(1, n - 1)
    o1 = cut_permutations_one_point_fixed(p1, p2, k)
    o2 = cut_permutations_one_point_fixed(p2, p1, k)
    return [o1, o2]


# generates the one-point cut permutation of two lists p1 and p2 with the cutting point k
def cut_permutations_one_point_fixed(p1: list, p2: list, k: int):
    o = p1[0:k]
    used = set(o)
    for elem in p2:
        if elem not in used:
            o.append(elem)
    return o


def cross_lists_uniform(lists_pair: list[list], random: Random, context=None) -> list[list]:
    l1, l2 = lists_pair[0], lists_pair[1]
    o1 = []
    o2 = []
    for e1, e2 in zip(l1, l2):
        if random.random() < 0.5:
            o1.append(e1)
            o2.append(e2)
        else:
            o1.append(e2)
            o2.append(e1)
    return [o1, o2]
