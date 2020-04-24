## recur_heur.py

import utils

expanded_node_cnt = 0

## Without heuristic version
def simple(cur_board, cur_domains, constraints, constraint_list, changed_node, forward_check):
    global expanded_node_cnt
    ## Do forward checking, only check the constraints which affect changed node
    if changed_node is not None and forward_check:
        check_res, history = utils.check_avail(cur_board, cur_domains, constraints[changed_node])
        ## If checking fail, reverse the changed domain, and back to previous node
        if not check_res:
            utils.reverse_domain_hist(cur_domains, history)
            return None
    
    ## If all domains has assigned (reach the leaf), check whether it's acceptable
    ## If failed, reverse and go back to previous node
    ## If succeed, return the solution
    if sum([cur_domains[key][1] for key in cur_domains]) == 0:
        if not utils.check_accept(cur_board, constraint_list):
            if forward_check:
                utils.reverse_domain_hist(cur_domains, history)
            return None
        else:
            return cur_board

    ## Find the node which hasn't assigned
    for (x, y) in cur_domains.keys():
        if not cur_domains[(x, y)][1]:
            continue
        new_x, new_y = x, y
        break

    ## Expand node
    expanded_node_cnt += 1
    domain, _ = cur_domains[(new_x, new_y)]
    for new_val, available in enumerate(domain):
        ## If the domain value is available
        if available:
            cur_domains[(new_x, new_y)][1] = False
            cur_board[new_y][new_x] = new_val
            res = simple(cur_board, cur_domains, constraints, constraint_list, (new_x, new_y), forward_check)
            ## If it has solution, return it
            if res is not None:
                return res
            ## Go back to previous status
            cur_domains[(new_x, new_y)][1] = True
            cur_board[new_y][new_x] = 0

    ## Reverse changed by forward checking
    if changed_node is not None and forward_check:
        utils.reverse_domain_hist(cur_domains, history)
    
    return None

def MRV(cur_board, cur_domains, constraints, constraint_list, changed_node, forward_check):
    global expanded_node_cnt
    ## Do forward checking, only check the constraints which affect changed node
    if changed_node is not None and forward_check:
        check_res, history = utils.check_avail(cur_board, cur_domains, constraints[changed_node])
        
        ## If checking fail, reverse the changed domain, and back to previous node
        if not check_res:
            utils.reverse_domain_hist(cur_domains, history)
            return None
    
    ## If all domains has assigned (reach the leaf), check whether it's acceptable
    ## If failed, reverse and go back to previous node
    ## If succeed, return the solution
    if sum([cur_domains[key][1] for key in cur_domains]) == 0:
        if not utils.check_accept(cur_board, constraint_list):
            if forward_check:
                utils.reverse_domain_hist(cur_domains, history)
            return None
        else:
            return cur_board

    ## Choose the node to expand which has minimum available domain
    new_node, min_avail_num = None, -1
    for (new_x, new_y) in cur_domains.keys():
        if not cur_domains[(new_x, new_y)][1]:
            continue
        avail_num = sum(cur_domains[(new_x, new_y)][0])
        if avail_num < min_avail_num or min_avail_num == -1:
            new_node, min_avail_num = (new_x, new_y), avail_num
    
    ## Expand nodes in priority sequence
    expanded_node_cnt += 1
    new_x, new_y = new_node
    domain, _ = cur_domains[(new_x, new_y)]
    for new_val, available in enumerate(domain):
        ## If the domain value is available
        if available:
            cur_domains[(new_x, new_y)][1] = False
            cur_board[new_y][new_x] = new_val
            res = MRV(cur_board, cur_domains, constraints, constraint_list, (new_x, new_y), forward_check)
                
            ## If it has solution, return it
            if res is not None:
                return res
                
            ## Go back to previous status
            cur_domains[(new_x, new_y)][1] = True
            cur_board[new_y][new_x] = 0

    ## Reverse the changed by forward checking
    if changed_node is not None and forward_check:
        utils.reverse_domain_hist(cur_domains, history)
    
    return None

