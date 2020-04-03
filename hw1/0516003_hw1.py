import copy

from BFS import BFS_graph
from DFS import DFS_graph
from IDS import IDS
from A_star import A_star
from IDA_star import IDA_star
import utils

## The main running function of this program
def run(algo_type, s_x, s_y, g_x, g_y, board_size=8):
    ## do different search based on algo_type
    if algo_type == 0:
        print("BFS")
        sol_pth, cost_time = BFS_graph(s_x, s_y, g_x, g_y, board_size)
    elif algo_type == 1:
        print("DFS")
        sol_pth, cost_time = DFS_graph(s_x, s_y, g_x, g_y, board_size)
    elif algo_type == 2:
        print("IDS")
        sol_pth, cost_time = IDS(s_x, s_y, g_x, g_y, board_size)
    elif algo_type == 3:
        print("A*")
        sol_pth, cost_time = A_star(s_x, s_y, g_x, g_y, board_size)
    elif algo_type == 4:
        print("IDA*")
        sol_pth, cost_time = IDA_star(s_x, s_y, g_x, g_y, board_size)
    else:
        print("Algo Type Error!")
        exit(1)
    print("---")

    ## print result and cost time
    print(f'It cost {cost_time} sec')
    if sol_pth is None:
        print('Can not find path!')
    else:
        print(f'number of steps = {len(sol_pth)-1}')
        for _, i in enumerate(sol_pth):
            print(f'{i}', end=' ')
        print()

if  __name__ == "__main__":
    algo_type = 4      ## (0: BFS), (1: DFS), (2: IDS), (3: A*), (4: IDA*)
    s_x, s_y = 0, 1     ## starting position
    g_x, g_y = 2, 2     ## target position
    board_size = 25      ## the edge size of square board

    run(algo_type, s_x, s_y, g_x, g_y, board_size)