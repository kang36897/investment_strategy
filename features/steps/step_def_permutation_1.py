from os import path

import parse
from behave import register_type, given, when, then

from permutation import try_generating
from utils import collect_material


@parse.with_pattern(r"\d+")
def parse_integer(text):
    return int(text)


def parse_path(text):
    return path.abspath(path.join(path.dirname(__file__), '../resources', text))


register_type(Integer=parse_integer)
register_type(Path=parse_path)


@given('signals in "{signal_file:Path}", the quantity allowed is "{target_quantity:Integer}"')
def step_impl(context, signal_file, target_quantity):
    """
    :type context: behave.runner.Context
    """
    print('signal_file: {}'.format(signal_file))
    print('target_quantity: {}'.format(target_quantity))
    material, groups, signals, objectives = collect_material(signal_file)

    context.material = material
    context.signals = signals
    context.objectives = objectives
    context.target_quantity = target_quantity
    pass


@when('try to pick up the right items')
def step_imp(context):
    """
    :type context: behave.runner.Context
    """
    print([x for x in context.objectives.keys()])

    available_seeds = [0]
    available_seeds.extend([x.combination for x in context.material.get(1)])
    permutation = try_generating(available_seeds, context.objectives, context.target_quantity)

    actual = []
    for team in permutation:
        p = []
        for item in team:
            key = ','.join(item)
            p.append(context.objectives[key].describe_node_details(context.signals))
        actual.append(','.join(sorted(p)))

    context.actual = actual


@then("the following permutations are chosen")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    expected = set()
    for row in context.table:
        expected.add(row['permutation'])
        print('row: {}'.format(row['permutation']))

    assert len(context.actual) == len(expected), "the number of actual and expected result not match"

    for item in context.actual:

        if item not in expected:
            assert False, "item: {} not in expected result".format(item)
