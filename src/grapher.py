import matplotlib.pyplot as plt


def display_graph(things_to_graph):
    '''

    :param things_to_graph: List of tuples where each tuple
        represents one graph. Tuples are as follows: x array,
        y array, x label, y label, title
    :return: None
    '''

    graph_number = 1

    for graph in things_to_graph:
        plt.subplot(len(things_to_graph), 1, graph_number)
        plt.plot(graph[0], graph[1])
        plt.xlabel(graph[2])
        plt.ylabel(graph[3])
        plt.title(graph[4])

        graph_number += 1

    plt.tight_layout()
    plt.show()