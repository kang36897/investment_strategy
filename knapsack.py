# -*- coding:utf-8 -*-

from utils import get_sum_of_draw_down, get_sum_of_growth, generate_group_detail, describe_desired_group


def extend_groups(m_groups):
    t = set()
    for c in m_groups:
        t.update(c.detail)
    return t


def find_highest_growth(combination_list, t_capacity):
    ordered_combination_list = sorted(combination_list, key=lambda x: x.growth)
    c_length = len(ordered_combination_list)
    knapsack = [[[0, []] for y in range(0, t_capacity + 1)] for x in range(0, c_length + 1)]

    for i in range(1, c_length + 1):
        for j in range(1, t_capacity + 1):

            c = ordered_combination_list[i - 1]
            if c.weight <= j:
                l_pocket = knapsack[i - 1][j - c.weight]
                v = abs(c.growth) + l_pocket[0]

                p_pocket = knapsack[i - 1][j]

                if v > p_pocket[0]:
                    # consider some combinations may have an intersection
                    if extend_groups(l_pocket[1]).isdisjoint(c.detail):
                        m_groups = [c]
                        m_groups.extend(l_pocket[1])
                        knapsack[i][j] = [v, m_groups]
                    else:
                        knapsack[i][j] = p_pocket
                else:
                    knapsack[i][j] = p_pocket
            else:
                knapsack[i][j] = knapsack[i - 1][j]

    return knapsack[c_length][t_capacity]


def find_lowest_draw_down(combination_list, t_capacity, compensation=1000_000):
    ordered_combination_list = sorted(combination_list, key=lambda x: compensation + x.draw_down)
    c_length = len(ordered_combination_list)
    knapsack = [[[0, []] for y in range(0, t_capacity + 1)] for x in range(0, c_length + 1)]

    for i in range(1, c_length + 1):
        for j in range(1, t_capacity + 1):

            c = ordered_combination_list[i - 1]
            if c.weight <= j:
                l_pocket = knapsack[i - 1][j - c.weight]
                v = compensation + c.draw_down + l_pocket[0]

                p_pocket = knapsack[i - 1][j]

                if v > p_pocket[0]:
                    # consider some combinations may have an intersection
                    if extend_groups(l_pocket[1]).isdisjoint(c.detail):
                        m_groups = [c]
                        m_groups.extend(l_pocket[1])
                        knapsack[i][j] = [v, m_groups]
                    else:
                        knapsack[i][j] = p_pocket
                else:
                    knapsack[i][j] = p_pocket
            else:
                knapsack[i][j] = knapsack[i - 1][j]

    return knapsack[c_length][t_capacity]


def find_highest_ratio(combination_list, t_capacity):
    ordered_combination_list = sorted(combination_list, key=lambda x: abs(x.growth) / abs(x.draw_down))
    c_length = len(ordered_combination_list)
    knapsack = [[[0, []] for y in range(0, t_capacity + 1)] for x in range(0, c_length + 1)]

    for i in range(1, c_length + 1):
        for j in range(1, t_capacity + 1):

            c = ordered_combination_list[i - 1]
            if c.weight <= j:
                l_pocket = knapsack[i - 1][j - c.weight]

                sum_growth = abs(c.growth) + get_sum_of_growth(l_pocket[1])
                sum_draw_down = abs(c.draw_down) + get_sum_of_draw_down(l_pocket[1])

                v = sum_growth / sum_draw_down

                p_pocket = knapsack[i - 1][j]

                if v > p_pocket[0]:
                    # consider some combinations may have an intersection
                    if extend_groups(l_pocket[1]).isdisjoint(c.detail):
                        m_groups = [c]
                        m_groups.extend(l_pocket[1])
                        knapsack[i][j] = [v, m_groups]
                    else:
                        knapsack[i][j] = p_pocket
                else:
                    knapsack[i][j] = p_pocket
            else:
                knapsack[i][j] = knapsack[i - 1][j]

    return knapsack[c_length][t_capacity]


def try_finding(combination_list, t_capacity, signals):
    pocket = find_highest_growth(combination_list, t_capacity)
    print('group {} with the highest growth: '.format(
        generate_group_detail(pocket[1], signals)))
    describe_desired_group(pocket[1])

    pocket = find_lowest_draw_down(combination_list, t_capacity)
    print('group {} with the lowest draw_down: '.format(
        generate_group_detail(pocket[1], signals)))
    describe_desired_group(pocket[1])

    pocket = find_highest_ratio(combination_list, t_capacity)
    print('group {} with the highest ratio: '.format(
        generate_group_detail(pocket[1], signals)))
    describe_desired_group(pocket[1])
