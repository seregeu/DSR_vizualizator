import os

import imageio
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


def animate_algo():
    # Путь к папке с изображениями
    images_folder = 'static/img/DSR_gallery/'

    # Получаем список файлов с расширением .png или .jpg
    image_files = [os.path.join(images_folder, f) for f in os.listdir(images_folder) if
                   f.endswith('.png') or f.endswith('.jpg')]

    # Создаем список с изображениями
    images = []
    for filename in image_files:
        images.append(imageio.imread(filename))

    # Создаем анимацию
    animation_file = 'animation.gif'
    imageio.mimsave(animation_file, images, duration=1)  # duration - задает время показа каждого кадра в секундах


def animate_path(G, path):
    fixed_nodes = list(G.nodes)

    random_pos0 = nx.kamada_kawai_layout(G)
    pos = nx.spring_layout(G, pos=random_pos0.copy(), fixed=fixed_nodes.copy())
    fig, ax = plt.subplots()

    # добавляем подписи к вершинам
    labels = {i: i for i in range(0, len(G))}
    #nx.draw_networkx_labels(G, pos, labels=labels)

    def update(ii):
        ax.clear()
        nx.draw_networkx_nodes(G, pos, node_color='blue', ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=[path[ii]], node_color='red', ax=ax)
        nx.draw_networkx_edges(G, pos, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=ax)

        # добавляем подписи к вершинам
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='white', font_weight='bold', ax=ax)

        ax.set_title(f"Шаг {ii+1} / {len(path)}")

    animation = FuncAnimation(fig, update, frames=len(path), repeat=True)
    writer = PillowWriter(fps=2)
    animation.save('path.gif', writer=writer)