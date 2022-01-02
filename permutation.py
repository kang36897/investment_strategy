# -*- coding:utf-8 -*-

def team(existing_teams, newbie):
    p = []
    for tea in existing_teams:
        t = []
        t.extend(tea)
        t.append([newbie])
        p.append(t)

    return p


def partner(existing_teams, newbie, objectives):
    p = []

    for team in existing_teams:
        fixed_groups = []
        for i in range(len(team)):
            group = team[i]
            if len(group) >= 2:
                if ','.join(group) in objectives:
                    fixed_groups.append(group)
                else:
                    break
                continue

            else:
                t = [newbie]
                t.extend(group)
                n_group = sorted(t)
                if ','.join(n_group) in objectives:
                    n_team = []
                    n_team.extend(fixed_groups)
                    n_team.append(n_group)
                    n_team.extend(team[(i + 1):])
                    p.append(n_team)

                fixed_groups.append(group)
    return p


def try_generating(container, objectives, desired_length):
    if desired_length == 1:
        return [[x] for x in container[1:]]

    nt = [[[container[1]]]]
    for i in range(2, desired_length + 1, 1):
        p = team(nt, container[i])
        p.extend(partner(nt, container[i], objectives))

        nt = p

    return nt
