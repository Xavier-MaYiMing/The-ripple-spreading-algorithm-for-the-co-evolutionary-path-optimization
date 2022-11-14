#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/3 9:24
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com.com
# @File    : RSA4CEPO.py
# @Statement : The ripple-spreading algorithm for the co-evolutionary path optimization
# @Reference : HU X B,ZHANG M K,ZHANG Q,et al.Co-evolutionary path optimization by ripple-spreading algorithm[J].Transportation Research:Part B,2017,106:411-432.
import matplotlib.pyplot as plt
import math
import random
import copy
from matplotlib.patches import Circle


def find_neighbor(network):
    """
    Find the neighbor of each node
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :return: {node 1: [the neighbor nodes of node 1], ...}
    """
    nn = len(network)
    neighbor = []
    for i in range(nn):
        neighbor.append(list(network[i].keys()))
    return neighbor


def find_speed(network, neighbor):
    """
    Find the ripple spreading speed
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param neighbor: the neighbor set
    :return:
    """
    speed = 1e10
    for i in range(len(network)):
        for j in neighbor[i]:
            speed = min(speed, network[i][j])
    return speed


def routing_environmental_dynamics(network, t, orad, ospeed, x, y):
    """
    The obstacle moves from the lower right corner to the upper left corner
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param t: current time index
    :param orad: the radius of the obstacle
    :param ospeed: the moving speed of the obstacle
    :param x: the x axis coordinates of nodes
    :param y: the y axis coordinates of nodes
    :return:
    """
    active_node = [i for i in range(len(network))]
    inactive_node = []
    current_coord = [90 - ospeed * t / math.sqrt(2), ospeed * t / math.sqrt(2)]  # the current position of the obstacle
    new_network = copy.deepcopy(network)
    for i in range(len(x)):
        if math.sqrt((x[i] - current_coord[0]) ** 2 + (
                y[i] - current_coord[1]) ** 2) <= orad:  # the node is within the obstancle range
            inactive_node.append(i)
            active_node.remove(i)
    for i in range(len(network)):
        if i in inactive_node:
            new_network[i] = {}
        else:
            need_to_pop = []
            for j in network[i].keys():
                if j in inactive_node:
                    need_to_pop.append(j)
            for j in need_to_pop:
                new_network[i].pop(j)
    return new_network, active_node, inactive_node


def draw_pic(x, y, network, orad, ospeed, t, path, v):
    """
    Plot the result of the CEPO
    :param x: the x axis coordinates of nodes
    :param y: the y axis coordinates of nodes
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param orad: the radius of the obstacle
    :param ospeed: the moving speed of the obstacle
    :param t: time index
    :param path: the shortest path output by the RSA
    :param v: the ripple spreading speed
    """
    path_cost = [0]
    for i in range(len(path) - 1):
        path_cost.append(path_cost[-1] + network[path[i]][path[i + 1]])
    for time in range(t + 1):
        temp_path = []
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # Plot the network
        for i in range(len(network)):
            for j in network[i].keys():
                temp_x = [x[i], x[j]]
                temp_y = [y[i], y[j]]
                plt.plot(temp_x, temp_y, 'springgreen', linewidth=2)
        plt.scatter(x, y, c='springgreen', s=100)
        plt.scatter(x[0], y[0], c='red', s=100)  # plot the source node
        plt.scatter(x[-1], y[-1], c='black', s=100)  # plot the destination node

        # Plot the obstacle
        current_coord = [90 - ospeed * time / math.sqrt(2), ospeed * time / math.sqrt(2)]
        cir = Circle(xy=(current_coord), radius=orad, alpha=0.5)
        ax.add_patch(cir)
        for i in range(len(path)):
            if time * v >= path_cost[i]:
                temp_path.append(path[i])
        if len(temp_path) > 1:
            for i in range(len(temp_path) - 1):
                temp_x = [x[temp_path[i]], x[temp_path[i + 1]]]
                temp_y = [y[temp_path[i]], y[temp_path[i + 1]]]
                plt.plot(temp_x, temp_y, c='navy', linewidth=2)
        plt.xticks([])
        plt.yticks([])
        name = str(time) + '.png'
        plt.savefig(name, dpi=400, bbox_inches='tight')
        plt.show()


