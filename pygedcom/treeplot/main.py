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
        for person in generation:
            ax.text(
                1,
                gen_level,
                person[1],
                bbox=BBOX,
                fontsize=15,
                ha='center',
                va='center',
            )
        gen_level += 2
    ax.set_xlim([-10, 10])
    ax.set_ylim([0, 10])
