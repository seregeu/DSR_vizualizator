import os

import Imaginator
from static import constants
from DSR import generate_graph_DSR, create_graph_visualization_DSR, get_route

if __name__ == '__main__':
    nodes = int(input("Введите количество вершин графа: "))
    a = int(input("Введите вершину А: "))
    b = int(input("Введите вершину Б: "))

    images_path = constants.images_path
    if not os.path.exists(images_path):
        os.makedirs(images_path)

    for filename in os.listdir(images_path):
        file_path = os.path.join(images_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    # генерируем случайный граф
    current_graph = generate_graph_DSR(nodes)
    # создаем визуализыйию графа
    create_graph_visualization_DSR(current_graph)

    route = get_route(current_graph, a, b)
    current_graph
    print(current_graph)
    print(route)
    Imaginator.animate_path(current_graph, route)
    Imaginator.animate_algo()
