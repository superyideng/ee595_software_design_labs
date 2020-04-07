import math


def read_from(path):
    """
    :param path: str, path of file to be read
    :return: int, number of nodes
             list, position information of each node
    """
    f = open(path, 'r')
    result = list()
    num = int(f.readline().strip())
    for line in f.readlines():
        line = line.strip()
        num_arr = [int(curr) for curr in line.split()]
        result.append(num_arr[1:])
    return num, result


def generate_cycle(curdict, n1, n2):
    """
    :param curdict: dict, adjacency list
    :param n1: int, start node
    :param n2: int, end node
    :return: bool, whether or not adding the edge generates a cycle
    """
    if n1 not in curdict.keys() or n2 not in curdict.keys():
        return False
    temp = curdict[n1].copy()
    visited = set()
    while len(temp) > 0:
        node = temp.pop()
        if node == n2:
            return True
        if node in curdict.keys() and node not in visited:
            temp.extend(curdict[node])
            visited.add(node)
    return False


def write_output(path, array):
    """
    :param path: str, path of output file
    :param array: list
    :return: void
    """
    f = open(path, 'w')
    f.write("The total number of edges: " + str(len(array)) + '\n')
    for e in range(len(array)):
        f.write(str(array[e][0]) + ' ' + str(array[e][1]) + '\n')
    f.close()


if __name__ == '__main__':
    # extract input data from file
    filename = "input_part1.txt"
    num_cities, city_pos = read_from(filename)

    # generate distance array whose elem = [start, end, distance between]
    distances = []
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            i_pos = city_pos[i]
            j_pos = city_pos[j]
            cur_dist = math.sqrt(math.pow(i_pos[0] - j_pos[0], 2) + math.pow(i_pos[1] - j_pos[1], 2))
            distances.append([i, j, cur_dist])
    distances.sort(key=lambda dist: dist[2])

    # loop over all the distances and decide whether to add to result edges
    adjacency = {}
    edges = list()
    curr_ind = 0
    while len(edges) < num_cities - 1:
        start, end = distances[curr_ind][0], distances[curr_ind][1]

        if not generate_cycle(adjacency, start, end):
            start_neighbors = adjacency[start] if start in adjacency.keys() else list()
            end_neighbors = adjacency[end] if end in adjacency.keys() else list()
            start_neighbors.append(end)
            end_neighbors.append(start)
            adjacency[start] = start_neighbors
            adjacency[end] = end_neighbors
            edges.append([start, end])

        curr_ind += 1

    # write output to "output_part1.txt"
    write_output("output_part1.txt", edges)


