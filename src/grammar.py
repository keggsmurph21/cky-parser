from collections import defaultdict
from utils import slugify

class Rule:

    def __init__(self, src, tars, is_terminal):

        self.src = src
        self.tars = tars
        self.is_terminal = is_terminal

    def is_unit(self):
        return not self.is_terminal and len(self.tars) == 1

    def is_long(self):
        return not self.is_terminal and len(self.tars) > 2

    def __repr__(self):
    
        s = 'Rule('
        s += self.src
        s += ' => '

        if self.is_terminal:
            s += ' | '.join(self.tars)

        else:
            s += ' '.join(self.tars)

        s += ')'

        return s

    def has_target(self, tar):
        return not self.is_terminal and tar in self.tars

class Grammar:

    def __init__(self):

        self.rules = []

    def add_rule(self, src, tars, is_terminal):

        rule = Rule(src, tars, is_terminal)
        self.rules.append(rule)

    def dedup(self):

        seen = set()
        rules = []
        tokens = defaultdict(set)

        for rule in self.rules:

            if rule.is_terminal:

                for tar in rule.tars:
                    tokens[rule.src].add(tar)

            else:

                key = hash(slugify( [rule.src] + list(rule.tars) ))

                if key not in seen:

                    rules.append(rule)
                    seen.add(key)

        for (src, tars) in tokens.items():
            rules.append(Rule(src, tars, True))

        self.rules = rules

    def __repr__(self):

        lines = []

        for rule in self.rules:
            if not rule.is_terminal:

                line = f'{rule.src} => {" ".join(rule.tars)}'
                lines.append(line)

        for rule in self.rules:
            if rule.is_terminal:

                line = f'{rule.src} => {" | ".join(rule.tars)}'
                lines.append(line)

        return '\n'.join(lines)

    def is_CNF(self):

        for rule in self.rules:
            if not rule.is_terminal and len(rule.tars) != 2:
                return False

        return True

def read_grammar(filepath):

    grammar = Grammar()

    with open(filepath) as fp:

        all_tags = read_tags(fp)
        fp.seek(0)
        add_rules(grammar, fp, all_tags)

    return grammar

def add_rules(grammar, lines, all_tags):

    for line in lines:

        line = line.strip()
        tags = line.split(' ')
        tags = [ t for t in tags if t != '|' ]

        src = tags[0]
        tars = tags[2:]

        is_terminal = True
        for tar in tars:
            if tar in all_tags:
                is_terminal = False

        grammar.add_rule(src, tars, is_terminal)

def read_tags(lines):

    all_tags = set()
    for line in lines:
        tag = line.split(' ')[0]
        all_tags.add(tag)

    return all_tags
