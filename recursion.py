# -*- coding:utf-8 -*-
import math

from utils import describe_desired_group


def generate_group_detail(selected_group, nodes):
    detail = []
    for c in selected_group:
        snippet = c.describe_node_details(nodes)
        detail.append(snippet)

    return ','.join(detail)


def try_find(matched_combinations, g_capacity, materials, c_capacity=-1, bowl=[], current_bucket=set()):
    if c_capacity == 0:
        return

    if g_capacity in materials:
        available_combinations = materials[g_capacity]

        for c in available_combinations:
            if not c.detail.isdisjoint(current_bucket):
                continue

            cloned_bowl = list(bowl)
            cloned_bowl.append(c)
            matched_combinations.append(c)

        remaining = materials.copy()
        del remaining[g_capacity]

        try_find(matched_combinations, g_capacity, remaining, c_capacity=g_capacity - 1)
        return

    else:

        if c_capacity == -1:
            try_find(matched_combinations, g_capacity, materials, c_capacity=g_capacity - 1)
            return

        if c_capacity in materials:
            available_combinations = materials[c_capacity]
            for c in available_combinations:
                if not c.detail.isdisjoint(current_bucket):
                    continue

                cloned_bucket = set(current_bucket)
                cloned_bucket.update(c.detail)

                cloned_bowl = list(bowl)
                cloned_bowl.append(c)

                if g_capacity == len(cloned_bucket):
                    matched_combinations.append(cloned_bowl)
                    continue
                else:
                    try_find(matched_combinations, g_capacity, materials.copy(),
                             c_capacity=g_capacity - len(cloned_bucket),
                             bowl=cloned_bowl, current_bucket=cloned_bucket)

            remaining = materials.copy()
            del remaining[c_capacity]

            try_find(matched_combinations, g_capacity, remaining, c_capacity=c_capacity - 1, bowl=bowl,
                     current_bucket=current_bucket)
        else:
            try_find(matched_combinations, g_capacity, materials.copy(), c_capacity=c_capacity - 1,
                     bowl=bowl, current_bucket=current_bucket)


def find_desired_combination(material, groups, signals, target_capacity):
    match_combinations = []
    try_find(match_combinations, target_capacity, material)

    g_with_lowest_drawback = None
    g_with_highest_growth = None
    g_with_highest_ratio = None

    lowest_drawback = math.inf
    highest_growth = 0
    highest_ratio = 0

    matched_groups = set()
    for bowl in match_combinations:

        drawback = sum([abs(groups[c.id].draw_down) for c in bowl])
        if drawback < lowest_drawback:
            g_with_lowest_drawback = bowl

        growth = sum([abs(groups[c.id].growth) for c in bowl])
        if growth > highest_growth:
            g_with_highest_growth = bowl

        ratio = growth / drawback
        if ratio > highest_ratio:
            g_with_highest_ratio = bowl

        matched_groups.add(','.join(map(str, sorted([x.id for x in bowl]))))

    print('groups meet requirement: {}'.format(len(matched_groups)))

    print('group {} with the highest growth: '.format(
        generate_group_detail(g_with_highest_growth, signals)))
    describe_desired_group(g_with_highest_growth)

    print('group {} with the lowest draw_down: '.format(
        generate_group_detail(g_with_lowest_drawback, signals)))
    describe_desired_group(g_with_lowest_drawback)

    print('group {} with the highest ratio: '.format(
        generate_group_detail(g_with_highest_ratio, signals)))
    describe_desired_group(g_with_highest_ratio)

    #
    # print('group with the highest ratio: {}'.format(generate_group_detail(g_with_highest_ratio, signals)))
