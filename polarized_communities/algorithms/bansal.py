from algorithms.subroutines.commons import *
from utilities.time_measure import ExecutionTime
from utilities.print_console import print_end_algorithm


def bansal(signed_graph):
    # start of the algorithm
    execution_time = ExecutionTime()

    # initialize the solution as empty
    solution_x = None
    solution_objective_function = np.finfo(float).min

    # get the best clustering from the neighborhood of each node
    for node, neighbors in enumerate(signed_graph.adjacency_list):
        x = np.zeros(signed_graph.number_of_nodes)
        x[node] = 1
        for neighbor in neighbors[0]:
            x[neighbor] = 1
        for neighbor in neighbors[1]:
            x[neighbor] = -1

        # update the solution if needed
        objective_function = evaluate_objective_function(signed_graph, x)
        if objective_function > solution_objective_function:
            solution_x = x
            solution_objective_function = objective_function

    # build the solution
    solution = build_solution(solution_x)

    # end of the algorithm
    execution_time.end_algorithm()

    # print algorithm's results
    print_end_algorithm(execution_time.execution_time_seconds, solution_x, signed_graph)

    # return the solution
    return solution, solution_x
