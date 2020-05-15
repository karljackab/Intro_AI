import obj
import time

def experiment_one(x=30, y=16, safe_cells_num=22, Times=100):
    res_cnt = [0, 0]
    print(f'x_size {x}, y_size {y}, test times {Times}')
    for mines_num in range(50, 100, 5):
        res_cnt = [0, 0]
        tot_time = 0.0
        for _ in range(Times):
            Env = obj.Environment(x, y, mines_num)
            safe_cell_list = Env.give_safe_cells(safe_cells_num)

            start = time.time()
            Player = obj.Agent(x, y, mines_num, safe_cell_list)
            res = Player.process(Env)
            this_time = time.time() - start
            tot_time += this_time
            if res:
                res_cnt[0] += 1
            else:
                res_cnt[1] += 1
        print(f'{mines_num}: success {res_cnt[0]}, lose {res_cnt[1]}, time {tot_time/Times}')

def experiment_two(x=9, y=9, mines_num=10, start_safe_num=1, Times=100):
    print(f'x_size {x}, y_size {y}, mines_num {mines_num}, test times {Times}')
    for safe_cells_num in range(start_safe_num, x*y, 5):
        acc_cnt = 0
        tot_time = 0.0
        for i in range(Times):
            Env = obj.Environment(x, y, mines_num)
            safe_cell_list = Env.give_safe_cells(safe_cells_num)

            start = time.time()
            Player = obj.Agent(x, y, mines_num, safe_cell_list)
            res = Player.process(Env)
            this_time = time.time() - start
            tot_time += this_time
            if res:
                acc_cnt += 1
        accuracy = acc_cnt/(Times)
        print(f'{safe_cells_num}: accuracy {accuracy}, time {tot_time/Times}')
        if accuracy >= 0.9:
            break


# experiment_one()
experiment_two(x=30, y=16, mines_num=99, start_safe_num=200, Times=20)