## main.py

import utils
import recur_heur

def solve(cur_board, cur_domains, constraints, constraint_list, forward_check, heur):
    recur_heur.expanded_node_cnt = 0
    if heur == 'None':
        return recur_heur.simple(cur_board, cur_domains, constraints, constraint_list, None, forward_check), recur_heur.expanded_node_cnt
    elif heur == 'MRV':
        return recur_heur.MRV(cur_board, cur_domains, constraints, constraint_list, None, forward_check), recur_heur.expanded_node_cnt
    elif heur == 'Degree':
        return recur_heur.Degree(cur_board, cur_domains, constraints, constraint_list, None, forward_check), recur_heur.expanded_node_cnt
    elif heur == 'LCV':
        return recur_heur.LCV(cur_board, cur_domains, constraints, constraint_list, None, forward_check), recur_heur.expanded_node_cnt

if __name__ == "__main__":
    ## Read and process input
    inp = input()
    orig_map, board, domains, constraints, constraint_list = utils.parse_input(list(map(lambda x: int(x), inp.split(' '))))

    ## Experiment Flags
    forward_check = True
    heur = 'Degree' ## could be: None, MRV, Degree, LCV

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