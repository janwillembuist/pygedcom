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
    ax.text(
        1,
        1,
        tree.selected_individual.fullname,
        bbox=BBOX,
        fontsize=15,
        ha='center',
        va='center',
    )
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 10])
