import time
import utils

def recursive_dfs(cur_x, cur_y, g_x, g_y, board, cur_steps, cur_pth, max_steps, board_size=8):    
    ## if achieve goal state, return the path
    if cur_x == g_x and cur_y == g_y:
        return cur_pth
    
    ## check whether next_steps is greater than threshold
    new_steps = cur_steps+1
    if new_steps > max_steps:
        return None
    
    for move in utils.moves:
        new_x, new_y = cur_x+move[0], cur_y+move[1] ## compute new node coordinate
        
        ## check whether it is valid and this state hasn't expanded or previous expanded depth is deeper
        if utils.check_valid_pos(new_x, new_y, board_size=board_size)\
                and (board[new_x][new_y][0] or new_steps<board[new_x][new_y][1]):
            board[new_x][new_y] = (False, new_steps) ## mark the state as achieved
            cur_pth.append((new_x, new_y))  ## add this node to path list
            
            ## do recursive
            res_pth = recursive_dfs(new_x, new_y, g_x, g_y, board, new_steps, cur_pth, max_steps, board_size=board_size)

            ## if it find the path, then return it
            if res_pth is not None:
                return res_pth
            
            ## if this node could not achieve goal state, remove it from path list
            cur_pth.remove(cur_pth[-1])
    
    return None

def dfs(s_x, s_y, g_x, g_y, max_steps, board_size=8):
    cur_pth = [(s_x, s_y)]

    ## construct board, element is (hasn't expanded, previous expanded depth)
    board = utils.build_board(board_size, (True, 0))

    ## mark the initial state as expanded, and do the recursion
    board[s_x][s_y] = (False, -1)
    sol_pth = recursive_dfs(s_x, s_y, g_x, g_y, board, 0, cur_pth, max_steps, board_size=board_size)

    return sol_pth

def IDS(s_x, s_y, g_x, g_y, board_size):
    ## initial process time, to compute the program time
    start_time = time.process_time()

    ## do iterative DFS, `i` would be the threshold for current iteration
    for i in range(1, board_size**2):
        sol_pth = dfs(s_x, s_y, g_x, g_y, max_steps=i, board_size=board_size)

        ## if achieve goal state, then break this loop
        if sol_pth is not None:
            break

    ## calculate the process time
    cost_time = time.process_time() - start_time

    return sol_pth, cost_time