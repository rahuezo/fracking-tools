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

# events = [
#     ['Event A', 'Event B', 'Event C'],
#     ['A', 'A', 'B' ],
#     ['B', 'C', 'C' ],
#     ['C', '', '' ],
# ]
#
#
# pairs = [
#     ['A', 'B'],
#     ['C', 'A'],
#     ['B', 'C']
# ]
#
# df2csv(AdjacencyMatrix(events).build(), './tryingoutfunc.csv')
# import csv
#
# wd = r'C:\Users\Rudy\Desktop\events.csv'
#
# events = [row for row in csv.reader(open(wd, 'rb'), delimiter=str(u',').encode('utf-8'))]
#           # csv.reader(open(wd, 'rb'), delimiter=',')]
#
# print AdjacencyMatrix(events).build()