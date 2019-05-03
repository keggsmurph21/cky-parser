'''
Kevin Murphy
Spring 2019
Linguistics Honors project
'''


import argparse
import sys
from add_lexicon import add_lexicon
from analyzer import analyze
from cky import parse_sents, pretty_print
from grammar import read_grammar
from inducer import induce
from to_cnf import normalize
from utils import get_corpus, load_tags, save_tags


class Output:

    def __init__(self, filename):

        self.filename = filename
        self.fp = None

    def __enter__(self):
        
        if type(self.filename) == str:
            self.fp = open(self.filename, 'w')
        else:
            self.fp = self.filename # sys.stdout

    def __exit__(self):

        self.fp.close()

def write_grammar(grammar, output):

    text = str(grammar)

    if output is None:
        sys.stdout.write(text)
    
    else:
        with open(output, 'w') as fp:
            fp.write(text)

def read_or_build_grammar(args):

    if args.grammar:
        grammar = read_grammar(args.grammar)
    else:
        sents = get_corpus(args.corpus, 'parsed', args.num_sents)
        grammar = induce(sents)

    return grammar

def build_tags(args):

    grammar = read_or_build_grammar(args)
    lexicon = get_corpus(args.lexicon, 'tagged')
    tags = add_lexicon(grammar, lexicon)

    return tags


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('action')
    parser.add_argument('-c', '--corpus')
    parser.add_argument('-g', '--grammar')
    parser.add_argument('-j', '--json')
    parser.add_argument('-l', '--lexicon')
    parser.add_argument('-n', '--num_sents', type=int)
    parser.add_argument('-o', '--output')
    parser.add_argument('-t', '--test', nargs='+')
    parser.add_argument('-T', '--truth')
    parser.add_argument('-w', '--words', type=int)
    args = parser.parse_args()

    if args.action == 'get':

        sents = get_corpus(args.corpus, 'parsed', args.num_sents)
        for sent in sents:
            print(sent)

    elif args.action == 'draw':

        sents = get_corpus(args.corpus, 'parsed', args.num_sents)
        for sent in sents:
            sent.draw()

    elif args.action == 'induce':

        sents = get_corpus(args.corpus, 'parsed', args.num_sents)
        induced = induce(sents)
        write_grammar(induced, args.output)

    elif args.action == 'normalize':

        grammar = read_or_build_grammar(args)
        grammar = normalize(grammar)
        write_grammar(grammar, args.output)
    
    elif args.action == 'add-lexicon':

        tags = build_tags(args)
        save_tags(tags, args.json)

    elif args.action == 'parse':

        if args.json:
            tags = load_tags(args.json)
        else:
            tags = build_tags(args)

        sents = get_corpus(args.lexicon, 'unparsed', args.num_sents)
        parses = parse_sents(tags, sents, args.words)
        pretty_print(sents, parses)

    elif args.action == 'analyze':
        
        test_data = [ (filename, load_tags(filename)) for filename in args.test ]
        truth_tags = load_tags(args.truth)
        parsed_sents = get_corpus(args.lexicon, 'parsed', args.num_sents)
        unparsed_sents = get_corpus(args.lexicon, 'unparsed', args.num_sents)

        (fields, truth_results, test_results) = analyze(parsed_sents,
                unparsed_sents, truth_tags, test_data, args.words)

        truth_h1 = round(truth_results['h1_max_n'], 3)
        truth_h2 = round(truth_results['h2_avg_n'], 3)
        truth_h3 = round(truth_results['h3_non0_n'], 3)
        truth_p1 = round(truth_results['p1_recog'], 3)
        sents = truth_results['sents']

        for (filename, results) in test_results:

            h1 = round(results['h1_max_n'], 3)
            h2 = round(results['h2_avg_n'], 3)
            h3 = round(results['h3_non0_n'], 3)
            p1 = round(results['p1_recog'], 3)

            s = '\t\t$G$ & '
            s += str(h1)
            s += ' & '
            s += str(round(h1/truth_h1, 3))
            s += ' & '
            s += str(h2)
            s += ' & '
            s += str(round(h2/truth_h2, 3))
            s += ' & '
            s += str(h3)
            s += ' & '
            s += str(round(h3/truth_h3, 3))
            s += ' \\\\ % '
            s += filename

            print(s)

            s = '\t\t$P$ & '
            s += str(p1)
            s += ' & '
            s += str(round(p1/sents, 3))
            s += ' & '
            s += str(round(p1/truth_p1, 3))
            s += ' \\\\ % '
            s += filename

            print(s)
        
        s = '\t\t$G^{100}$ & '
        s += str(truth_h1)
        s += ' & $-$ & '
        s += str(truth_h2)
        s += ' & $-$ & '
        s += str(truth_h3)
        s += ' & $-$ \\\\ % '
        s += args.truth

        print(s)

        s = '\t\t$P^{100}$ & '
        s += str(truth_p1)
        s += ' & '
        s += str(round(truth_p1/sents, 3))
        s += ' & $-$ \\\\ % '
        s += filename

        print(s)
        

    else:
        ValueError(f'unrecognized command "{args.action}" (get)')
        exit(1)
    
