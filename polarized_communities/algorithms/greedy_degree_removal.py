from blist import sorteddict

from algorithms.subroutines.commons import *
from utilities.time_measure import ExecutionTime
from utilities.print_console import print_end_algorithm


def greedy_degree_removal(signed_graph, signed_degree=True):
    # start of the algorithm
    execution_time = ExecutionTime()

    # initialize the solution with all nodes
    solution = set(signed_graph.nodes_iterator)
    solution_x = build_x(signed_graph, solution)
    solution_objective_function = evaluate_objective_function(signed_graph, solution_x)

    # compute the degree of each node and divide them in sets
    degree = {}
    degree_sets = sorteddict()

    for node, neighbors in enumerate(signed_graph.adjacency_list):
        degree[node] = len(neighbors[0])
        if signed_degree:
            degree[node] -= len(neighbors[1])

        try:
            degree_sets[degree[node]].add(node)
        except KeyError:
            degree_sets[degree[node]] = {node}

    # pick a lowest degree node
    nodes = solution.copy()
    x = solution_x.copy()
    while len(degree_sets) > 0:
        lowest_degree = degree_sets.keys()[0]
        while len(degree_sets[lowest_degree]) > 0:
            node = degree_sets[lowest_degree].pop()

            # update the degree of its neighbors
            for neighbor in signed_graph.adjacency_list[node][0]:
                if neighbor in nodes:
                    degree_sets[degree[neighbor]].remove(neighbor)
                    degree[neighbor] -= 1
                    try:
                        degree_sets[degree[neighbor]].add(neighbor)
                    except KeyError:
                        degree_sets[degree[neighbor]] = {neighbor}
                        if degree[neighbor] < lowest_degree:
                            lowest_degree = degree[neighbor]

            if signed_degree:
                for neighbor in signed_graph.adjacency_list[node][1]:
                    if neighbor in nodes:
                        degree_sets[degree[neighbor]].remove(neighbor)
                        degree[neighbor] += 1
                        try:
                            degree_sets[degree[neighbor]].add(neighbor)
                        except KeyError:
                            degree_sets[degree[neighbor]] = {neighbor}

            # remove the node from the current set of nodes
            nodes.remove(node)

            # update the solution if needed
            x[node] = 0
            objective_function = evaluate_objective_function(signed_graph, x)
            if objective_function > solution_objective_function:
                solution = nodes.copy()
                solution_x = x.copy()
                solution_objective_function = objective_function

        # remove the empty set from the dict
        del degree_sets[lowest_degree]

    # end of the algorithm
    execution_time.end_algorithm()

    # print algorithm's results
    print_end_algorithm(execution_time.execution_time_seconds, solution_x, signed_graph)

    # return the solution
    return solution, solution_x
