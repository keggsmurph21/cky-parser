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
from utils import get_corpus, load_tags, save_tags, prepare_for_latex


def write_grammar(grammar, output):

    text = str(grammar)

    if output is None:
        sys.stdout.write(text)

    else:
        with open(output, 'w') as fp:
            fp.write(text)

def read_or_build_grammar(args):

    if args.ingrammar:
        grammar = read_grammar(args.ingrammar)
    else:
        sents = get_corpus(args.induce, 'parsed', args.num_sents)
        grammar = induce(sents)

    return grammar

def build_tags(args):

    grammar = read_or_build_grammar(args)
    lexicon = get_corpus(args.lexicon, 'tagged')
    tags = add_lexicon(grammar, lexicon)

    return tags


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=''''\
CKY Parser & more : for more info, check out the README :)''')
    parser.add_argument('action')
    parser.add_argument('-i', '--induce'
        , help='corpus to induce a grammar from (cess_cat/cess_esp)')
    parser.add_argument('-g', '--ingrammar'
        , help='filepath to read a grammar from')
    parser.add_argument('-o', '--outgrammar'
        , help='filepath to write a grammar to')
    parser.add_argument('-c', '--cache'
        , help='read tags to/from, saves lots of time when parsing')
    parser.add_argument('-l', '--lexicon'
        , help='which lexicon to use when preparing the grammar for parsing')
    parser.add_argument('-n', '--num_sents', type=int
        , help='consider only the first N sentences when analyzing')
    parser.add_argument('-t', '--test', nargs='+'
        , help='whitespaced-separated list of cache files to analyzed')
    parser.add_argument('-T', '--truth'
        , help='cache file to use as the "ground truth" for analysis')
    parser.add_argument('-w', '--words', type=int
        , help='only consider the first W words of sentences (useful for making sense out parse output)')
    args = parser.parse_args()

    if args.action == 'get':

        sents = get_corpus(args.induce, 'parsed', args.num_sents)
        for sent in sents:
            print(sent)

    elif args.action == 'draw':

        sents = get_corpus(args.induce, 'parsed', args.num_sents)
        for sent in sents:
            sent.draw()

    elif args.action == 'induce':

        sents = get_corpus(args.induce, 'parsed', args.num_sents)
        induced = induce(sents)
        write_grammar(induced, args.outgrammar)

    elif args.action == 'normalize':

        grammar = read_or_build_grammar(args)
        grammar = normalize(grammar)
        write_grammar(grammar, args.outgrammar)

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

        prepare_for_latex(args.truh, truth_results, test_results)


    else:
        ValueError(f'unrecognized command "{args.action}" (get)')
        exit(1)
