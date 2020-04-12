import utils
import recur_heur
import heuristic

# def check_accept(board, constraint_list):
#     for constraint in constraint_list:
#         node_list, tar_value = constraint
#         value = sum([board[y][x] for x, y in node_list])
#         if value != tar_value:
#             return False
#     return True

# def check_avail(board, domains, constraint_list):
#     for constraint in constraint_list:
#         node_list, tar_value = constraint
#         value = sum([board[y][x] for x, y in node_list])
#         upper_bound, lower_bound = value, value

#         for node in node_list:
#             if node in domains:
#                 if domains[node][1]:
#                     upper_bound += 1
#                 elif not domains[node][0] and domains[node][1]:
#                     lower_bound += 1

#         if upper_bound < tar_value or lower_bound > tar_value:
#             return False

#         if upper_bound == tar_value:    ## set all domains to upper bound value
#             for node in node_list:
#                 if node in domains:
#                     if domains[node][1]:
#                         domains[node][0] = False
            
#         if lower_bound == tar_value:    ## set all domains to lower bound value
#             for node in node_list:
#                 if node in domains:
#                     if domains[node][0]:
#                         domains[node][1] = False
    
#     return True

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
    inp = input()
    orig_map, board, domains, constraints, constraint_list = utils.parse_input(list(map(lambda x: int(x), inp.split(' '))))

    ## Flags
    forward_check = True
    heur = 'LCV' ## could be: None, MRV, Degree, LCV

    ## print board
    utils.print_board(orig_map, board)

    print(f'Forward Checking: {forward_check}, {heur} version')

    board, node_num = solve(board, domains, constraints, constraint_list, forward_check, heur)

    if board is None:
        print('No solution')
    else:
        print(f'Number of expanded nodes: {node_num}')
        utils.print_board(orig_map, board)