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
    ax.axis('off')
    gen_level = 1
    for generation in tree:
        person_amount = 2 ** (gen_level-1)
        if person_amount > 1:
            x = np.linspace(-gen_level, gen_level, person_amount)
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

    # Set limits
    ax.set_xlim([-gen_level, gen_level])
    ax.set_ylim([0, gen_level])
