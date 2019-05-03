from collections import defaultdict
from to_cnf import normalize

def add_lexicon(grammar, sents):

    tags = get_tag_lookup(grammar)

    for sent in sents:
        for (token, pos) in sent:

           tags[token].add(pos) 

    return tags


def get_tag_lookup(grammar):
    
    grammar = normalize(grammar)

    tags = defaultdict(set)

    for rule in grammar.rules:

        if not rule.is_terminal:

            if len(rule.tars) != 2:
                raise ValueError('corpus not normalized')
            
            key = tuple(rule.tars)
            tags[key].add(rule.src)

    return tags

