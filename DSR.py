import itertools
import os
import matplotlib.animation as animation

import numpy.random as rnd
import networkx as nx
import matplotlib.pyplot as plt
import re

from moviepy.video.io.bindings import mplfig_to_npimage
from pyvis import network as net

from static import constants

IMAGE_W = 10
IMAGE_H = 7


def generate_graph(n, p):
    G = nx.Graph()
    nodes = range(n)
    G.add_nodes_from(nodes)
    for pair in itertools.permutations(nodes, 2):
        if rnd.random() < p:
            G.add_edge(*pair)
    return G


def RREQ_str(RREQ):
    return str(RREQ[0]) + ", " + str(RREQ[1]) + ", " + str(RREQ[2]) + ", " + str(RREQ[3])


def is_nodes_connected(u, v, Graph):
    return u in Graph.neighbors(v)


def req(H, src, init_src, dict_nodes, pos, my_nodelist, dst, broadcasted, counter):
    counter += 1
    node_labels = {}
    node_number = len(H.nodes)
    list_adj = list(H.neighbors(src))
    if (init_src != -1):
        list_adj.remove(init_src)
    if not list_adj:
        print("finita la commedia!\n")
    else:
        for i in list_adj:
            if (not (dict_nodes[i])[1]):  # Не пусто
                if (i != int((dict_nodes[i])[2])):  # Не отправитель
                    (dict_nodes[i])[1] = (dict_nodes[src])[1] + str(i) + ';'
            # Поиск наименьшего
            else:
                alt_path = (dict_nodes[src])[1] + str(i) + ';'
                alt_path_semi = re.sub('[^;]', '', alt_path)
                init_path_semi = re.sub('[^;]', '', (dict_nodes[i])[1])
                if (len(alt_path_semi) < len(init_path_semi)):
                    (dict_nodes[i])[1] = alt_path
            # Установка цвета вершин
            node_colors = ['#fef89a'] * node_number
            node_colors[i] = '#6495ED'
            # Рисование графа
            figure = plt.gcf()
            figure.set_size_inches(IMAGE_W, IMAGE_H)
            plt.cla()
            node_labels.clear()
            for j in range(node_number):
                if (not (dict_nodes[j])[1]):
                    node_labels[j] = str(j)
                else:
                    node_colors[j] = '#6495ED'
                    node_labels[j] = str(dict_nodes[j]) + "\n" + str(j)
            nx.draw(H, pos, node_color=node_colors, edge_color='#9d9d95', node_size=420, with_labels=False)
            my_nodelist.append(src)
            # nx.draw(H, pos, nodelist=my_nodelist, node_color='#fe679f', edge_color='#9d9d95', node_size=420,
            #         with_labels=False)
            nx.draw_networkx_labels(H, pos, node_labels, font_size=9)

            plt.savefig((f'{constants.images_path}' + '{:04d}.png').format(counter))

        broadcasted.append(src)
        for i in list_adj:
            if (i not in broadcasted and i != dst):
                req(H, i, src, dict_nodes, pos, my_nodelist, dst, broadcasted, counter)




def generate_graph_DSR(nodes):
    while True:
        H = generate_graph(nodes, 0.12)
        if (nx.is_connected(H) == True and nx.has_bridges(H) == False):
            return H

def create_graph_visualization_DSR(H):
    plt.clf()
    fixed_nodes = list(H.nodes)

    random_pos0 = nx.kamada_kawai_layout(H)
    pos = nx.spring_layout(H, pos=random_pos0.copy(), fixed=fixed_nodes.copy())

    figure = plt.gcf()
    figure.set_size_inches(IMAGE_W, IMAGE_H)
    nx.draw(H, pos, node_color='#fef89a', edge_color='#9d9d95', node_size=420, with_labels=True)
    try:
        os.remove(constants.images_path + '0.png')
    except:
        print('oops')
    plt.savefig(constants.images_path + '0.png')


def get_route(H, src, dst):
    UID = 2

    dict_nodes = {}
    RREQ = []
    fixed_nodes = list(H.nodes)
    random_pos0 = nx.kamada_kawai_layout(H)
    pos = nx.spring_layout(H, pos=random_pos0.copy(), fixed=fixed_nodes.copy())
    figure = plt.gcf()
    figure.set_size_inches(IMAGE_W, IMAGE_H)
    nx.draw(H, pos, node_color='#fef89a', edge_color='#9d9d95', node_size=420, with_labels=True)
    # plt.pause(1.6)

    # заполняем RREQ
    RREQ.append(UID)
    RREQ.append("")
    RREQ.append(src)
    RREQ.append(dst)
    node_number = len(H.nodes)
    for j in range(node_number):
        dict_nodes[j] = RREQ.copy()

    my_nodelist = [src, dst]
    # чтобы не бродкастить повторно
    broadcasted = []
    req(H, src, -1, dict_nodes, pos, my_nodelist, dst, broadcasted, 0)

    # отрисовываем сам маршрут
    route_node_list = list(((dict_nodes[dst])[1]).split(";"))
    route_node_list.pop(-1)
    route_node_list = list(map(int, route_node_list))
    route_node_list.insert(0, src)

    # вытаскиваем ребра графа
    my_edge_list = []
    for i in range(len(route_node_list) - 1):
        e = route_node_list[i], route_node_list[i + 1]
        my_edge_list.append(e)

    # Вывод конечного маршрута
    plt.clf()
    nx.draw(H, pos, node_color='#fff3a8', edge_color='#9d9d95', node_size=420, with_labels=True)
    nx.draw(H, pos, nodelist=route_node_list, node_color='#8dc2ff', edge_color='#9d9d95', node_size=420,
            with_labels=True)
    plt.savefig(constants.images_path + '1000.png')
    return route_node_list
