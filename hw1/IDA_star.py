import time
import copy
import heapq
import utils

def recursive_dfs(cur_x, cur_y, g_x, g_y, history_record, cur_steps, max_threshold, min_node_weight, board_size=8):    
    ## if achieve goal state, return this path
    if cur_x == g_x and cur_y == g_y:
        return True, min_node_weight

    new_steps = cur_steps+1
    prev_hist_idx = len(history_record)-1   ## the previous node index in history_record
    
    for move in utils.moves:
        new_x, new_y = cur_x+move[0], cur_y+move[1] ## compute new node coordinate
        if utils.check_valid_pos(new_x, new_y, board_size=board_size):  ## check whether it is valid
            ## check if it reach the threshold, if yes, then cut it
            node_weight = utils.compute_f(new_x, new_y, g_x, g_y, new_steps)
            if node_weight > max_threshold:
                if min_node_weight is None or min_node_weight > node_weight:
                    min_node_weight = node_weight
                continue
            
            history_record.append((new_x, new_y, prev_hist_idx))
            
            ## do recursion
            found, min_node_weight = recursive_dfs(new_x, new_y, g_x, g_y, history_record, new_steps, max_threshold, min_node_weight, board_size=board_size)

            ## if it find the path, then return it
            if found:
                return found, min_node_weight
    
    return False, min_node_weight

def dfs_heur(s_x, s_y, g_x, g_y, max_threshold, board_size=8):
    ## every element woule be (cur_x, cur_y, prev_idx), for traceing back the path
    history_record = [(s_x, s_y, -1)] 
    
    found, min_node_weight = recursive_dfs(s_x, s_y, g_x, g_y, history_record, 0, max_threshold=max_threshold, min_node_weight=None, board_size=board_size)
    
    ## construct the path to goal state
    ## if we can't find path, then return None
    if not found:
        sol_pth = None
    else:
        sol_pth = [(history_record[-1][0], history_record[-1][1])]  ## every element is (x, y)
        prev_idx = history_record[-1][2]    ## the previous index of this node
        ## if it hasn't reach the initial state (prev_idx of initial state is -1)
        while prev_idx != -1:
            sol_pth.append((history_record[prev_idx][0], history_record[prev_idx][1]))
            prev_idx = history_record[prev_idx][2]
        sol_pth.reverse()

    return sol_pth, min_node_weight

## IDA* algorithm
def IDA_star(s_x, s_y, g_x, g_y, board_size):
    ## initial process time, to compute the program time
    start_time = time.process_time()

    sol_pth = None  ## the final solution path
    ## set the initial f threshold as h score of initial state
    max_f = utils.compute_h(s_x, s_y, g_x, g_y)  

    ## if it hasn't find the path, then continue
    while sol_pth is None:
        sol_pth, min_node_weight = dfs_heur(s_x, s_y, g_x, g_y, max_threshold=max_f, board_size=board_size)
        
        if sol_pth is not None:
            break
        ## update f threshold as the minimum node weight of drop nodes
        max_f = min_node_weight

    ## calculate the process time
    cost_time = time.process_time() - start_time

    return sol_pth, cost_time