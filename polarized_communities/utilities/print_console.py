import numpy as np

from algorithms.subroutines.commons import evaluate_objective_function


def print_input(dataset, algorithm):
    print '------------- Input -------------'
    print 'dataset:               ' + dataset
    print 'algorithm:             ' + algorithm


def print_end_algorithm(runtime, x, signed_graph, beta=np.nan, threshold=np.nan):
    print '------------- Output ------------'

    # parameters
    print 'tau:                   ' + str(threshold)
    print 'multiplicative factor: ' + str(beta)

    # performance information
    print 'runtime:               ' + str(runtime)

    # quality of the solution
    print 'polarity:              ' + str(evaluate_objective_function(signed_graph, x))

    # print the nodes of the two communities
    community_p1 = {node for node, element in enumerate(x) if element == 1}
    community_m1 = {node for node, element in enumerate(x) if element == -1}

    print 'S_1:                   ' + str(str(community_p1).replace('set([', '').replace('])', ''))
    print 'S_2:                   ' + str(str(community_m1).replace('set([', '').replace('])', ''))
