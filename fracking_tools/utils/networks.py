from matrices import AdjacencyMatrix
import csv


class NetworkComparison:
    @staticmethod
    def to_csv(fn, header, rows):
        with open(fn, 'wb') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(header)

            for row in rows:
                writer.writerow(row)

        return fn

    def __init__(self, network_name, network_a, network_b):
        self.network_name = AdjacencyMatrix.clean_text(network_name).title()
        self.network_a = network_a
        self.network_b = network_b

    def get_ab_actor_overlap(self):
        return list(set(self.network_a.nodes()) & set(self.network_b.nodes()))

    def get_ab_relationship_overlap(self):
        return list(set(self.network_a.edges()) & set(self.network_b.edges()))

    def get_unique_actors(self):
        nodes_a, nodes_b = self.network_a.nodes(), self.network_b.nodes()
        return filter(lambda x: x not in nodes_b, nodes_a), filter(lambda x: x not in nodes_a, nodes_b)

    def get_unique_relationships(self):
        edges_a, edges_b = self.network_a.edges(), self.network_b.edges()
        return filter(lambda x: x not in edges_b, edges_a), filter(lambda x: x not in edges_a, edges_b)

    def summarize(self):
        def add_spaces(source, target_size):
            if len(source) < target_size:
                return source + ['' for i in xrange(target_size - len(source))]
            return source

        summary_name = '{0} -- network comparison summary.csv'.format(self.network_name)
        header = ['AB Actor Overlap', 'AB Relationship Overlap', 'Unique A Actors',
                  'Unique B Actors', 'Unique A Relationships', 'Unique B Relationships']

        actor_overlap = self.get_ab_actor_overlap()
        relationship_overlap = self.get_ab_relationship_overlap()
        unique_a_actors, unique_b_actors = self.get_unique_actors()
        unique_a_relationships, unique_b_relationships = self.get_unique_relationships()

        columns = [actor_overlap, relationship_overlap, unique_a_actors,
                   unique_b_actors, unique_a_relationships, unique_b_relationships]

        max_size = max(map(lambda x: len(x), columns))

        actor_overlap = add_spaces(actor_overlap, max_size)
        relationship_overlap = add_spaces(relationship_overlap, max_size)
        unique_a_actors, unique_b_actors = add_spaces(unique_a_actors, max_size), add_spaces(unique_b_actors, max_size)
        unique_a_relationships, unique_b_relationships = add_spaces(unique_a_relationships, max_size), \
                                                         add_spaces(unique_b_relationships, max_size)

        rows = [[actor_overlap[i], relationship_overlap[i], unique_a_actors[i], unique_b_actors[i],
                unique_a_relationships[i], unique_b_relationships[i]] for i in xrange(max_size)]

        return summary_name, header, rows

# import csv
#
# with open(r'C:\Users\rahue\Desktop\adjmat.csv', 'rb') as f:
#     rows1 = [row for row in csv.reader(f, delimiter=',')]
#
# with open(r'C:\Users\rahue\Desktop\net2.csv', 'rb') as f:
#     rows2 = [row for row in csv.reader(f, delimiter=',')]

# net1 = AdjacencyMatrix(rows1).to_network()
# net2 = AdjacencyMatrix(rows2).to_network()
#
# nc = NetworkComparison('Sample', net1, net2)
#
# fn, header, rows = nc.summarize()
#
# print nc.to_csv(fn, header, rows)


