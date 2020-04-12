import utils
import recur_heur
import heuristic

# def solve(orig_map, process_stack, constraints, constraint_list, forward_check, heur):
#     expanded_node_num = 0
#     while True:
#         if len(process_stack) == 0:
#             return None, None

#         cur_board, cur_domains = process_stack[-1]
#         expanded_node_num += 1
#         del process_stack[-1]

#         if forward_check:
#             if not utils.check_avail(orig_map, cur_board, cur_domains, constraint_list):
#                 continue
        
#         ## reach leaf of search tree
#         if len(cur_domains) == 0:
#             if not utils.check_accept(orig_map, cur_board, constraint_list):
#                 continue
#             else:
#                 return cur_board, expanded_node_num
        
#         ## expand node
#         if heur == 'None':
#             heuristic.simple(cur_board, cur_domains, process_stack)
#         elif heur == 'MRV':
#             heuristic.MRV(cur_board, cur_domains, process_stack)
#         elif heur == 'Degree':
#             heuristic.Degree(cur_board, cur_domains, process_stack, constraints)

def solve(cur_board, cur_domains, constraints, constraint_list, forward_check, heur):
    if heur == 'None':
        return recur_heur.simple(cur_board, cur_domains, constraints, constraint_list, None, forward_check, 0)
    elif heur == 'MRV':
        return recur_heur.MRV(cur_board, cur_domains, constraints, constraint_list, None, forward_check, 0)
    elif heur == 'Degree':
        return recur_heur.Degree(cur_board, cur_domains, constraints, constraint_list, None, forward_check, 0)
    elif heur == 'LCV':
        return recur_heur.LCV(cur_board, cur_domains, constraints, constraint_list, None, forward_check, 0)

if __name__ == "__main__":
    ## Read and process input
    inp = input()
    orig_map, board, domains, constraints, constraint_list = utils.parse_input(list(map(lambda x: int(x), inp.split(' '))))

    ## Experiment Flags
    forward_check = True
    heur = 'MRV' ## could be: None, MRV, Degree, LCV

    ## Print board
    utils.print_board(orig_map, board)

    print(f'Forward Checking: {forward_check}, {heur} version')

    ## Start search
    board, node_num = solve(board, domains, constraints, constraint_list, forward_check, heur)

    ## Print result
    if board is None:
        print('No solution')
    else:
        print(f'Number of expanded nodes: {node_num}')
        utils.print_board(orig_map, board)