## experiment.py

import main
import gen_case
import utils
import copy
import time

def display_capacity(version_list, time_list):
    print('----------------------')
    for idx in range(len(version_list)):
        print(f'{version_list[idx]}: {time_list[idx]}')

def capacity_testing(version_list, size=8, round_num=5):
    out_cnt = 0
    time_list = [[], [], [], []] ## for capacity testing, element would be(size, time)
    orig_version = copy.deepcopy(version_list)
    while out_cnt < 4:
        mines_num, hint_num = round(size*size*0.277777), round(size*size*0.444444)
        time_sum_list = [0, 0, 0, 0]
        display_capacity(orig_version, time_list)

        for idx in range(round_num):
            inp = gen_case.gen_case(size, size, mines_num, hint_num)
            _, board, domains, constraints, constraint_list = utils.parse_input(list(map(lambda x: int(x), inp.split(' '))))
            for ver_idx, ver in enumerate(version_list):
                if ver == 'Out':
                    continue

                sub_board, sub_domains = copy.deepcopy(board), copy.deepcopy(domains)
                ## Start search
                st = time.process_time()
                sub_board, _ = main.solve(sub_board, sub_domains, constraints, constraint_list, forward_check, ver)
                et = time.process_time()
                time_sum_list[ver_idx] += et-st

                if sub_board is None:
                    print(f"ERROR! {ver}")
                    exit(1)
        
        for idx in range(4):
            avg_time = time_sum_list[idx]/round_num
            if avg_time != 0:
                time_list[idx].append((size, avg_time))
                if avg_time > 1:
                    out_cnt += 1
                    version_list[idx] = 'Out'
        
        size += 1
    display_capacity(orig_version, time_list)

if __name__ == "__main__":
    ## Setting
    x_size, y_size = 6, 6
    mines_num, hint_num = 10, 8
    round_num = 500
    forward_check = True
    version_list = ['None', 'MRV', 'Degree', 'LCV']

    node_sum_list = [0, 0, 0, 0]
    time_sum_list = [0, 0, 0, 0]

    for idx in range(round_num):
        print('==================')
        print(f'Round {idx}:')
        inp = gen_case.gen_case(x_size, y_size, mines_num, hint_num)
        orig_map, board, domains, constraints, constraint_list = utils.parse_input(list(map(lambda x: int(x), inp.split(' '))))
        utils.print_board(orig_map, board)
        for ver_idx, ver in enumerate(version_list):
            print(ver, end=' ')
            sub_board, sub_domains = copy.deepcopy(board), copy.deepcopy(domains)
            ## Start search
            st = time.process_time()
            sub_board, node_num = main.solve(sub_board, sub_domains, constraints, constraint_list, forward_check, ver)
            et = time.process_time()
            time_sum_list[ver_idx] += et-st

            if sub_board is None:
                print(f"ERROR! {ver}")
                exit(1)

            node_sum_list[ver_idx] += node_num
        print()

    print('=======================')
    print(f'Board Size: ({x_size}, {y_size})')
    print(f'Mines Number: {mines_num}')
    print(f'Hints Number: {hint_num}')
    print(f'Sample Number: {round_num}')
    print()
    for ver_idx, ver in enumerate(version_list):
        print(f'{ver}: {node_sum_list[ver_idx]/round_num}, {time_sum_list[ver_idx]/round_num}s')