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
    

    '''
    for (unit, tars) in unit_tars.items():

        for tar in tars:
            if tar in unit_tars:
                for sub_tar in unit_tars[tar]:
                    unit_tars[unit].add(sub_tar)

                #print(unit, tar, non_unit_counts[tar])
        #print()
        #print(unit)
        for tar in unit_tars:
            if tar in unit_tars:
                pass#print(tar)
                '''

    #print()
    #for rule in non_unit_rules:
        #print(rule)
    #print()
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


    #print()
    #for rule in non_unit_rules:
        ##print(rule)
    #print()
    long_rules = []
    for rule in non_unit_rules:

        tars = set(rule.tars)
        contains_unit = False

        for unit in unit_tars.keys():
            if non_unit_counts[unit] == 0 and unit in tars:
                contains_unit = True

        if not contains_unit:
           long_rules.append(rule)
   

    ##print(unit_tars)
    #print(topo)
    #print()
    #for rule in long_rules:
        #print(rule)
    #print()
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

                        #while unit_tar in unit_tars:
                            #if non_unit_counts[unit_tar] > 0:
                                #raise ValueError()
                            #elif len(unit_tars[unit_tar]) > 1:
                                #print(unit_tar, unit_tars[unit_tar])
                                #raise ValueError()
                            #unit_tar = list(unit_tars[unit_tar])[0]

                        new_tars.append(unit_tar)
                    
                    else:
                        new_tars.append(tar)

                new_rule = Rule(rule.src, new_tars, False)
                long_rules[i] = new_rule
    #print()
    #for rule in long_rules:
        ##print(rule)
    #print()

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
    #print()
    #for rule in grammar.rules:
        #print(rule)
    #print()

    '''
    #for rule in grammar.rules:
        #for tar in rule.tars:
            #if tar not in terminals:
                #found = False
                #for rule in grammar.rules:
                    #if tar == rule.src:
                        #found = True
               
                if not found:
                    print('!!!', rule.src, tar)
                    raise ValueError()
                    ValueError(rule.src, tar)
                    '''
    #for (src, tars) in terminals.items():
        #rule = Rule(src, tars, True)
        #grammar.rules.append(rule)
    ##print(unit_tars)
    return grammar

    for rule in grammar.rules:

        if rule.is_terminal:

            for tar in rule.tars:
                terminals[rule.src].add(tar)

        else:

            if rule.is_unit():
                unit_counts[rule.src] += 1
                units.add(rule)

            else:
                non_unit_counts[rule.src] += 1
                g_new.rules.append(rule)

    #for unit in units:
        #print(unit_counts[unit.src], non_unit_counts[unit.src], unit)
    for (i, rule) in enumerate(g_new.rules):

        if rule is None:
            continue

        tars = set(rule.tars)

        for unit in units:
            if unit.src in tars:


                new_tars = []
                for tar in rule.tars:
                    
                    if tar == unit.src:
                        new_tars.append(unit.tars[0])
                    else:
                        new_tars.append(tar)

                new_rule = Rule(rule.src, new_tars, False)

                if non_unit_counts[unit.src] == 0:
                    g_new.rules[i] = None
                g_new.rules.append(new_rule)

                #if non_unit_counts[unit.src] > 0 or unit_counts[unit.src] > 1:

                    #print('append', rule.src, unit.src, new_rule)
                    #g_new.rules.append(new_rule)

                #else:

                    #print('overwrite', rule.src, unit.src,new_rule)
                    #g_new.rules[i] = new_rule

                unit_counts[unit.src] -= 1

    g= Grammar()
    for rule in g_new.rules:

        if rule is not None:
            g.rules.append(rule)

        continue
        
        tars = set(rule.tars)
        contains_unit = False

        for unit in units:
            if contains_unit or unit.src in tars:
                contains_unit = True

        if not contains_unit:
            g.rules.append(rule)


    #for u in units:
        #print(u)
    #print()
    #print(g_new)
    #print()
    print(g)

def _normalize(g_old):

    if g_old.is_CNF():
        return g_old

    g_new = Grammar()
    units = set()
    src_counts = defaultdict(int)
    reverse_lookup = defaultdict(set)
    tokens = defaultdict(set)

    for rule in g_old.rules:

        if rule.is_terminal:
            g_new.add_rule(rule.src, rule.tars, True)

        elif not rule.is_unit():

            src_counts[rule.src] += 1

            for tar in rule.tars:
                reverse_lookup[tar].add(rule)
            g_new.add_rule(rule.src, rule.tars, False)

        else:

            units.add(rule)

    #print()
    #print(g_new)
    #print()

    #print(units)
    #for u in units:
        #print(src_counts[u.src], u)

    for (i, rule) in enumerate(g_new.rules):

        tars = set(rule.tars)

        for unit in units:

            if unit.src in tars:#if rule.has_targeIt(unit.src):
                
                new_tars = []
                for tar in rule.tars:
                    
                    if tar == unit.src:
                        new_tars.append(unit.tars[0])
                    else:
                        new_tars.append(tar)

                r = Rule(rule.src, new_tars, False)
                #print(rule, r)
                #g_new.rules[i] = r#Rule(rule.src, new_tars, False)
                #g_new.add_rule(rule.src, new_tars, False)
                g_new.add_rule(rule.src, new_tars, False)
                g_new.rules[i] = None

    g_new.rules = [ r for r in g_new.rules if r is not None ]

    #print()
    #print(g_new)
    #print()

    g_old = g_new
    g_new = Grammar()

    all_tags = set()
    for rule in g_old.rules:
        all_tags.add(rule.src)

    for rule in g_old.rules:
    
        is_valid = True
        if not rule.is_terminal:
            for tar in rule.tars:
                is_valid = (is_valid and tar in all_tags)

        if is_valid:
            g_new.add_rule(rule.src, rule.tars, rule.is_terminal)

    #print()
    #print(g_new)
    #print()

    g_old = g_new
    g_new = Grammar()

    for rule in g_old.rules:

        if rule.is_terminal:
            g_new.add_rule(rule.src, rule.tars, True)
        elif not rule.is_long():
            g_new.add_rule(rule.src, rule.tars, False)
        else:

            src = rule.src
            head = rule.tars[0]
            tail = rule.tars[1:]

            while len(tail) > 1:

                dummy = str(hash(slugify(tail)))

                g_new.add_rule(src, [head, dummy], False)

                src = dummy
                head = tail[0]
                tail = tail[1:]

            g_new.add_rule(src, [head, tail[0]], False)
    
    g_old = g_new
    g_new = Grammar()
    dedup = set()

    for rule in g_old.rules:

        key = slugify( [rule.src] + list(rule.tars) )

        if key not in dedup:

            g_new.add_rule(rule.src, rule.tars, rule.is_terminal)
            dedup.add(key)

    for (src, tars) in tokens.items():
        g_new.add_rule(src, tars, True)

    return g_new


