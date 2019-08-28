from array import array
from scipy.sparse import *
import gc


class SignedGraph:

    def __init__(self, dataset_path):
        # nodes
        self.number_of_nodes = 0
        self.nodes_iterator = xrange(0)

        # adjacency list
        self.adjacency_list = []

        # adjacency matrix and laplacian
        self.a = None
        self.l = None

        # load the dataset
        self.load_dataset(dataset_path)

        # set the dataset path
        self.dataset_path = dataset_path

        # call the garbage collector
        gc.collect()

    def load_dataset(self, dataset_path):
        # open the file
        try:
            dataset_file = open('../datasets/' + dataset_path + '.txt')
        except IOError:
            dataset_file = open('../../datasets/' + dataset_path + '.txt')

        # get the number of nodes from the first line
        self.number_of_nodes = int(dataset_file.readline().replace('# ', ''))
        self.nodes_iterator = xrange(self.number_of_nodes)

        # create the empty adjacency list
        self.adjacency_list = [[array('i'), array('i')] for _ in self.nodes_iterator]

        # fill the adjacency matrix (0: positive neighbors, 1: negative neighbors)
        for line in dataset_file:
            split_line = line.split('\t')
            from_node = int(split_line[0])
            to_node = int(split_line[1])
            sign = int(split_line[2])

            # add the undirected edge
            self.add_edge(from_node, to_node, sign)

    # add the edge to the adjacency list if it is not a self loop
    def add_edge(self, from_node, to_node, sign):
        if sign == 1:
            sign = 0
        else:
            sign = 1

        if from_node != to_node:
            self.adjacency_list[from_node][sign].append(to_node)
            self.adjacency_list[to_node][sign].append(from_node)

    def get_adjacency_matrix(self):
        if self.a is None:
            self.a = lil_matrix((self.number_of_nodes, self.number_of_nodes), dtype='d')

            for node, neighbors in enumerate(self.adjacency_list):
                for neighbor in neighbors[0]:
                    self.a[node, neighbor] = 1
                for neighbor in neighbors[1]:
                    self.a[node, neighbor] = -1

            self.a = self.a.tocsr()

        return self.a

    def get_signed_laplacian(self):
        if self.l is None:
            self.l = lil_matrix((self.number_of_nodes, self.number_of_nodes), dtype='d')

            # add the inverted signs and the degree on the diagonal
            for node, neighbors in enumerate(self.adjacency_list):
                for neighbor in neighbors[0]:
                    self.l[node, neighbor] = -1
                for neighbor in neighbors[1]:
                    self.l[node, neighbor] = 1
                self.l[node, node] = len(neighbors[0]) + len(neighbors[1])

            self.l = self.l.tocsr()

        return self.l

    def get_signed_laplacian_subgraph(self, nodes):
        # order the nodes
        nodes = list(nodes)
        nodes.sort()

        # get the ordering in a map
        ordering = dict(zip(nodes, xrange(len(nodes))))

        rows, columns, data = [], [], []
        for node in nodes:
            order = ordering[node]
            degree = 0
            for neighbor in self.adjacency_list[node][0]:
                if neighbor in ordering:
                    rows.append(order)
                    columns.append(ordering[neighbor])
                    data.append(-1)
                    degree += 1
            for neighbor in self.adjacency_list[node][1]:
                if neighbor in ordering:
                    rows.append(order)
                    columns.append(ordering[neighbor])
                    data.append(1)
                    degree += 1
            rows.append(order)
            columns.append(order)
            data.append(degree)

        return coo_matrix((data, (rows, columns)), shape=(len(nodes), len(nodes)), dtype='d').tocsr()
