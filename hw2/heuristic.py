import copy

def simple(cur_board, cur_domains, process_stack):
    for (new_x, new_y) in cur_domains.keys():
        domain = cur_domains[(new_x, new_y)]
        for new_val, available in enumerate(domain):
            if available:
                new_board, new_domains = copy.deepcopy(cur_board), copy.deepcopy(cur_domains)
                del new_domains[(new_x, new_y)]
                new_board[new_y][new_x] = new_val
                process_stack.append((new_board, new_domains))

def MRV(cur_board, cur_domains, process_stack):
    priority_seq = []
    for (new_x, new_y) in cur_domains.keys():
        avail_num = sum(cur_domains[(new_x, new_y)])
        priority_seq.append(((new_x, new_y), avail_num))
    priority_seq = sorted(priority_seq, key=lambda x: x[1])
    priority_seq.reverse()
    for node in priority_seq:
        (new_x, new_y) = node[0]
        domain = cur_domains[(new_x, new_y)]
        for new_val, available in enumerate(domain):
            if available:
                new_board, new_domains = copy.deepcopy(cur_board), copy.deepcopy(cur_domains)
                del new_domains[(new_x, new_y)]
                new_board[new_y][new_x] = new_val
                process_stack.append((new_board, new_domains))

def Degree(cur_board, cur_domains, process_stack, constraints):
    priority_seq = []
    for (new_x, new_y) in cur_domains.keys():
        constraint_num = len(constraints[(new_x, new_y)])
        priority_seq.append(((new_x, new_y), constraint_num))
    priority_seq = sorted(priority_seq, key=lambda x: x[1])
    
    for node in priority_seq:
        (new_x, new_y) = node[0]
        domain = cur_domains[(new_x, new_y)]
        for new_val, available in enumerate(domain):
            if available:
                new_board, new_domains = copy.deepcopy(cur_board), copy.deepcopy(cur_domains)
                del new_domains[(new_x, new_y)]
                new_board[new_y][new_x] = new_val
                process_stack.append((new_board, new_domains))