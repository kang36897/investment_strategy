# -*- coding:utf-8 -*-

import time
from os import path
from colorama import Fore, Style
from knapsack import find_highest_growth, generate_group_detail, \
    describe_desired_group, find_lowest_draw_down, find_highest_ratio
from permutation import try_generating
from utils import collect_material, get_count_of_combination_of_length_then_one, analyze_signals_and_combination,get_sum_of_growth, get_sum_of_draw_down


def populate_highest_growth_combination_matrix(highest_growth_combination, combination_list, target_capacity, signals):
    pocket = find_highest_growth(combination_list, target_capacity)
    index = get_count_of_combination_of_length_then_one(pocket[1])
    if len(highest_growth_combination[index]) == 0:
        record = []
        record.extend(pocket)
        record.append(combination_list)

        key = generate_group_detail(pocket[1], signals)
        highest_growth_combination[index].setdefault(key, record)
    else:
        current = [x for x in highest_growth_combination[index].values()]
        if pocket[0] > current[0][0]:
            highest_growth_combination[index].clear()

            record = []
            record.extend(pocket)
            record.append(combination_list)

            key = generate_group_detail(pocket[1], signals)
            highest_growth_combination[index].setdefault(key, record)

        else:
            current = [x for x in highest_growth_combination[index].values()]
            if pocket[0] == current[0][0]:

                key = generate_group_detail(pocket[1], signals)
                if key not in highest_growth_combination[index]:
                    record = []
                    record.extend(pocket)
                    record.append(combination_list)

                    highest_growth_combination[index].setdefault(key, record)


def show_highest_growth_combinations_info(highest_growth_combination, signals):
    print('permutation : {}'.format(generate_group_detail(highest_growth_combination[2], signals)))
    print(('group {} with '+ Fore.GREEN  + 'the highest growth'+ Style.RESET_ALL + ': ').format(
        generate_group_detail(highest_growth_combination[1], signals)))
    describe_desired_group(highest_growth_combination[1])
    print('\n')


def pick_up_optimized_combinations_for_highest_growth(highest_growth_combination, possible_max_combination_length,
                                                      signals):
    optimized_hrc = None
    highest_growth_combination = sorted(highest_growth_combination,
                                        key=lambda x: ([p[0] for p in x.values()])[0] if len(x) > 0 else 0)
    for i in range(possible_max_combination_length, 0, -1):
        if len(highest_growth_combination[i]) > 0:
            current = [x for x in highest_growth_combination[i].values()]

            if get_count_of_combination_of_length_then_one(current[0][1]) > 0:
                optimized_hrc = current
                break

    optimized_hrc = sorted(optimized_hrc, key = lambda x: round(get_sum_of_growth(x[2]) / get_sum_of_draw_down(x[2]), 2), reverse=True)

    for item in optimized_hrc:
        show_highest_growth_combinations_info(item, signals)


def populate_lowest_draw_down_combination_matrix(lowest_draw_down_combination, combination_list, target_capacity,
                                                 compensation_c):
    pocket = find_lowest_draw_down(combination_list, target_capacity,
                                   compensation=abs(compensation_c.draw_down))

    index = get_count_of_combination_of_length_then_one(pocket[1])

    if len(lowest_draw_down_combination[index]) == 0:
        lowest_draw_down_combination[index] = []
        lowest_draw_down_combination[index].extend(pocket)
        lowest_draw_down_combination[index].append(combination_list)
    else:
        if pocket[0] > lowest_draw_down_combination[index][0]:
            lowest_draw_down_combination[index] = []
            lowest_draw_down_combination[index].extend(pocket)
            lowest_draw_down_combination[index].append(combination_list)
        else:
            if pocket[0] == lowest_draw_down_combination[index][0]:
                if get_count_of_combination_of_length_then_one(pocket[1]) > get_count_of_combination_of_length_then_one(
                        lowest_draw_down_combination[index][1]):
                    lowest_draw_down_combination[index] = []
                    lowest_draw_down_combination[index].extend(pocket)
                    lowest_draw_down_combination[index].append(combination_list)


def show_lowest_draw_down_combinations_info(lowest_draw_down_combination, signals):
    print('permutation : {}'.format(generate_group_detail(lowest_draw_down_combination[2], signals)))
    print(('group {} with '+ Fore.GREEN  + 'the lowest draw_down'+  Style.RESET_ALL + ': ').format(
        generate_group_detail(lowest_draw_down_combination[1], signals)))
    describe_desired_group(lowest_draw_down_combination[1])
    print('\n')


