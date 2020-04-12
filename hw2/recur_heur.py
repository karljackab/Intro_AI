import utils

def simple(cur_board, cur_domains, constraints, constraint_list, changed_node, forward_check, node_num):
    # print(node_num)
    if changed_node is not None and forward_check:
        check_res, history = utils.check_avail(cur_board, cur_domains, constraints[changed_node])
        if not check_res:
            utils.reverse_domain_hist(cur_domains, history)
            return None, node_num
    
    if sum([cur_domains[key][1] for key in cur_domains]) == 0:
        if not utils.check_accept(cur_board, constraint_list):
            if forward_check:
                utils.reverse_domain_hist(cur_domains, history)
            return None, node_num
        else:
            return cur_board, node_num

    for (new_x, new_y) in cur_domains.keys():
        if not cur_domains[(new_x, new_y)][1]:
            continue
        domain, _ = cur_domains[(new_x, new_y)]
        for new_val, available in enumerate(domain):
            if available:
                cur_domains[(new_x, new_y)][1] = False
                cur_board[new_y][new_x] = new_val
                res, node_num = simple(cur_board, cur_domains, constraints, constraint_list, (new_x, new_y), forward_check, node_num+1)
                if res is not None:
                    return res, node_num
                cur_domains[(new_x, new_y)][1] = True
                cur_board[new_y][new_x] = 0

    if forward_check:
        utils.reverse_domain_hist(cur_domains, history)
    
    return None, node_num

def MRV(cur_board, cur_domains, constraints, constraint_list, changed_node, forward_check, node_num):
    if changed_node is not None and forward_check:
        check_res, history = utils.check_avail(cur_board, cur_domains, constraints[changed_node])
        if not check_res:
            utils.reverse_domain_hist(cur_domains, history)
            return None, node_num
    
    if sum([cur_domains[key][1] for key in cur_domains]) == 0:
        if not utils.check_accept(cur_board, constraint_list):
            if forward_check:
                utils.reverse_domain_hist(cur_domains, history)
            return None, node_num
        else:
            return cur_board, node_num

    priority_seq = []
    for (new_x, new_y) in cur_domains.keys():
        if not cur_domains[(new_x, new_y)][1]:
            continue
        avail_num = sum(cur_domains[(new_x, new_y)][0])
        priority_seq.append(((new_x, new_y), avail_num))
    priority_seq = sorted(priority_seq, key=lambda x: x[1])
    priority_seq.reverse()

    ## expand node
    for node in priority_seq:
        (new_x, new_y) = node[0]
        domain, _ = cur_domains[(new_x, new_y)]
        for new_val, available in enumerate(domain):
            if available:
                cur_domains[(new_x, new_y)][1] = False
                cur_board[new_y][new_x] = new_val
                res, node_num = MRV(cur_board, cur_domains, constraints, constraint_list, (new_x, new_y), forward_check, node_num+1)
                if res is not None:
                    return res, node_num
                cur_domains[(new_x, new_y)][1] = True
                cur_board[new_y][new_x] = 0

    if forward_check:
        utils.reverse_domain_hist(cur_domains, history)
    return None, node_num

def Degree(cur_board, cur_domains, constraints, constraint_list, changed_node, forward_check, node_num):
    if changed_node is not None and forward_check:
        check_res, history = utils.check_avail(cur_board, cur_domains, constraints[changed_node])
        if not check_res:
            utils.reverse_domain_hist(cur_domains, history)
            return None, node_num
    
    if sum([cur_domains[key][1] for key in cur_domains]) == 0:
        if not utils.check_accept(cur_board, constraint_list):
            if forward_check:
                utils.reverse_domain_hist(cur_domains, history)
            return None, node_num
        else:
            return cur_board, node_num

    priority_seq = []
    for (new_x, new_y) in cur_domains.keys():
        if not cur_domains[(new_x, new_y)][1]:
            continue
        constraint_num = len(constraints[(new_x, new_y)])
        priority_seq.append(((new_x, new_y), constraint_num))
    priority_seq = sorted(priority_seq, key=lambda x: x[1])
    
    ## expand node
    for node in priority_seq:
        (new_x, new_y) = node[0]
        domain, _ = cur_domains[(new_x, new_y)]
        for new_val, available in enumerate(domain):
            if available:
                cur_domains[(new_x, new_y)][1] = False
                cur_board[new_y][new_x] = new_val
                res, node_num = Degree(cur_board, cur_domains, constraints, constraint_list, (new_x, new_y), forward_check, node_num+1)
                if res is not None:
                    return res, node_num
                cur_domains[(new_x, new_y)][1] = True
                cur_board[new_y][new_x] = 0

    if forward_check:
        utils.reverse_domain_hist(cur_domains, history)
    return None, node_num

def LCV(cur_board, cur_domains, constraints, constraint_list, changed_node, forward_check, node_num):
    if changed_node is not None and forward_check:
        check_res, history = utils.check_avail(cur_board, cur_domains, constraints[changed_node])
        if not check_res:
            utils.reverse_domain_hist(cur_domains, history)
            return None, node_num
    
    if sum([cur_domains[key][1] for key in cur_domains]) == 0:
        if not utils.check_accept(cur_board, constraint_list):
            if forward_check:
                utils.reverse_domain_hist(cur_domains, history)
            return None, node_num
        else:
            return cur_board, node_num

    check_rm_history, priority_seq = [], []
    for (new_x, new_y) in cur_domains.keys():
        if not cur_domains[(new_x, new_y)][1]:
            continue
        domain, _ = cur_domains[(new_x, new_y)]
        for new_val, available in enumerate(domain):
            if available:
                cur_domains[(new_x, new_y)][1] = False
                cur_board[new_y][new_x] = new_val
                can_do, out_cnt = utils.check_avail(
                    cur_board, cur_domains, constraints[(new_x, new_y)], True
                )
                cur_domains[(new_x, new_y)][1] = True
                cur_board[new_y][new_x] = 0
                if not can_do:
                    cur_domains[(new_x, new_y)][0][new_val] = False
                    check_rm_history.append(((new_x, new_y), new_val))
                else:
                    priority_seq.append(((new_x, new_y, new_val), out_cnt))
    
    priority_seq = sorted(priority_seq, key=lambda x: x[1])
    priority_seq.reverse()

    for node in priority_seq:
        (new_x, new_y, new_val) = node[0]
        domain, _ = cur_domains[(new_x, new_y)]
        
        cur_domains[(new_x, new_y)][1] = False
        cur_board[new_y][new_x] = new_val
        res, node_num = LCV(cur_board, cur_domains, constraints, constraint_list, (new_x, new_y), forward_check, node_num+1)
        if res is not None:
            return res, node_num
        cur_domains[(new_x, new_y)][1] = True
        cur_board[new_y][new_x] = 0

    if forward_check:
        utils.reverse_domain_hist(cur_domains, history)
    
    for (x, y), val in check_rm_history:
        cur_domains[(x, y)][0][val] = True

    return None, node_num