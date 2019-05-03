from collections import defaultdict


class MatrixNode:

    def __init__(self, i, j):

        self.coords = (i,j)
        self.token = None
        self.children = defaultdict(set)

    def __repr__(self):

        s = f'<m'
        s += str(self.coords)
        return s

        if len(self.pos_tags):
            s += ' ' 
            s += '@'.join(self.pos_tags)
        if self.token:
            s += ' "'
            s += self.token
            s += '"'
        if len(self):
            s += ' ['
            s += ','.join([ str(c) for c in self.children ])
            s += ']'
        s += '>'

        return s

    def __len__(self):
        return len(self.children)

def build_matrix(tags, tokens):

    dim = range(len(tokens))

    X = [ [ MatrixNode(i,j) for j in dim ] for i in dim ]
    D = [ [ set() for i in tokens ] for i in tokens ]

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

                            #mnode.children.add( (parent, left_mnode, right_mnode) )

    return X

    if False:
        for pos_tag in tags[token]:

            D[i][i].add( (pos_tag, token, None) )

        for j in range(i-1, -1, -1):
            for k in range(1, i-j+1):

                # indexing magic
                left_tags = D[i-k][j]
                right_tags = D[i][i-k+1]

                for left_tag in left_tags:
                    for right_tag in right_tags:

                        key = (left_tag[0], right_tag[0])
                        #print((i,j), key, tags[key])
                        for parent in tags[key]:

                            left_trace = (i-k, j, left_tag[0])
                            right_trace = (i, i-k+1, right_tag[0])
                            
                            mnode = X[i][j]
                            left_mnode = X[i-k][j]
                            right_mnode = X[i][i-k+1]
    
                            mnode.children.add( (key, left_mnode, right_mnode) )

                            D[i][j].add( (parent, left_trace, right_trace) )

    return X
    print(X)
    return D

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
        #for row in matrix:
            #print(row)

        backtrace = trace_back(matrix)
        
        #print(backtrace)

        parses.append(matrix)

    return parses

def pretty_print(sents, parses):

    #key = []
    for (sent, matrix) in zip(sents, parses):
        print(' '.join(sent))
        for row in matrix:
            s = ''
            for col in row:
                if len(col):
                    s += 'O'
                    #s += str(len(key))
                    #key.append(col)
                else:
                    s += '.'
                s += ' '
            print(s)
    #for (i,k) in enumerate(key):
        #print(i,k)

