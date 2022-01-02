# -*- coding:utf-8 -*-
import re
from os import path

from behave import *

from knapsack import find_highest_growth, find_lowest_draw_down, find_highest_ratio, generate_group_detail
from utils import collect_material


@given("signals in {signal_file}, the capacity of the knapsack is {target_capacity}")
def step_impl(context, signal_file, target_capacity):
    """
    :type context: behave.runner.Context
    :type signal_file: str
    :type target_capacity: str
    """

    input_file = path.join(path.dirname(__file__), '../resources', signal_file)
    material, groups, signals, objectives = collect_material(input_file)
    context.objectives = objectives
    context.signals = signals
    context.target_capacity = int(target_capacity)


@when("try to pick up the items in order to keep the sum of their growth value largest")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    combination_list = []
    for key, value in context.objectives.items():
        combination_list.append(value)
    pocket = find_highest_growth(combination_list, context.target_capacity)
    print('largest_growth: {}'.format(pocket[0]))
    context.actual = generate_group_detail(pocket[1], context.signals)


@when("try to pick up the items in order to keep the sum of their drawback value lowest")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    combination_list = []
    for key, value in context.objectives.items():
        combination_list.append(value)

    compensation_c = max(context.objectives.values(), key=lambda c: abs(c.draw_down))
    pocket = find_lowest_draw_down(combination_list, context.target_capacity,
                                   compensation=abs(compensation_c.draw_down))
    print('lowest_draw_back: {}'.format(abs(compensation_c.draw_down) * context.target_capacity - pocket[0]))
    context.actual = generate_group_detail(pocket[1], context.signals)


@when("try to pick up the items in order to keep the sum of their ratio value largest")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    combination_list = []
    for key, value in context.objectives.items():
        combination_list.append(value)

    pocket = find_highest_ratio(combination_list, context.target_capacity)
    print('largest_ratio: {}'.format(pocket[0]))
    context.actual = generate_group_detail(pocket[1], context.signals)


@then("{expected_items} should be in the knapsack")
def step_impl(context, expected_items):
    """
    :type context: behave.runner.Context
    :type expected_items: str
    """
    pattern = re.compile('\({1,}([a-z0-9,]+)\){1,}')
    expected = ','.join(sorted(['({})'.format(x) for x in pattern.findall(expected_items)]))

    print('actual: {}'.format(context.actual))
    print('expect: {}'.format(expected))

    assert context.actual == expected
