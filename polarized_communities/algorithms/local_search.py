import random

from bansal import bansal
from algorithms.subroutines.commons import *
from utilities.time_measure import ExecutionTime
from utilities.print_console import print_end_algorithm


def local_search(signed_graph, maximum_changes, convergence_threshold, partial_solution='r'):
    # start of the algorithm
    execution_time = ExecutionTime()

    # solution and value of the objective function
    if partial_solution == 'b':
        solution, _, original_x = bansal(signed_graph, verbose=False)
    else:
        solution = random_solution(signed_graph)
        original_x = build_x(signed_graph, set(signed_graph.nodes_iterator))
    solution_x = build_x(signed_graph, solution, eigenvector=original_x)
    solution_objective_function = evaluate_objective_function(signed_graph, solution_x)

    # while there might be improvements to the solution
    improvable = True
    changes = 0
    while improvable and (maximum_changes is None or changes < maximum_changes):
        # find the node of highest gain
        best_node = None
        best_gain = .0

        # move each node in or out the solution
        for node in signed_graph.nodes_iterator:
            if node in solution:
                solution.remove(node)
                solution_x[node] = 0

                objective_function = evaluate_objective_function(signed_graph, solution_x)

                solution.add(node)
                solution_x[node] = original_x[node]
            else:
                solution.add(node)
                solution_x[node] = original_x[node]

                objective_function = evaluate_objective_function(signed_graph, solution_x)

                solution.remove(node)
                solution_x[node] = 0

            # update the node of highest gain
            gain = objective_function - solution_objective_function
            if gain > best_gain:
                best_node = node
                best_gain = gain

        # update the solution if there is a considerable gain
        if best_gain >= convergence_threshold:
            if best_node in solution:
                solution.remove(best_node)
                solution_x[best_node] = 0
            else:
                solution.add(best_node)
                solution_x[best_node] = original_x[best_node]

            solution_objective_function = evaluate_objective_function(signed_graph, solution_x)
            changes += 1
        else:
            # stop the algorithm otherwise
            improvable = False

    # end of the algorithm
    execution_time.end_algorithm()

    # print algorithm's results
    print_end_algorithm(execution_time.execution_time_seconds, solution_x, signed_graph)

    # return the solution
    return solution, solution_x


def random_solution(signed_graph):
    # choice list
    choice_list = [True, False]

    # create a random solution
    solution = set()
    for node in signed_graph.nodes_iterator:
        if random.choice(choice_list):
            solution.add(node)

    return solution
