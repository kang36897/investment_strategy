import re

from os import path

from behave import *
from colorama import Fore, Style

from knapsack import find_highest_growth, find_lowest_draw_down, find_highest_ratio, generate_group_detail
from permutation import try_generating
from utils import collect_material, get_count_of_combination_of_length_then_one, remove_useless_combinations, \
    get_sum_of_draw_down

use_step_matcher("re")




@given("signals come from (?P<signal_file>.+), the capacity of the knapsack is (?P<target_capacity>.+)")
def step_impl(context, signal_file, target_capacity):
    """
    :type context: behave.runner.Context
    :type signal_file: str
    :type target_capacity: str
    """
    input_file = path.join(path.dirname(__file__), '../resources', signal_file)
    material, groups, signals, objectives = collect_material(input_file)
    remove_useless_combinations(objectives)
    context.objectives = objectives
    context.signals = signals
    context.target_capacity = int(target_capacity)

    target_quantity = len(signals)
    available_seeds = [0]
    available_seeds.extend([x.combination for x in material.get(1)])

    context.permutation = try_generating(available_seeds, objectives, target_quantity)
    print('permutation number: {}'.format(len(context.permutation)))


@when(
    "try to pick up the items in order to keep the sum of their growth value largest, but the selected signals should "
    "be unique in the permutation")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    possible_max_combination_length = round(context.target_capacity / 2) if context.target_capacity % 2 != 0 else round(
        context.target_capacity / 2) + 1
    highest_growth_combination = [{} for x in range(0, possible_max_combination_length + 1)]
    for team in context.permutation:
        combination_list = []
        for item in team:
            key = ','.join(item)
            combination_list.append(context.objectives.get(key))

        pocket = find_highest_growth(combination_list, context.target_capacity)
        index = get_count_of_combination_of_length_then_one(pocket[1])

        if len(highest_growth_combination[index]) == 0:
            record = []
            record.extend(pocket)
            record.append(combination_list)

            key = generate_group_detail(pocket[1], context.signals)
            highest_growth_combination[index].setdefault(key, record)
        else:
            current = [x for x in highest_growth_combination[index].values()]
            if pocket[0] > current[0][0]:
                highest_growth_combination[index].clear()

                record = []
                record.extend(pocket)
                record.append(combination_list)

                key = generate_group_detail(pocket[1], context.signals)
                highest_growth_combination[index].setdefault(key, record)

            else:
                current = [x for x in highest_growth_combination[index].values()]
                if pocket[0] == current[0][0]:
                    # print('There is a lucy record')
                    # print('orignal_record: {}'.format(
                    #     generate_group_detail(highest_growth_combination[1], context.signals)))
                    # print('lucky_record: {}'.format(
                    #     generate_group_detail(pocket[1], context.signals)))

                    key = generate_group_detail(pocket[1], context.signals)
                    if key not in highest_growth_combination[index]:
                        record = []
                        record.extend(pocket)
                        record.append(combination_list)

                        highest_growth_combination[index].setdefault(key, record)

    optimized_hrc = None
    highest_growth_combination = sorted(highest_growth_combination, key=lambda x: ([p[0] for p in x.values()])[0] if len(x) > 0 else 0)

    for i in range(possible_max_combination_length, 0, -1):
        if len(highest_growth_combination[i]) > 0:
            current = [x for x in highest_growth_combination[i].values()]

            if get_count_of_combination_of_length_then_one(current[0][1]) > 0:
                optimized_hrc = current
                break

    print('largest_growth: {}'.format(optimized_hrc[0][0]))
    context.actual_total_value = round(optimized_hrc[0][0], 2)
    context.actual = [generate_group_detail(item[1], context.signals) for item in optimized_hrc]


