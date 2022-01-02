# -*- coding:utf-8 -*-
from os import path

import pandas as pd
from colorama import Fore, Style

from node import Node, Combination


def collect_material(input_file):
    df = pd.read_excel(input_file)

    signals = {}
    for idx, val in enumerate(df.columns[1:-2]):
        id = idx + 1
        n = Node(id, val)
        signals.setdefault(id, n)

    groups = {}
    material = {}
    objectives = {}

    for data in df.itertuples(index=False):
        row_length = len(data)
        c = Combination(data[0])

        for i in range(1, row_length - 2):
            if data[i] == 1:
                c.add_node(i)

        c.draw_down = data[-2]
        c.growth = data[-1]

        objectives.setdefault(c.combination, c)
        if c.length not in material:
            material[c.length] = []

        container = material[c.length]

        container.append(c)
        groups[c.id] = c

    return material, groups, signals, objectives


def get_sum_of_draw_down(m_groups):
    sum_of_draw_down = 0
    for c in m_groups:
        sum_of_draw_down += abs(c.draw_down)
    return sum_of_draw_down


def get_sum_of_growth(m_groups):
    sum_of_growth = 0
    for c in m_groups:
        sum_of_growth += abs(c.growth)
    return sum_of_growth


def generate_group_detail(selected_group, signals):
    return ','.join(sorted([c.describe_node_details(signals) for c in selected_group]))


def get_count_of_combination_of_length_then_one(selected_group):
    return sum([1 if c.length > 1 else 0  for c in selected_group])


def remove_useless_combinations(objectives):
    useless_combinations = []

    for key, value in objectives.items():
        node_list = key.split(',')
        if len(node_list) == 1:
            continue;

        useless_flag = 0
        sum_draw_down = 0
        sum_growth = 0

        for cid in node_list:
            c = objectives[cid]

            sum_draw_down += abs(c.draw_down)
            sum_growth += abs(c.growth)

        if sum_growth == abs(value.growth) and sum_draw_down == abs(value.draw_down):
            useless_combinations.append(key)

    for key in useless_combinations:
        del objectives[key]

def describe_desired_group(pocket):
    desc = ''
    sumOfGrowth = get_sum_of_growth(pocket)
    sumOfDrawDown = get_sum_of_draw_down(pocket)
    desc += 'growth: ' + Fore.RED + '{}'.format(round(sumOfGrowth, 2)) + Style.RESET_ALL
    desc += ' draw_down: ' + Fore.GREEN + '{} '.format(round(sumOfDrawDown, 2)) + Style.RESET_ALL
    desc += ' ratio: ' + Fore.BLUE + '{}'.format(round(sumOfGrowth / sumOfDrawDown, 2)) + Style.RESET_ALL
    print(desc)


def analyze_signals_and_combination(objectives, signals):
    for key, value in objectives.items():
        node_list = key.split(',')
        if len(node_list) == 1:
            continue;

        sum_draw_down = 0
        sum_growth = 0

        for cid in node_list:
            c = objectives[cid]

            sum_draw_down += abs(c.draw_down)
            sum_growth += abs(c.growth)

        description = 'For combination {}:'.format(
            value.describe_node_details(signals))

        if sum_growth == abs(value.growth):
            description += Fore.BLUE + ' its growth equals with the sum of the growth of its individual signals ' + Style.RESET_ALL
        else:
            if abs(value.growth) > sum_growth:
                description += Fore.GREEN + ' its growth larger than the sum of the growth of its individual signals ' + Style.RESET_ALL
            else:
                description += Fore.RED + ' its growth less than the sum of the growth of its individual signals   ' + Style.RESET_ALL

        if sum_draw_down == abs(value.draw_down):
            description += Fore.BLUE + ' its draw_down equals the sum of the draw_down of its individual signals ' + Style.RESET_ALL
        else:
            if abs(value.draw_down) < sum_draw_down:
                description += Fore.GREEN + ' its draw_down less than the sum of the draw_down of its individual signals ' + Style.RESET_ALL
            else:
                description += Fore.RED + ' its draw_down larger than the sum of the draw_down of its individual signals ' + Style.RESET_ALL

        print(description)


if __name__ == '__main__':
    input_directory = path.abspath("inputs")
    input_file = path.join(input_directory, 'performance.xlsx')

    material, groups, signals, objectives = collect_material(input_file)
    analyze_signals_and_combination(objectives, signals)
