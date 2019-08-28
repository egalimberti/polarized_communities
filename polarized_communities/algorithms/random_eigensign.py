from algorithms.subroutines.commons import *
from utilities.time_measure import ExecutionTime
from utilities.print_console import print_end_algorithm


def random_eigensign(signed_graph, beta, maximum_eigenvector=None, execution_time_seconds=None):
    # start of the algorithm
    execution_time = ExecutionTime()

    if maximum_eigenvector is None:
        # obtain the adjacency matrix
        a = signed_graph.get_adjacency_matrix()

        # get the eigenvector corresponding to the maximum eigenvalue
        maximum_eigenvector = np.squeeze(eigsh(a, k=1, which='LA')[1])

        # consolidate beta
        if beta == 'l1':
            beta = np.linalg.norm(maximum_eigenvector, ord=1)
        elif beta == 'sqrt':
            beta = np.sqrt(signed_graph.number_of_nodes)
        else:
            beta = float(beta)

        # multiply the maximum eigenvector by beta
        maximum_eigenvector *= beta

    # compute x
    x = np.array([0 for _ in signed_graph.nodes_iterator])
    for node, element in enumerate(maximum_eigenvector):
        # check the probability for a certain number of times
        if np.random.choice((True, False), p=(min(np.abs(element), 1), max(1 - np.abs(element), 0))):
            x[node] = np.sign(element)

    # build the solution
    solution = build_solution(x)

    # end of the algorithm
    execution_time.end_algorithm()

    # print algorithm's results
    if execution_time_seconds is None:
        execution_time_seconds = execution_time.execution_time_seconds
    print_end_algorithm(execution_time_seconds, x, signed_graph, beta=beta)

    # return the solution
    return solution, x, maximum_eigenvector, execution_time_seconds, beta
