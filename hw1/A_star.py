import time
import heapq
import utils

def A_star(s_x, s_y, g_x, g_y, board_size=8):
    ## initial process time, to compute the program time
    start_time = time.process_time()

    history_record = [] ## every element woule be (cur_x, cur_y, prev_idx), for traceing back the path
    frontier = [] ## every element would be (f, new_x, new_y, prev_hist_idx, new_g)

    ## add first node to priority queue
    heapq.heappush(frontier, (0, s_x, s_y, None, 0))
    done = False

    while len(frontier) > 0:
        node = heapq.heappop(frontier)
        history_record.append((node[1], node[2], node[3]))
        prev_hist_idx = len(history_record)-1   ## get the index of last history_record

        ## check if the node is goal state
        if node[1] == g_x and node[2] == g_y:
            done = True
            break

        ## push new nodes to frontier
        for move in utils.moves:
            new_x, new_y = node[1]+move[0], node[2]+move[1] ## compute new node coordinate
            if utils.check_valid_pos(new_x, new_y, board_size=board_size):    ## check if it is valid
                new_g = node[4]+1   ## compute g score
                f = utils.compute_f(new_x, new_y, g_x, g_y, new_g)  ## compute f score of new node

                ## add it to frontier
                heapq.heappush(frontier, (f, new_x, new_y, prev_hist_idx, new_g))
    
    ## calculate the process time
    cost_time = time.process_time() - start_time

    ## construct the path to goal state
    ## if it didn't find path, then return None
    if not done:
        sol_pth = None
    else:
        sol_pth = [(history_record[-1][0], history_record[-1][1])]  ## every element is (x, y)
        prev_idx = history_record[-1][2]    ## the previous index of this node
        
        ## if it hasn't reach the initial state (prev_idx of initial state is None)
        while prev_idx is not None: 
            sol_pth.append((history_record[prev_idx][0], history_record[prev_idx][1]))
            prev_idx = history_record[prev_idx][2]
        sol_pth.reverse()

    return sol_pth, cost_time