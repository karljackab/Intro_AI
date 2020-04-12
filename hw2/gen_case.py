import random

def gen_case(x_size, y_size, mines_num, hint_num):
    board = []
    res = ''
    for _ in range(y_size):
        board.append([])
        for _ in range(x_size):
            board[-1].append('O')

    done_mine_num = 0
    while done_mine_num != mines_num:
        x, y = random.randint(0, x_size-1), random.randint(0, y_size-1)
        if board[y][x] == 'O':
            board[y][x] = 'X'
            done_mine_num += 1
    
    done_hint_num = 0
    while done_hint_num != hint_num:
        x, y = random.randint(0, x_size-1), random.randint(0, y_size-1)
        if board[y][x] == 'O':
            cnt = 0
            for y_d in [-1, 0, 1]:
                for x_d in [-1, 0, 1]:
                    if x+x_d<0 or x+x_d>=x_size or y+y_d<0 or y+y_d>=y_size:
                        continue
                    if board[y+y_d][x+x_d] == 'X':
                        cnt += 1
            board[y][x] = cnt
            done_hint_num += 1

    # for y in range(y_size):
    #     for x in range(x_size):
    #         print(board[y][x], end=' ')
    #     print()

    print(f'{x_size} {y_size} {mines_num}',end=' ')
    res = f'{x_size} {y_size} {mines_num} '
    for y in range(y_size):
        for x in range(x_size):
            if type(board[y][x]) == int:
                print(f'{board[y][x]}',end='')
                res += f'{board[y][x]}'
            else:
                print('-1',end='')
                res += '-1'
            if x != x_size-1 or y != y_size-1:
                print(' ',end='')
                res += ' '
    print()
    return res

if __name__ == '__main__':
    gen_case(4, 4, 5, 4)