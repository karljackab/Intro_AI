import time
import utils

def recursive_dfs(cur_x, cur_y, g_x, g_y, board, cur_steps, cur_pth, board_size=8):    
    ## if achieve goal state, return the path
    if cur_x == g_x and cur_y == g_y:
        return cur_pth

    for move in utils.moves:
        new_x, new_y = cur_x+move[0], cur_y+move[1] ## compute new node coordinate
        if utils.check_valid_pos(new_x, new_y, board_size=board_size) and board[new_x][new_y]:  ## check whether it is valid
            board[new_x][new_y] = False ## mark the state as expanded
            cur_pth.append((new_x, new_y))  ## add this node to path list
            
            ## do recursion
            res_pth = recursive_dfs(new_x, new_y, g_x, g_y, board, cur_steps+1, cur_pth, board_size=board_size)

            ## if find the path, then return it
            if res_pth is not None:
                return res_pth
            
            ## if this node could not achieve goal state, remove it from path list
            cur_pth.remove(cur_pth[-1])
    
    return None

def DFS_graph(s_x, s_y, g_x, g_y, board_size=8):
    ## initial process time, to compute the program time
    start_time = time.process_time()

    cur_pth = [(s_x, s_y)]

    ## construct board, element is "True"
    ##      to record which state has been reach, True means it hasn't expanded
    board = utils.build_board(board_size, True)

    ## mark the initial state as expanded, and do the recursion
    board[s_x][s_y] = False
    sol_pth = recursive_dfs(s_x, s_y, g_x, g_y, board, 0, cur_pth, board_size=board_size)
    
    ## calculate the process time
    cost_time = time.process_time() - start_time
    return sol_pth, cost_time