import os

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import Imaginator
from DSR import generate_graph_DSR, create_graph_visualization_DSR, get_route

if __name__ == '__main__':
    images_path = 'static/img/DSR_gallery/'
    if not os.path.exists(images_path):
        os.makedirs('static/img/DSR_gallery/')

    for filename in os.listdir('static/img/DSR_gallery/'):
        file_path = os.path.join('static/img/DSR_gallery/', filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    """G = nx.Graph()
    G.add_edges_from([(0, 1),
                      (0, 2),
                      (1, 3),
                      (2, 3),
                      (3, 4),
                      (4, 5),
                      (4, 6),
                      (5, 6)])

    path = [0, 1, 3, 4, 6]
    Imaginator.animate_path(G,path)"""
    nodes = 16
    # сгенерировать граф, он в виде графа
    current_graph = generate_graph_DSR(nodes)
    # создать визуализацию графа
    create_graph_visualization_DSR(current_graph)

    route = get_route(current_graph, 1, 5)
    current_graph
    print(current_graph)
    print(route)
    Imaginator.animate_path(current_graph, route)
    Imaginator.animate_algo()





