import numpy as np

def gini(sequence):
    categories = set(sequence)
    res, num = 1., len(sequence)
    if num == 0:
        return 0
    for category in categories:
        res -= (len(sequence[sequence == category])/num) ** 2
    return res


def entropy(sequence):
    categories = set(sequence)
    res, num = 0, len(sequence)
    if num == 0:
        return 0
    for category in categories:
        prob = len(sequence[sequence == category])/num
        res += -prob*np.log2(prob)
    return res
