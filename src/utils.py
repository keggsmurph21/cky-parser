import json
from collections import defaultdict
from nltk.corpus import cess_cat, cess_esp

def slugify(array):
    array = [s for s in array if s != '|']
    return '~~~'.join(array)

def deslugify(string):
    return string.split('~~~')

def get_corpus(name, level, n=None):

    # validate corpus name
    if name == 'cess_cat':
        corpus = cess_cat

    elif name == 'cess_esp':
        corpus = cess_esp

    else:
        raise ValueError(f'unrecognized corpus name "{name}" (cess_cat/cess_esp)')

    # validate corpus type
    if level == 'parsed':
        sents = corpus.parsed_sents()

    elif level == 'tagged':
        sents = corpus.tagged_sents()

    elif level == 'unparsed':
        sents = corpus.sents()

    else:
        raise ValueError(f'unrecognized corpus type "{level}" (parsed/tagged/unparsed)')

    # truncate
    if n is not None:
        sents = sents[:n]

    return sents

def save_tags(tags, filename):

    if filename is None:
        raise ValueError('no filename specified')

    obj = {}

    for (tag_key, tag_val) in tags.items():

        if type(tag_key) == str:
            tag_key = [tag_key]
        json_key = '+++'.join(tag_key)
        json_val = list(tag_val)

        obj[json_key] = json_val

    with open(filename, 'w') as fp:
        json.dump(obj, fp, indent=2, sort_keys=True)

    return obj

def load_tags(filename):

    if filename is None:
        raise ValueError('no filename specified')

    tags = defaultdict(set)

    with open(filename) as fp:

        obj = json.load(fp)

        for (json_key, json_val) in obj.items():

            json_key = json_key.split('+++')

            if len(json_key) == 1:
                tag_key = json_key[0]
            else:
                tag_key = tuple(json_key)

            tag_val = set(json_val)
            tags[tag_key] = tag_val

    return tags

def prepare_for_latex(truth_filename, truth_results, test_results):

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
