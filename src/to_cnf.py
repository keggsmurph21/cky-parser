from collections import defaultdict
from grammar import Grammar, Rule
from utils import slugify


def descend(current, graph, leaves=set()):

    for neighbor in graph[current]:

        if neighbor in leaves:
            continue

        leaves.add(neighbor)

        if neighbor in graph:

            descend(neighbor, graph, leaves)

    return leaves

def normalize(grammar):

    if grammar.is_CNF():
        return grammar

    terminals = defaultdict(set)
    unit_tars = defaultdict(set)
    non_unit_counts = defaultdict(int)
    non_unit_rules = []

    for rule in grammar.rules:

        if rule.is_terminal:

            for tar in rule.tars:
                terminals[rule.src].add(tar)

        else:

            if rule.is_unit():
                unit_tars[rule.src].add(rule.tars[0])

            else:
                non_unit_counts[rule.src] += 1
                non_unit_rules.append(rule)

    topo = {}
    for (unit, tars) in unit_tars.items():
        topo[unit] = descend(unit, unit_tars, set())
    unit_tars = topo

    seen = set()
    for rule in non_unit_rules:

        tars = set(rule.tars)

        for unit in unit_tars.keys():
            if unit in tars:

                for i in range(len(unit_tars[unit])):

                    new_tars = []
                    for tar in rule.tars:

                        if tar == unit:
                            new_tars.append(f'{unit}_UNIT_{i}')
                        else:
                            new_tars.append(tar)

                    key = tuple([rule.src] + list(new_tars))
                    if key not in seen:

                        new_rule = Rule(rule.src, new_tars, False)
                        non_unit_rules.append(new_rule)
                        seen.add(key)

    long_rules = []
    for rule in non_unit_rules:

        tars = set(rule.tars)
        contains_unit = False

        for unit in unit_tars.keys():
            if non_unit_counts[unit] == 0 and unit in tars:
                contains_unit = True

        if not contains_unit:
           long_rules.append(rule)

    unit_map = {}
    for unit in unit_tars.keys():
        for (i, tar) in enumerate(unit_tars[unit]):

            key = f'{unit}_UNIT_{i}'
            unit_map[key] = tar

    for (i, rule) in enumerate(long_rules):

        tars = set(rule.tars)

        for (unit_key, unit_tar) in unit_map.items():

            if unit_key in tars:

                new_tars = []

                for tar in long_rules[i].tars:
                    if tar == unit_key:

                        new_tars.append(unit_tar)

                    else:
                        new_tars.append(tar)

                new_rule = Rule(rule.src, new_tars, False)
                long_rules[i] = new_rule

    grammar.rules = []
    for rule in long_rules:

        if rule.is_long():

            src = rule.src
            head = rule.tars[0]
            tail = rule.tars[1:]

            while len(tail) > 1:

                dummy = str(hash(slugify(tail)))
                dummy = slugify(tail)
                dummy_rule = Rule(src, [head, dummy], False)
                grammar.rules.append(dummy_rule)

                src = dummy
                head = tail[0]
                tail = tail[1:]

            dummy_rule = Rule(src, [head, tail[0]], False)
            grammar.rules.append(dummy_rule)

        else:

            grammar.rules.append(rule)

    return grammar