def pick_up_optimized_combinations_for_lowest_draw_down(lowest_draw_down_combination, possible_max_combination_length,
                                                        signals):
    optimized_hrc = None
    for i in range(possible_max_combination_length, 0, -1):
        if len(lowest_draw_down_combination[i]) > 0:
            optimized_hrc = lowest_draw_down_combination[i]
            break

    show_lowest_draw_down_combinations_info(optimized_hrc, signals)


def populate_highest_ratio_combination_matrix(highest_ratio_combination, combination_list, target_capacity):
    pocket = find_highest_ratio(combination_list, target_capacity)
    index = sum([c.length for c in pocket[1]])
    if len(highest_ratio_combination[index]) == 0:
        highest_ratio_combination[index] = []
        highest_ratio_combination[index].extend(pocket)
        highest_ratio_combination[index].append(combination_list)
    else:
        if pocket[0] > highest_ratio_combination[index][0]:
            highest_ratio_combination[index] = []
            highest_ratio_combination[index].extend(pocket)
            highest_ratio_combination[index].append(combination_list)
        else:
            if pocket[0] == highest_ratio_combination[index][0]:
                if get_count_of_combination_of_length_then_one(
                        pocket[1]) > get_count_of_combination_of_length_then_one(
                    highest_ratio_combination[index][1]):
                    highest_ratio_combination[index] = []
                    highest_ratio_combination[index].extend(pocket)
                    highest_ratio_combination[index].append(combination_list)


def pick_up_optimized_combinations_for_highest_ratio(highest_ratio_combination, target_capacity, signals):
    optimized_hrc = None
    for i in range(target_capacity, 0, -1):
        if len(highest_ratio_combination[i]) > 0:
            optimized_hrc = highest_ratio_combination[i]
            break

    print('permutation : {}'.format(generate_group_detail(optimized_hrc[2], signals)))
    print(('group {} with '+ Fore.GREEN  +'the highest ratio' + Style.RESET_ALL+': ').format(
        generate_group_detail(optimized_hrc[1], signals)))
    describe_desired_group(optimized_hrc[1])
    print('\n')


if __name__ == '__main__':
    input_directory = path.abspath("inputs")
    input_file = path.join(input_directory, 'signal_10_7.xlsx')

    material, groups, signals, objectives = collect_material(input_file)
    analyze_signals_and_combination(objectives, signals)
    print('\n')

    target_capacity = 7

    if target_capacity > len(signals):
        raise Exception('target capacity is larger than the available signals')

    start_time = time.time()
    target_quantity = len(signals)

    available_seeds = [0]
    available_seeds.extend([x.combination for x in material.get(1)])

    permutation = try_generating(available_seeds, objectives, target_quantity)
    print('permutation number: {}'.format(len(permutation)))
    print('\n')

    possible_max_combination_length = round(target_capacity / 2) if target_capacity % 2 != 0 else round(
        target_capacity / 2) + 1
    highest_growth_combination = [{} for x in range(0, possible_max_combination_length + 1)]

    lowest_draw_down_combination = [[] for x in range(0, possible_max_combination_length + 1)]
    compensation_c = max(objectives.values(), key=lambda c: abs(c.draw_down))

    highest_ratio_combination = [[] for x in range(0, target_capacity + 1)]

    for team in permutation:
        combination_list = []
        for item in team:
            key = ','.join(item)
            combination_list.append(objectives.get(key))

        populate_highest_growth_combination_matrix(highest_growth_combination, combination_list, target_capacity,
                                                   signals)
    pick_up_optimized_combinations_for_highest_growth(highest_growth_combination, possible_max_combination_length,
                                                      signals)

    for team in permutation:
        combination_list = []
        for item in team:
            key = ','.join(item)
            combination_list.append(objectives.get(key))

        populate_lowest_draw_down_combination_matrix(lowest_draw_down_combination, combination_list, target_capacity,
                                                     compensation_c)

    pick_up_optimized_combinations_for_lowest_draw_down(lowest_draw_down_combination, possible_max_combination_length,
                                                        signals)

    for team in permutation:
        combination_list = []
        for item in team:
            key = ','.join(item)
            combination_list.append(objectives.get(key))
        populate_highest_ratio_combination_matrix(highest_ratio_combination, combination_list, target_capacity)

    pick_up_optimized_combinations_for_highest_ratio(highest_ratio_combination, target_capacity, signals)

    print("time consuming: --- %s seconds ---" % (time.time() - start_time))
