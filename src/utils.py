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

