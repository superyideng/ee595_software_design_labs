import math
import random
import sys


def read_from(path):
    """
    :param path: str
    :return: int, list, dict
    """
    f = open(path, 'r')
    result = {}
    num = int(f.readline().strip())
    nodes = list()
    for line in f.readlines():
        line = line.strip()
        num_arr = [int(curr) for curr in line.split()]
        nodes.append(num_arr[0])
        result[num_arr[0]] = num_arr[1:]
    return num, nodes, result


def write_output(path, array, num):
    """
    :param path: str
    :param array: list
    :param num: float
    :return: void
    """
    f = open(path, 'w')
    f.write("Final Distance of SA Method: " + str(num) + '\n')
    for e in range(len(array)):
        f.write(str(array[e]) + '\n')
    f.close()


def distance_of(pos, trace):
    """
    :param pos: dict
    :param trace: list
    :return: float
    """
    result = 0
    for i in range(1, len(trace)):
        i_pos = pos[trace[i]]
        j_pos = pos[trace[i-1]]
        result += math.sqrt(math.pow(i_pos[0] - j_pos[0], 2)
                            + math.pow(i_pos[1] - j_pos[1], 2)
                            + math.pow(i_pos[2] - j_pos[2], 2))

    i_pos = pos[trace[0]]
    j_pos = pos[trace[len(trace) - 1]]
    result += math.sqrt(math.pow(i_pos[0] - j_pos[0], 2)
                        + math.pow(i_pos[1] - j_pos[1], 2)
                        + math.pow(i_pos[2] - j_pos[2], 2))
    return result


def apply_SA(T, beta, state):
    """
    :param T: float
    :param beta: float
    :param state: list
    :return: float, list, float
    """
    distance = distance_of(city_pos, state)
    unchanged_times = 0
    accepted_increase_deltas = list()
    i_time = 0
    while T > 0.00001:
        n1, n2 = random.sample(state, 2)
        ind1, ind2 = state.index(n1), state.index(n2)
        dist = distance_of(city_pos, state)
        temp_state = state.copy()
        temp_state[ind1], temp_state[ind2] = temp_state[ind2], temp_state[ind1]
        temp_dist = distance_of(city_pos, temp_state)

        delta = (temp_dist - distance) / dist
        p = math.exp(- delta / T) if delta > 0 else 1
        if delta <= 0 or p > random.random():
            if delta > 0:
                accepted_increase_deltas.append(delta)
            state = temp_state.copy()
            distance = temp_dist
            T *= beta
            unchanged_times = 0
        else:
            unchanged_times += 1
            if unchanged_times >= 80000:
                break
        i_time += 1
    T0 = - (sum(accepted_increase_deltas) / len(accepted_increase_deltas)) / math.log(0.8)
    return distance, state, T0, i_time


def find_opt_beta(T, s):
    """
    :param T: float
    :param s: list
    :return: float, float
    """
    beta = 0.9
    opt_beta = 0.9
    opt_avg_dist = sys.maxsize

    while beta < 1:
        cur_dists = list()
        iter_list = ""
        for i in range(5):
            cur_dist, cur_state, T1, iter_time = apply_SA(T, beta, s)
            cur_dists.append(cur_dist)
            iter_list += str(iter_time) + " "
        avg_dist = sum(cur_dists) / 5
        max_dist = max(cur_dists)
        min_dist = min(cur_dists)
        print("current beta: " + str(beta))
        print("current max distance: " + str(max_dist))
        print("current min distance: " + str(min_dist))
        print("current average distance: " + str(avg_dist))
        print("iteration times for current beta: " + iter_list)
        print("\n")
        if avg_dist < opt_avg_dist:
            opt_avg_dist = avg_dist
            opt_beta = beta
        beta += 0.01
    return opt_beta, opt_avg_dist


if __name__ == '__main__':
    # extract input data from file
    filename = "input_part2.txt"
    num_cities, s, city_pos = read_from(filename)
    random.shuffle(s)

    # apply SA
    fin_dist, fin_s, computed_T0 = apply_SA(80, 0.9, s)[:3]

    # write our results into output.txt
    write_output("output_part2.txt", fin_s, fin_dist)
    print("specified T0 is: " + str(computed_T0) + "\n")

    # find the optimal beta
    opt_b, opt_avg_d = find_opt_beta(computed_T0, s)

