import networkx as nx
import pandas as pd
import re


class AdjacencyMatrix:
    @staticmethod
    def clean_text(s):
        return ' '.join(' '.join(re.findall(r'[a-zA-Z0-9]+', s)).split())

    def __init__(self, rows, events=True):
        self.rows = rows
        self.events = events

    def get_events(self):
        df = pd.DataFrame(self.rows)
        return [[AdjacencyMatrix.clean_text(i) for i in df[cn].tolist()[1:] if type(i) is str and len(i) > 0]
                for cn in list(df)]

    def to_network(self):
        nodes = map(lambda x: AdjacencyMatrix.clean_text(x), self.rows[0][1:])
        values = map(lambda x: x[1:], self.rows[1:])

        network = nx.Graph()

        network.add_edges_from([(nodes[i], nodes[j], {'stance': values[i][j]})
                                for i in xrange(len(nodes)) for j in xrange(i + 1, len(nodes))])

        return network

    def build(self):
        network = nx.Graph()

        if self.events:
            for event in self.get_events():
                network.add_edges_from([(event[i], event[j])
                                        for i in xrange(len(event)) for j in xrange(i + 1, len(event))])
        else:
            network.add_edges_from(self.rows)

        labels = sorted(network.nodes())
        adj_matrix = nx.adjacency_matrix(network, nodelist=labels).todense().tolist()

        for i in xrange(len(adj_matrix)):
            adj_matrix[i].insert(0, labels[i])
        labels.insert(0, '')
        return pd.DataFrame.from_records(adj_matrix, columns=labels)


def df2csv(df, path):
    df.to_csv(path, index=False, mode='wb')


def get_adjmat_name(csv_fn):
    return "{0}_adjacency_matrix.csv".format(AdjacencyMatrix.clean_text(csv_fn.split('.csv')[0]))

# import csv
# with open(r'C:\Users\rahue\Desktop\adjmat.csv', 'rb') as f:
#     rows = [row for row in csv.reader(f, delimiter=',')]
#
# am = AdjacencyMatrix(rows)
#
# print am.to_network().edge['B']['C']['stance']