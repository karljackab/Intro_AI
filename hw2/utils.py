import copy

def add_constraint(constraints, constraint_list, x_idx, y_idx, board, x_size, y_size):
    node_list = []
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if y_idx+y < 0 or x_idx+x < 0 or x_idx+x >= x_size or y_idx+y >= y_size:
                continue
            if board[y_idx+y][x_idx+x] == -1:
                node_list.append((x_idx+x, y_idx+y))
    for node in node_list:
        constraints[node].append((node_list, board[y_idx][x_idx]))
    constraint_list.append((node_list, board[y_idx][x_idx]))

    return constraints, constraint_list

def parse_input(inp):
    x_size, y_size, mines_num = inp[0], inp[1], inp[2]
    board = []

    ## key: (x, y)
    ## value: [[True, True], True], it's domain and it's unassigned or not
    domains = dict()

    ## every elements in constraints would be dict
    ## key: (x, y)
    ## value: [constraint, constraint]
    ## the constraint would be ([(node1), (node2), (node3), ...], constraint value)
    constraints = dict()
    constraint_list = []

    for y_idx in range(y_size):
        board.append([])
        for x_idx in range(x_size):
            val = inp[3 + y_idx*x_size + x_idx]
            board[-1].append(val)
            if val == -1:   ## variable
                # domains[(x_idx, y_idx)] = [True, True]
                domains[(x_idx, y_idx)] = [[True, True], True]
                constraints[(x_idx, y_idx)] = list()

    for y_idx in range(y_size):
        for x_idx in range(x_size):
            if board[y_idx][x_idx] != -1:
                ## add constraints
                add_constraint(constraints, constraint_list, x_idx, y_idx, board, x_size, y_size)
    
    ## add global constraint
    node_list = [node for node in domains.keys()]
    for node in node_list:
        constraints[node].append((node_list, mines_num))
    constraint_list.append((node_list, mines_num))

    orig_map = copy.deepcopy(board)

    for y_idx in range(y_size):
        for x_idx in range(x_size):
            board[y_idx][x_idx] = 0

    return orig_map, board, domains, constraints, constraint_list

def check_accept(board, constraint_list):
    for constraint in constraint_list:
        node_list, tar_value = constraint
        value = sum([board[y][x] for x, y in node_list])
        if value != tar_value:
            return False
    return True

def check_avail(board, domains, constraint_list, just_calc=False):
    history = []    ## changed history, element would be (node, idx)
    out_cnt = 0
    for constraint in constraint_list:
        node_list, tar_value = constraint
        value = sum([board[y][x] for x, y in node_list])
        upper_bound, lower_bound = value, value

        for node in node_list:
            # if node in domains:
            if domains[node][1]:
                if domains[node][0][1]:
                    upper_bound += 1
                elif not domains[node][0][0] and domains[node][0][1]:
                    lower_bound += 1

        if upper_bound < tar_value or lower_bound > tar_value:
            if not just_calc:
                return False, history
            else:
                return False, out_cnt

        if upper_bound == tar_value:    ## set all domains to upper bound value
            for node in node_list:
                # if node in domains:
                if domains[node][1]:
                    if not domains[node][1]:
                        continue
                    if domains[node][0][1] and domains[node][0][0]:
                        if not just_calc:
                            history.append((node, 0))
                            domains[node][0][0] = False
                        else:
                            out_cnt += 1

        if lower_bound == tar_value:    ## set all domains to lower bound value
            for node in node_list:
                # if node in domains:
                if domains[node][1]:
                    if not domains[node][1]:
                        continue
                    if domains[node][0][0] and domains[node][0][1]:
                        if not just_calc:
                            history.append((node, 1))
                            domains[node][0][1] = False
                        else:
                            out_cnt += 1
    if not just_calc:
        return True, history
    else:
        return True, out_cnt

def reverse_domain_hist(domains, history):
    for node, idx in history:
        domains[node][0][idx] = True

def print_board(orig_map, board):
    for y_idx in range(len(orig_map)):
        for x_idx in range(len(orig_map[0])):
            if orig_map[y_idx][x_idx] != -1:
                print(orig_map[y_idx][x_idx], end=' ')
            elif board[y_idx][x_idx] == 0:
                print('O', end=' ')
            else:
                print('X', end=' ')
        print()