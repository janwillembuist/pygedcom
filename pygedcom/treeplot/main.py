import numpy as np
from matplotlib import pyplot as plt

BBOX = {
    'boxstyle': 'square',
    'fc': 'blue'
}

def plot_tree(tree, ax=None):
    if ax is None:
        ax = plt.gca()

    # Clear old plot if it exists
    ax.clear()
    gen_level = 1

    for generation in tree:
        person_amount = (gen_level-1) * 2
        if person_amount > 0:
            x = np.linspace(-2.5*gen_level, 2.5*gen_level, person_amount)
        else:
            x = [0]

        for person, dx in zip(generation, x):
            ax.text(
                dx,
                gen_level,
                person[1],
                bbox=BBOX,
                fontsize=12,
                ha='center',
                va='center',
            )
        gen_level += 1
    ax.set_xlim([-20, 20])
    ax.set_ylim([0, 4])
