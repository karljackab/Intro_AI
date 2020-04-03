import copy

moves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

def check_valid_pos(x, y, board_size=8):
    ## if it has been outside the board, then return False, otherwise return True
    if x < 0 or y < 0 or x >= board_size or y >= board_size:
        return False
    return True

## build initla board for BFS and DFS
def build_board(board_size, element):
    board = [
        [
            copy.deepcopy(element) for _ in range(board_size)
        ] for _ in range(board_size)
    ]
    return board

def compute_h(new_x, new_y, g_x, g_y):
    ## compute h score, would be (|dx|+|dy|)/3
    return int((max(0, g_x-new_x)+max(0, g_y-new_y))/3)

def compute_g(prev_cost):
    ## compute g score (unit cost)
    return prev_cost

def compute_f(new_x, new_y, g_x, g_y, cur_cost):
    ## compute f score, add by h score and g score
    return compute_h(new_x, new_y, g_x, g_y) + compute_g(cur_cost)

