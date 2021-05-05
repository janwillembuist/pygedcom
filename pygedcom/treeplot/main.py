from matplotlib import pyplot as plt
def plot_tree(tree, ax=None):
    if ax is None:
        ax = plt.gca()

    # Clear old plot if it exists
    ax.clear()
    ax.plot([1, 2, 3], label='hoi')
    ax.legend()