def init_network():
    """
    Randomly initialize the network with 100 nodes
    """
    x = []
    y = []
    x_num = 10
    y_num = 10
    p1 = 0.7
    p2 = 0.05
    p3 = 0.03
    connection_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                       99, 98, 97, 96, 95, 94, 93, 92, 91, 90,
                       10, 20, 30, 40, 50, 60, 70, 80,
                       19, 29, 39, 49, 59, 69, 79, 89]
    for i in range(x_num):
        for j in range(y_num):
            x.append(i * 10 + random.uniform(-2, 2))
            y.append(j * 10 + random.uniform(-2, 2))
    network = {}
    for i in range(100):
        network[i] = {}
        for j in range(100):
            if i != j and i in connection_list and j in connection_list and math.sqrt(
                    (x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) < 15:
                network[i][j] = math.sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2)
    for i in range(100):
        for j in range(100):
            if (abs(i - j) == 1 or abs(i - j) == x_num or abs(i - j) == y_num) and \
                    math.sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) < 20:  # 横或竖相连
                if random.random() < p1:
                    temp_num = math.sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2)
                    network[i][j] = temp_num
                    network[j][i] = temp_num
            if (abs(i - j) == x_num + 1 or abs(i - j) == x_num - 1 or abs(i - j) == y_num + 1 or abs(i - j) == y_num - 1) \
                    and math.sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) < 20:  # 对角线相连
                if random.random() < p2:
                    temp_num = math.sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2)
                    network[i][j] = temp_num
                    network[j][i] = temp_num
            if (abs(i - j) == 2 or abs(i - j) == 2 * x_num or abs(i - j) == 2 * y_num) \
                    and math.sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2) < 30 and i in connection_list \
                    and j in connection_list:  # 两横线或两竖线相连
                if random.random() < p3:
                    temp_num = math.sqrt((x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2)
                    network[i][j] = temp_num
                    network[j][i] = temp_num
    # Plot the network
    for i in range(len(network)):
        for j in network[i].keys():
            temp_x = [x[i], x[j]]
            temp_y = [y[i], y[j]]
            plt.plot(temp_x, temp_y, 'springgreen', linewidth=2)
    plt.scatter(x, y, c='springgreen', s=100)
    plt.scatter(x[0], y[0], c='red', s=100)  # plot the source node
    plt.scatter(x[-1], y[-1], c='black', s=100)  # plot the destination node
    plt.show()
    return network, x, y


def main(network, source, destination, x, y, orad, ospeed):
    """
    The main function of the RSA4CEPO
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param source: the source node
    :param destination: the destination node
    :param x: the x axis coordinates of nodes
    :param y: the y axis coordinates of nodes
    :param orad: the radius of the obstacle
    :param ospeed: the moving speed of the obstacle
    """
    # Step 1. Initialization
    nn = len(network)  # node number
    neighbor = find_neighbor(network)  # the neighbor set
    v = find_speed(network, neighbor)  # the ripple spreading speed
    t = 0  # simulated time index
    nr = 0  # the current number of ripples - 1
    epicenter_set = []  # epicenter set
    radius_set = []  # radius set
    length_set = []  # length set
    path_set = []  # path set
    state_set = []  # state set, state_set[i] = 1, 2, 3 means ripple i is waiting, active, or dead
    omega = {}  # the set that records the ripple generated at each node
    for node in range(nn):
        omega[node] = -1

    # Step 2. Initialize the first ripple
    epicenter_set.append(source)
    radius_set.append(0)
    length_set.append(0)
    path_set.append([source])
    state_set.append(2)
    omega[source] = nr
    nr += 1

    # Step 3. The main loop
    while omega[destination] == -1:
        # Step 3.1. If there is no feasible solution
        flag = True
        for state in state_set:
            if state == 1 or state == 2:
                flag = False
                break
        if flag:
            print('There is no feasible solution!')
            return {}

        # Step 3.2. Time updates
        t += 1
        incoming_ripples = {}

        # Step 3.3. Update the obstacle based on the given routing environmental dynamics
        new_network, active_node, inactive_node = routing_environmental_dynamics(network, t, orad, ospeed, x, y)
        for i in range(nr):  # waiting nodes -> active nodes
            if state_set[i] == 1 and epicenter_set[i] in active_node:
                state_set[i] = 2

        for i in range(nr):
            if state_set[i] == 2:
                # Step 3.4. Active ripple spreads out
                radius_set[i] += v
                epicenter = epicenter_set[i]
                radius = radius_set[i]
                path = path_set[i]
                length = length_set[i]

                # Step 3.5. New incoming ripples
                for node in neighbor[epicenter]:
                    if omega[node] == -1:  # the node has not been visited yet
                        temp_length = network[epicenter][node]
                        if temp_length <= radius < temp_length + v:
                            # Step 3.6. Accessible node
                            if node in active_node:
                                temp_path = path.copy()
                                temp_path.append(node)
                                if node in incoming_ripples.keys():
                                    incoming_ripples[node].append({
                                        'path': temp_path,
                                        'radius': radius - temp_length,
                                        'length': length + temp_length,
                                        'state': 2
                                    })
                                else:
                                    incoming_ripples[node] = [{
                                        'path': temp_path,
                                        'radius': radius - temp_length,
                                        'length': length + temp_length,
                                        'state': 2
                                    }]

                            # Step 3.7. Inaccessible node
                            if node in inactive_node:
                                temp_path = path.copy()
                                temp_path.append(node)
                                if node in incoming_ripples.keys():
                                    incoming_ripples[node].append({
                                        'path': temp_path,
                                        'radius': 0,
                                        'length': length + temp_length,
                                        'state': 1
                                    })
                                else:
                                    incoming_ripples[node] = [{
                                        'path': temp_path,
                                        'radius': 0,
                                        'length': length + temp_length,
                                        'state': 1
                                    }]

        # Step 3.8. Generate new ripples
        for node in incoming_ripples.keys():
            if node in active_node:
                new_ripple = sorted(incoming_ripples[node], key=lambda x: x['radius'], reverse=True)[
                    0]  # the ripple with the largest radius is selected
            else:
                new_ripple = sorted(incoming_ripples[node], key=lambda x: x['length'])[
                    0]  # the ripple with the smallest length is selected
            epicenter_set.append(node)
            radius_set.append(new_ripple['radius'])
            length_set.append(new_ripple['length'])
            path_set.append(new_ripple['path'])
            state_set.append(new_ripple['state'])
            omega[node] = nr
            nr += 1

        # Step 3.9. Determine whether the ripple turns to be dead
        for i in range(nr):
            if state_set[i] == 1 or state_set[i] == 2:
                flag = True
                epicenter = epicenter_set[i]
                for node in neighbor[epicenter]:
                    if omega[node] == -1:
                        flag = False
                        break
                if flag:
                    state_set[i] = 3

    # Step 4. Plot the path
    ripple = omega[destination]
    # draw_pic(x, y, network, orad, ospeed, t, path_set[ripple], v)
    return {'shortest path': path_set[ripple], 'length': length_set[ripple]}


if __name__ == '__main__':
    network, x, y = init_network()
    s = 0
    d = 99
    orad = 15  # obstacle radius
    ospeed = 6  # obstacle speed
    print(main(network, s, d, x, y, orad, ospeed))
