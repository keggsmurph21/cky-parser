from collections import defaultdict

class MatrixNode:

    def __init__(self, i, j):

        self.coords = (i,j)
        self.token = None
        self.children = defaultdict(set)

    def __len__(self):
        return len(self.children)

def build_matrix(tags, tokens):

    dim = range(len(tokens))
    X = [ [ MatrixNode(i,j) for j in dim ] for i in dim ]

    for (i, token) in enumerate(tokens):

        for pos_tag in tags[token]:

            mnode = X[i][i]
            mnode.children[pos_tag].add( (None, None) )
            mnode.token = token

        for j in range(i-1, -1, -1):

            mnode = X[i][j]

            for k in range(1, i-j+1):

                # indexing magic
                left_mnode = X[i-k][j]
                right_mnode = X[i][i-k+1]

                for left_pos in left_mnode.children.keys():
                    for right_pos in right_mnode.children.keys():

                        lookup_key = (left_pos, right_pos)
                        for parent in tags[lookup_key]:

                            mnode.children[parent].add( ( (left_mnode, left_pos), (right_mnode, right_pos) ) )

    return X

def _trace_back(node, pos='S'):

    children = []

    for (left, right) in node.children[pos]:

        if left is None and right is None:
            return (pos, node.token)

        children.append( (pos, _trace_back(*left), _trace_back(*right) ) )

    return children

def trace_back(matrix):

    corner = matrix[-1][0]

    if len(corner) == 0:
        return None

    return _trace_back(corner)

def parse_sents(tags, sents, word_depth=None):

    parses = []

    for sent in sents:

        if word_depth is not None:
            sent = sent[:word_depth]

        matrix = build_matrix(tags, sent)
        backtrace = trace_back(matrix)

        #print(backtrace)

        parses.append(matrix)

    return parses

def pretty_print(sents, parses):

    for (sent, matrix) in zip(sents, parses):
        print(' '.join(sent))
        for row in matrix:
            s = ''
            for col in row:
                if len(col):
                    s += 'O'
                else:
                    s += '.'
                s += ' '
            print(s)
