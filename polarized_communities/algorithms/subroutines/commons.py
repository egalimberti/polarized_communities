from scipy.sparse.linalg import eigsh
import numpy as np


def evaluate_objective_function(signed_graph, x):
    # special case with no nodes in the solution
    if x.dot(x) == 0:
        return np.nan

    # obtain the adjacency matrix
    a = signed_graph.get_adjacency_matrix()

    # compute the objective function
    a_dot_x = a.dot(x)
    return x.dot(a_dot_x) / x.dot(x)


def build_solution(x):
    # return the nodes having the corresponding index of x different from 0
    return {node for node, element in enumerate(x) if element != 0}


def build_x(signed_graph, nodes, eigenvector=None):
    # get the maximum eigenvector of the adjacency matrix
    if eigenvector is None:
        a = signed_graph.get_adjacency_matrix()
        eigenvector = np.squeeze(eigsh(a, k=1, which='LA')[1])

    # build x from the signs of the minimum eigenvector
    return np.array([np.sign(element) if node in nodes else 0 for node, element in enumerate(eigenvector)])
