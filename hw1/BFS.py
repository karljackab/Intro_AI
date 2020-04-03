import time
import utils

def BFS_graph(s_x, s_y, g_x, g_y, board_size=8):
    ## initial process time, to compute the program time
    start_time = time.process_time()

    ## construct the board
    ## the element would be (prev_x, prev_y, current_length)
    board = utils.build_board(board_size, (0, 0, 0))

    frontier = [(s_x, s_y, 0)]  ## frontier list as a queue
    done = False

    while len(frontier) > 0 and not done:
        cur_pos = frontier[0]   ## get one node from frontier list
        frontier.remove(cur_pos) ## pop out the current node from frontier list

        for move in utils.moves:
            new_x, new_y = cur_pos[0]+move[0], cur_pos[1]+move[1]   ## compute new node coordinate

            ## check whether it is valid
            if utils.check_valid_pos(new_x, new_y, board_size=board_size) and board[new_x][new_y][2] == 0:
                board[new_x][new_y] = (cur_pos[0], cur_pos[1], cur_pos[2]+1)    ## update the board values
                frontier.append((new_x, new_y, cur_pos[2]+1))   ## add new node to frontier

            ## if achieve goal state, break it
            if new_x == g_x and new_y == g_y:
                done = True
                break

    ## calculate the process time
    cost_time = time.process_time() - start_time

    ## construct the path from initial state to goal state
    if board[g_x][g_y][2] == 0: ## if the goal state hasn't achieve, set sol_pth as None
        sol_pth = None
    else:
        sol_pth = [(g_x, g_y)]
        ## add nodes to sol_pth until the sol_pth has initial state
        while sol_pth[-1][0] != s_x or sol_pth[-1][1] != s_y:
            prev_pos = board[sol_pth[-1][0]][sol_pth[-1][1]]   ## get previous node
            sol_pth.append((prev_pos[0], prev_pos[1]))
        sol_pth.reverse()

    return sol_pth, cost_time