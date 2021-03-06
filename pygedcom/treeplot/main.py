import numpy as np
from matplotlib import pyplot as plt

BBOX = {
    'boxstyle': 'square',
    'fc': '#80AF95'
}

def plot_tree(tree, ax=None):
    if ax is None:
        ax = plt.gca()

    # Clear old plot if it exists
    ax.clear()
    ax.axis('off')

    gen_level = 0

    for generation in tree:
        gen_level += 1
        person_amount = len(generation)
        if person_amount > 1:
            if generation[0][0] == 0:
                # Kid generation
                x = np.linspace(-scaling(person_amount), scaling(person_amount), person_amount)
                size = 14
            elif generation[0][0] == 1:
                # Parents
                x = [0, 1]
            else:
                # Elders
                x = np.linspace(-scaling(gen_level), scaling(gen_level), person_amount)
                size = 18 - (gen_level-1)*2
        else:
            try:
                level = generation[0][0]
                if level == 0:
                    size = 14
                else:
                    size = 18 - (gen_level-1)*2
            except IndexError:
                size = 18 - (gen_level-1)*2
            x = [0]

        for person, dx in zip(generation, x):
            if person[1] is not None:
                ax.text(
                    dx,
                    gen_level,
                    person[1].fullname.replace(' ', '\n'),
                    bbox=BBOX,
                    fontsize=size,
                    ha='center',
                    va='center',
                    picker=5
                )

    # Set limits
    ax.set_xlim([-scaling(gen_level), scaling(gen_level)])
    ax.set_ylim([0.99, gen_level + 0.01])

def scaling(gen_level):
    return gen_level / 2
