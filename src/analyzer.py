from collections import Counter
from cky import build_matrix, pretty_print, trace_back

def score_matrix(matrix, ctr, parsed_sent):
   
    dim = len(matrix)

    ctr['sents'] += 1

    ctr['p1_recog'] += (len(matrix[-1][0]) > 0)
    #ctr['p2_valid'] += verify_parse(matrix, parsed_sent) # note: this isn't working :(

    dists = [ 0 for i in range(dim) ]
    for i in range(dim):
        for j in range(i+1, dim):

            if len(matrix[j][i]) > 0:

                dist = j - i
                
                if dist > dists[i]:
                    dists[i] = dist

                if dist > dists[j]:
                    dists[j] = dist

    h1 = max(dists)
    h2 = sum(dists)/(len(dists) - 1)
    h3 = sum([ (i>0) for i in dists ])

    ctr['h1_max'] += h1
    ctr['h1_max_n'] += h1 / (dim - 1)
    ctr['h2_avg'] += h2
    ctr['h2_avg_n'] += h2 / (dim - 1)
    ctr['h3_non0'] += h3
    ctr['h3_non0_n'] += h3 / dim

def verify_parse(matrix, parsed_sent):

    # can't figure out a good way to implement this function ... these objects
    #  have very different data structures ... 

    backtrace = trace_back(matrix)
    tagged_sent = parsed_sent.pos()

    return 0

def analyze(parsed_sents, unparsed_sents, truth_tags, test_data, word_depth):

    truth_counter = Counter()
    test_counters = [ Counter() for j in test_data ]

    for (sent, parsed_sent) in zip(unparsed_sents, parsed_sents):
   
        if word_depth is not None:
            sent = sent[:word_depth]

        matrix = build_matrix(truth_tags, sent)
        score_matrix(matrix, truth_counter, parsed_sent)

        for ((tag_name, test_tags), ctr) in zip(test_data, test_counters):

            matrix = build_matrix(test_tags, sent)
            score_matrix(matrix, ctr, parsed_sent)


    fields = ['h1_max', 'h1_max_n', 'h2_avg', 'h2_avg_n', 'h3_avg', 'h3_avg_n', 'p1_recog']

    test_results = []
    for (i, (filename, _)) in enumerate(test_data):
        test_results.append( (filename, test_counters[i]) )

    return (fields, truth_counter, test_results)