def Degree(cur_board, cur_domains, constraints, constraint_list, changed_node, forward_check):
    global expanded_node_cnt
    
    ## Do forward checking, only check the constraints which affect changed node
    if changed_node is not None and forward_check:
        check_res, history = utils.check_avail(cur_board, cur_domains, constraints[changed_node])
        
        ## If checking fail, reverse the changed domain, and back to previous node
        if not check_res:
            utils.reverse_domain_hist(cur_domains, history)
            return None
    
    ## If all domains has assigned (reach the leaf), check whether it's acceptable
    ## If failed, reverse and go back to previous node
    ## If succeed, return the solution
    if sum([cur_domains[key][1] for key in cur_domains]) == 0:
        if not utils.check_accept(cur_board, constraint_list):
            if forward_check:
                utils.reverse_domain_hist(cur_domains, history)
            return None
        else:
            return cur_board

    ## Choose the node to expand which has maximum constraint number
    new_node, max_constraint_num = None, -1
    for (new_x, new_y) in cur_domains.keys():
        if not cur_domains[(new_x, new_y)][1]:
            continue
        constraint_num = len(constraints[(new_x, new_y)])
        if constraint_num > max_constraint_num:
            new_node, max_constraint_num = (new_x, new_y), constraint_num

    ## Expand the node
    expanded_node_cnt += 1
    (new_x, new_y) = new_node
    domain, _ = cur_domains[(new_x, new_y)]
    for new_val, available in enumerate(domain):
        ## If the domain value is available
        if available:
            cur_domains[(new_x, new_y)][1] = False
            cur_board[new_y][new_x] = new_val
            res = Degree(cur_board, cur_domains, constraints, constraint_list, (new_x, new_y), forward_check)
                
            ## If it has solution, return it
            if res is not None:
                return res
                
            ## Go back to previous status
            cur_domains[(new_x, new_y)][1] = True
            cur_board[new_y][new_x] = 0

    ## Reverse the changed by forward checking
    if changed_node is not None and forward_check:
        utils.reverse_domain_hist(cur_domains, history)
    
    return None

def LCV(cur_board, cur_domains, constraints, constraint_list, changed_node, forward_check):
    global expanded_node_cnt
    ## Do forward checking, only check the constraints which affect changed node
    if changed_node is not None and forward_check:
        check_res, history = utils.check_avail(cur_board, cur_domains, constraints[changed_node])

        ## If checking fail, reverse the changed domain, and back to previous node
        if not check_res:
            utils.reverse_domain_hist(cur_domains, history)
            return None
    
    ## If all domains has assigned (reach the leaf), check whether it's acceptable
    ## If failed, reverse and go back to previous node
    ## If succeed, return the solution
    if sum([cur_domains[key][1] for key in cur_domains]) == 0:
        if not utils.check_accept(cur_board, constraint_list):
            if forward_check:
                utils.reverse_domain_hist(cur_domains, history)
            return None
        else:
            return cur_board

    ## Find the node which hasn't assigned
    for (x, y) in cur_domains.keys():
        if not cur_domains[(x, y)][1]:
            continue
        new_x, new_y = x, y
        break

    value_seq = []
    if cur_domains[(new_x, new_y)][0][0] and cur_domains[(new_x, new_y)][0][1]:
        ## sort the value in increasing order
        cur_domains[(new_x, new_y)][1] = False
        cur_board[new_y][new_x] = 0
        zero_can_do, zero_out_cnt = utils.check_avail(
            cur_board, cur_domains, constraints[(new_x, new_y)], True
        )
        cur_board[new_y][new_x] = 1
        one_can_do, one_out_cnt = utils.check_avail(
            cur_board, cur_domains, constraints[(new_x, new_y)], True
        )
        cur_board[new_y][new_x] = 0
        cur_domains[(new_x, new_y)][1] = True
        if zero_can_do and one_can_do:
            if zero_out_cnt > one_out_cnt:
                value_seq = [1, 0]
            else:
                value_seq = [0, 1]
        elif zero_can_do:
            value_seq = [0]
        elif one_can_do:
            value_seq = [1]
    elif cur_domains[(new_x, new_y)][0][0]:
        value_seq = [0]
    elif cur_domains[(new_x, new_y)][0][1]:
        value_seq = [1]

    expanded_node_cnt += 1
    for new_val in value_seq:
        cur_domains[(new_x, new_y)][1] = False
        cur_board[new_y][new_x] = new_val
        res = LCV(cur_board, cur_domains, constraints, constraint_list, (new_x, new_y), forward_check)
                        
        ## If it has solution, return it
        if res is not None:
            return res
                        
        ## Go back to previous status
        cur_domains[(new_x, new_y)][1] = True
        cur_board[new_y][new_x] = 0

    ## Reverse the changed by forward checking
    if changed_node is not None and forward_check:
        utils.reverse_domain_hist(cur_domains, history)
        
    return None