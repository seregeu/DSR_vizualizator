import os

import imageio
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from matplotlib.animation import FuncAnimation, PillowWriter

from static import constants


# Вывод пошаговых картинок
def saveCurStepAsImage():
    pass


# Вывод анимации путем склеивания пошаговых картинок
def animate_algo():
    # Путь к папке с изображениями
    images_folder = constants.images_path

    # Получаем список файлов с расширением .png или .jpg
    image_files = [os.path.join(images_folder, f) for f in os.listdir(images_folder) if
                   f.endswith('.png') or f.endswith('.jpg')]

    # Создаем список с изображениями и добавляем подписи и рамки
    images = []
    font = ImageFont.truetype("arial.ttf", 20)  # шрифт и размер подписи
    for i, filename in enumerate(image_files):
        im = Image.open(filename)
        draw = ImageDraw.Draw(im)
        # координаты текста
        text_width, text_height = draw.textsize(f"Шаг {i+1}", font=font)
        x = (im.width - text_width) // 2
        y = 10
        draw.text((x, y), f"Шаг {i+1}", font=font, fill=(0, 0, 0))  # добавляем подпись на изображение
        # добавляем рамку
        draw.rectangle([0, 0, im.width - 1, im.height - 1], outline=(0, 0, 0))
        images.append(im)

    # Создаем анимацию
    animation_file = 'animation.gif'
    imageio.mimsave(animation_file, images, duration=1)  # duration - задает время показа каждого кадра в секундах



# Анимируем путь и выводим в виде гифки
def animate_path(G, path):
    fixed_nodes = list(G.nodes)

    random_pos0 = nx.kamada_kawai_layout(G)
    pos = nx.spring_layout(G, pos=random_pos0.copy(), fixed=fixed_nodes.copy())
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 7)

    # добавляем подписи к вершинам
    labels = {i: i for i in range(0, len(G))}

    def update(ii):
        ax.clear()
        nx.draw_networkx_nodes(G, pos, node_color='blue', ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=[path[ii]], node_color='red', ax=ax)
        nx.draw_networkx_edges(G, pos, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=ax)

        # добавляем подписи к вершинам
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='white', font_weight='bold', ax=ax)

        ax.set_title(f"Шаг {ii + 1} / {len(path)}")

    animation = FuncAnimation(fig, update, frames=len(path), repeat=True)
    writer = PillowWriter(fps=2)
    animation.save('path.gif', writer=writer)
