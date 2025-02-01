import avl
import matplotlib.pyplot as plt
import copy


def plot_tree(avl: avl.AVL) -> None:
    """Visualize whole tree"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')

    plot_node(avl.raw(), 0, 0, 0, ax)
    plt.show()


def plot_node(node, x, y, offset, ax, level=1):
    """Helper function to visualize tree node by node"""
    if node is not None:
        horizontal_offset = 1.5 / level
        level += 1

        # Plot lines for child nodes
        if node.left is not None:
            ax.plot([x, x - horizontal_offset], [y, y - 1], color="black")
            plot_node(node.left, x - horizontal_offset, y - 1, horizontal_offset / 2, ax, level)
        if node.right is not None:
            ax.plot([x, x + horizontal_offset], [y, y - 1], color="black")
            plot_node(node.right, x + horizontal_offset, y - 1, horizontal_offset / 2, ax, level)

        # Draw label for each node
        ax.text(x, y, str(node.key), ha="center", va="center",
                bbox=dict(facecolor="skyblue", edgecolor="black", boxstyle="circle"))

if __name__ == "__main__":
    # Example of tree visualization
    avl = avl.AVL()
    keys = [50, 50, 30, 70, 20, 40, 60, 80]
    for key in keys:
        avl.insert(key)

    new_avl = avl + avl + avl + avl + avl + avl
    
    plot_tree(new_avl)
