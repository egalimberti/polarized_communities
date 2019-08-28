from algorithms.subroutines.commons import *
from utilities.time_measure import ExecutionTime
from utilities.print_console import print_end_algorithm


def eigensign(signed_graph):
    # start of the algorithm
    execution_time = ExecutionTime()

    # initialize the solution as empty
    solution_x = None
    solution_objective_function = np.finfo(float).min
    solution_threshold = None

    # obtain the adjacency matrix
    a = signed_graph.get_adjacency_matrix()

    # get the eigenvector corresponding to the maximum eigenvalue
    maximum_eigenvector = np.squeeze(eigsh(a, k=1, which='LA')[1])

    # get the thresholds from the eigenvector
    thresholds = {int(np.abs(element) * 1000) / 1000.0 for element in maximum_eigenvector}

    # compute x for all the values of the threshold
    for threshold in thresholds:
        x = np.array([np.sign(element) if np.abs(element) >= threshold else 0 for element in maximum_eigenvector])

        # update the solution if needed
        objective_function = evaluate_objective_function(signed_graph, x)
        if objective_function > solution_objective_function:
            solution_x = x
            solution_objective_function = objective_function
            solution_threshold = threshold

    # build the solution
    solution = build_solution(solution_x)

    # end of the algorithm
    execution_time.end_algorithm()

    # print algorithm's results
    print_end_algorithm(execution_time.execution_time_seconds, solution_x, signed_graph, threshold=solution_threshold)

    # return the solution
    return solution, solution_x
