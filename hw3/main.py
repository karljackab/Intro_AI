import obj

x, y = 30, 16
Times = 100

res_cnt = [0, 0]
print(f'x_size {x}, y_size {y}, test times {Times}')
for mines_num in range(30, 80, 2):
    res_cnt = [0, 0]
    for i in range(Times):
        Env = obj.Environment(x, y, mines_num)
        safe_cell_list = Env.give_safe_cells(22)

        Player = obj.Agent(x, y, mines_num, safe_cell_list)
        res = Player.process(Env)
        if res:
            res_cnt[0] += 1
        else:
            res_cnt[1] += 1
    print(f'{mines_num}: success {res_cnt[0]}, lose {res_cnt[1]}')