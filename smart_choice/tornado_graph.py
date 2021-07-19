"""
Tornado Graph
===============================================================================


"""

import matplotlib.pyplot as plt
from operator import itemgetter


def tornado_graph(sensitivities: dict):
    """Creates a tornado graph of value sensitivities for the analyzed tree.

    :param sensitivities:
        dictionary contains ValueSensitivity results for individual values in the tree.

    """
    data = [
        (
            key,
            max(sensitivities[key].df_["Expected Value"])
            - min(sensitivities[key].df_["Expected Value"]),
            min(sensitivities[key].df_["Expected Value"]),
        )
        for key in sensitivities.keys()
    ]

    data = sorted(data, key=itemgetter(1), reverse=False)

    names = [value for value, _, _ in data]

    width = [value for _, value, _ in data]
    left = [value for _, _, value in data]
    seq = list(range(len(data)))

    plt.gca().barh(y=seq, width=width, left=left, color="gray", alpha=0.8)

    plt.gca().spines["bottom"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().set_xlabel("Expected values")

    plt.yticks(seq, names)

    plt.grid()