@when(
    "try to pick up the items in order to keep the sum of their drawback value lowest, but the selected signals "
    "should be unique in the permutation")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    possible_max_combination_length = round(context.target_capacity / 2) if context.target_capacity % 2 != 0 else round(
        context.target_capacity / 2) + 1
    lowest_draw_down_combination = [[] for x in range(0, possible_max_combination_length + 1)]
    compensation_c = max(context.objectives.values(), key=lambda c: abs(c.draw_down))

    for team in context.permutation:
        combination_list = []
        for item in team:
            key = ','.join(item)
            combination_list.append(context.objectives.get(key))

        pocket = find_lowest_draw_down(combination_list, context.target_capacity,
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
                    if get_count_of_combination_of_length_then_one(
                            pocket[1]) > get_count_of_combination_of_length_then_one(
                        lowest_draw_down_combination[index][1]):
                        lowest_draw_down_combination[index] = []
                        lowest_draw_down_combination[index].extend(pocket)
                        lowest_draw_down_combination[index].append(combination_list)

    optimized_hrc = None
    for i in range(possible_max_combination_length, 0, -1):
        if len(lowest_draw_down_combination[i]) > 0:
            optimized_hrc = lowest_draw_down_combination[i]
            break

    print('lowest_draw_back: {}'.format(get_sum_of_draw_down(optimized_hrc[1])))
    context.actual_total_value = round(get_sum_of_draw_down(optimized_hrc[1]), 2)
    context.actual = generate_group_detail(optimized_hrc[1], context.signals)


@when(
    "try to pick up the items in order to keep the sum of their ratio value largest, but the selected signals should "
    "be unique in the permutation")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    highest_ratio_combination = [[] for x in range(0, context.target_capacity + 1)]

    for team in context.permutation:
        combination_list = []
        for item in team:
            key = ','.join(item)
            combination_list.append(context.objectives.get(key))

        pocket = find_highest_ratio(combination_list, context.target_capacity)

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

    optimized_hrc = None
    for i in range(context.target_capacity, 0, -1):
        if len(highest_ratio_combination[i]) > 0:
            optimized_hrc = highest_ratio_combination[i]
            break

    print('largest_ratio: {}'.format(optimized_hrc[0]))
    context.actual_total_value = round(optimized_hrc[0], 2)
    context.actual = generate_group_detail(optimized_hrc[1], context.signals)


@then("(?P<expected_items>.+) should be put in the knapsack，and the total value would be (?P<expected_total_value>.+)")
def step_impl(context, expected_items, expected_total_value):
    """
    :type context: behave.runner.Context
    :type expected_items: str
    :type total_value: str
    """
    pattern = re.compile('\({1,}([a-z0-9,]+)\){1,}')
    expected = ','.join(sorted(['({})'.format(x) for x in pattern.findall(expected_items)]))

    print('actual: {}'.format(context.actual))
    print('expect: {}'.format(expected))

    print('actual_total_value: {}, expected_total_value: {}'.format(context.actual_total_value, expected_total_value))
    assert context.actual_total_value >= float(expected_total_value)



@then(
    "the total value would be larger than or equal with (?P<expected_total_value>.+), and maybe ("
    "?P<expected_items>.+) have been put in the knapsack")
def step_impl(context, expected_total_value, expected_items):
    """
    :type context: behave.runner.Context
    :type expected_total_value: str
    :type expected_items: str
    """
    pattern = re.compile('\({1,}([a-z0-9,]+)\){1,}')
    expected = ','.join(sorted(['({})'.format(x) for x in pattern.findall(expected_items)]))

    print(('actual: ' + Fore.GREEN+ '{}' +  Style.RESET_ALL).format(context.actual))
    print('expect: {}'.format(expected))
    if context.actual_total_value == float(expected_total_value):
        print((
                    'actual_total_value: ' + Fore.GREEN + '{}' + Style.RESET_ALL + ', expected_total_value: ' + Fore.GREEN + '{}' + Style.RESET_ALL).format(
            context.actual_total_value, expected_total_value))

    if context.actual_total_value > float(expected_total_value):
        print((
                    'actual_total_value: ' + Fore.RED + '{}' + Style.RESET_ALL + ', expected_total_value: ' + Fore.GREEN + '{}' + Style.RESET_ALL).format(
            context.actual_total_value, expected_total_value))

    assert context.actual_total_value >= float(expected_total_value)


@then(
    "the total value would be less than or equal with (?P<expected_total_value>.+), and maybe (?P<expected_items>.+) "
    "have been put in the knapsack")
def step_impl(context, expected_total_value, expected_items):
    """
    :type context: behave.runner.Context
    :type expected_total_value: str
    :type expected_items: str
    """
    pattern = re.compile('\({1,}([a-z0-9,]+)\){1,}')
    expected = ','.join(sorted(['({})'.format(x) for x in pattern.findall(expected_items)]))

    print(('actual: ' + Fore.GREEN+ '{}' +  Style.RESET_ALL).format(context.actual))
    print('expect: {}'.format(expected))

    if context.actual_total_value == float(expected_total_value):
        print((
                'actual_total_value: ' + Fore.GREEN + '{}' + Style.RESET_ALL + ', expected_total_value: ' + Fore.GREEN + '{}' + Style.RESET_ALL).format(
            context.actual_total_value, expected_total_value))

    if context.actual_total_value < float(expected_total_value):
        print((
                'actual_total_value: ' + Fore.BLUE + '{}' + Style.RESET_ALL + ', expected_total_value: ' + Fore.GREEN + '{}' + Style.RESET_ALL).format(
            context.actual_total_value, expected_total_value))

    assert context.actual_total_value <= float(expected_total_value)
