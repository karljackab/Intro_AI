import random
import itertools

class Environment():
    def __init__(self, x_size, y_size, mines_num):
        self.board = []
        self.x_size = x_size
        self.y_size = y_size
        self.mines_num = mines_num

        ## initial board
        for _ in range(y_size):
            self.board.append([])
            for _ in range(x_size):
                self.board[-1].append([False, 0])   ## [is_mine, mines_num_around_it]

        ## create mines
        done_mine_num = 0
        while done_mine_num != mines_num:
            x, y = random.randint(0, x_size-1), random.randint(0, y_size-1)
            if not self.board[y][x][0]:
                self.board[y][x] = [True, -1]
                done_mine_num += 1

        ## update safe cell number
        for y in range(y_size):
            for x in range(x_size):
                if not self.board[y][x][0]:
                    self.board[y][x][1] = self.get_sur_mines_num(x, y)

    ## get surrounding mines number
    def get_sur_mines_num(self, x_idx, y_idx):
        mines_cnt = 0
        for dy in [-1, 0, 1]:
            if y_idx+dy < 0 or y_idx+dy >= self.y_size:
                continue
            new_y = y_idx+dy
            for dx in [-1, 0, 1]:
                if x_idx+dx < 0 or x_idx+dx >= self.x_size:
                    continue
                new_x = x_idx+dx 
                if self.board[new_y][new_x][0]:
                    mines_cnt += 1
        return mines_cnt

    ## display whole board
    def show_whole_board(self):
        for y in range(self.y_size):
            for x in range(self.x_size):
                if self.board[y][x][0]:
                    print('X', end=', ')
                else:
                    print(self.board[y][x][1], end=', ')
            print()

    ## give safe cells list (for initial player)
    def give_safe_cells(self, safe_num):
        done_num = 0
        safe_list = []  ## element: (x_idx, y_idx, sur_mines_num)
        # x, y = random.randint(0, self.x_size-1), random.randint(0, self.y_size-1)
        while done_num != safe_num:
            x, y = random.randint(0, self.x_size-1), random.randint(0, self.y_size-1)
            if (not self.board[y][x][0]) and ((x, y, self.board[y][x][1]) not in safe_list):
                safe_list.append((x, y, self.board[y][x][1]))
                done_num += 1
            # dx, dy = random.randint(-1, 1), random.randint(-1, 1)
            # if x+dx >= 0 and x+dx < self.x_size:
            #     x = x+dx
            # if y+dy >= 0 and y+dy < self.y_size:
            #     y = y+dy
        
        return safe_list

class Agent():
    def __init__(self, x_size, y_size, mines_num, safe_cell_list):
        self.board = []
        self.x_size = x_size
        self.y_size = y_size
        self.mines_num = mines_num
        self.KB0 = dict()
        self.KB = []    ## element: [[Pos_or_Neg(True/False), x_idx, y_idx], ...]
        
        self.neighbor = []

        ## initial player's board and neighbor list for every cell
        for y_idx in range(y_size):
            self.board.append([])
            self.neighbor.append([])
            for x_idx in range(x_size):
                self.board[-1].append([False, -1])   ## [has_assigned, assigned_value(False means not mine)]
                neig = []
                for dy in [-1, 0, 1]:
                    if y_idx+dy < 0 or y_idx+dy >= self.y_size:
                        continue
                    for dx in [-1, 0, 1]:
                        if x_idx+dx < 0 or x_idx+dx >= self.x_size or (dx==0 and dy==0):
                            continue
                        neig.append((x_idx+dx, y_idx+dy))
                self.neighbor[-1].append(neig)

        ## put initial safe cell
        self.init_safe_cell(safe_cell_list)

    ## display the board the user currently know
    def show_current_board(self):
        print('==============================')
        for y_idx in range(self.y_size):
            for x_idx in range(self.x_size):
                if (x_idx, y_idx) in self.KB0.keys():
                    if self.board[y_idx][x_idx][1] < 0:
                        print('X', end=', ')
                    else:
                        print(self.board[y_idx][x_idx][1], end=', ')
                else:
                    print('-', end=', ')
            print()

    ## check sen2 contain sen1, for subsumption
    def all_in(self, sen1, sen2):
        success = True
        for element1 in sen1:
            for element2 in sen2:
                if not (element1 == element2):
                    success = False
                    break
            if not success:
                break
        return success

    ## insert a sentence to KB
    def insert_KB(self, sentence):
        if len(sentence) > 1:
            del_list = []
            sentence_len = len(sentence)

            ## Apply KB0 knowledge to shrink sentence
            for idx in range(sentence_len):
                if (sentence[idx][1], sentence[idx][2]) in self.KB0.keys():
                    if (self.KB0[(sentence[idx][1], sentence[idx][2])] and sentence[idx][0])\
                        or (not self.KB0[(sentence[idx][1], sentence[idx][2])] and not sentence[idx][0]):
                        return
                    else:
                        del_list.append(idx)
            del_list.reverse()
            self.check_dec_order(del_list)
            for idx in del_list:
                del sentence[idx]

            ## Check subsumption
            del_list = []
            for idx in range(len(self.KB)):
                if sentence_len < len(self.KB[idx]) and self.all_in(sentence, self.KB[idx]):
                    del_list.append(idx)
                elif sentence_len > len(self.KB[idx]) and self.all_in(self.KB[idx], sentence):
                    return
            del_list.reverse()
            for idx in del_list:
                del self.KB[idx]

        ## if the sentence has only one clause, and it exist in KB0, don't insert it
        elif (sentence[0][1], sentence[0][2]) in self.KB0.keys():
            return

        if sentence not in self.KB:
            self.KB.append(sentence)

    ## get clause for difference cases
    def gen_clause(self, x_idx, y_idx, mines_num):
        neig_num = len(self.neighbor[y_idx][x_idx])
        if mines_num == 0:
            for neig in self.neighbor[y_idx][x_idx]:
                self.insert_KB([[False, neig[0], neig[1]]])
        elif neig_num == mines_num:
            for neig in self.neighbor[y_idx][x_idx]:
                self.insert_KB([[True, neig[0], neig[1]]])
        else:
            true_elements = []
            for neig in self.neighbor[y_idx][x_idx]:
                true_elements.append([True, neig[0], neig[1]])

            false_elements = []
            for neig in self.neighbor[y_idx][x_idx]:
                false_elements.append([False, neig[0], neig[1]])

            pos_literals = list(itertools.combinations(true_elements, neig_num-mines_num+1))
            neg_literals = list(itertools.combinations(false_elements, mines_num+1))

            for sen in pos_literals:
                self.insert_KB(list(sen))
            for sen in neg_literals:
                self.insert_KB(list(sen))

    ## initial player's safe cell list
    def init_safe_cell(self, safe_list):
        for safe_cell in safe_list:
            self.KB0[(safe_cell[0], safe_cell[1])] = False
            self.board[safe_cell[1]][safe_cell[0]][0] = True
            self.board[safe_cell[1]][safe_cell[0]][1] = safe_cell[2]

            self.gen_clause(*safe_cell)

    ## get a the sentence index which could do resolution with other sentence
    def get_resolv_pairs(self):
        len_KB = len(self.KB)
        for sen_idx in range(len_KB):
            for sen_idx2 in range(sen_idx+1, len_KB):
                dup, fail = False, False
                for idx in range(len(self.KB[sen_idx])):
                    for idx2 in range(len(self.KB[sen_idx2])):
                        if self.KB[sen_idx][idx][1] == self.KB[sen_idx2][idx2][1] and\
                            self.KB[sen_idx][idx][2] == self.KB[sen_idx2][idx2][2] and\
                            self.KB[sen_idx][idx][0] != self.KB[sen_idx2][idx2][0]:
                            if dup:
                                fail = True
                                break
                            else:
                                dup = True
                                break
                    if fail:
                        break
                if not fail and dup:
                    return sen_idx
        return None

    ## do resolution
    def matching(self):
        sen_idx = self.get_resolv_pairs()
        
        del_list = []
        new_sentence_list = []
        if sen_idx is not None: ## if we have cell which could do resolution
            base_sentence = self.KB[sen_idx]
            del self.KB[sen_idx]
            
            ## iterate every sentence in our KB
            for sen_idx2 in range(len(self.KB)):
                dup_sen_idx1, dup_sen_idx2 = -1, -1
                fail = False
                for idx in range(len(base_sentence)):
                    for idx2 in range(len(self.KB[sen_idx2])):
                        if base_sentence[idx][1] == self.KB[sen_idx2][idx2][1] and\
                            base_sentence[idx][2] == self.KB[sen_idx2][idx2][2] and\
                            base_sentence[idx][0] != self.KB[sen_idx2][idx2][0]:
                            if dup_sen_idx1 != -1:
                                fail = True
                                break
                            else:
                                dup_sen_idx1, dup_sen_idx2 = idx, idx2
                                break
                    if fail:
                        break

                ## doing resolution
                if not fail and dup_sen_idx1 != -1:
                    new_sentence = []
                    for idx in range(len(base_sentence)):
                        if idx != dup_sen_idx1:
                            new_sentence.append(base_sentence[idx])
                    for idx in range(len(self.KB[sen_idx2])):
                        if idx != dup_sen_idx2 and self.KB[sen_idx2][idx] not in new_sentence:
                            new_sentence.append(self.KB[sen_idx2][idx])

                    new_sentence_list.append(new_sentence)
                    del_list.append(sen_idx2)

        ## delete the old sentences
        del_list.reverse()
        self.check_dec_order(del_list)
        for idx in del_list:
            del self.KB[idx]

        ## insert the new sentences
        for sentence in new_sentence_list:
            self.insert_KB(sentence)

    ## check every sentences we delete are in decreasing order
    def check_dec_order(self, seq):
        for i in range(1, len(seq)):
            if seq[i] >= seq[i-1]:
                print(seq)
                raise EnvironmentError("ERROR! order is not decreasing")

    ## use KB0 to update KB
    def update_KB(self):
        del_sen = []
        ## iterate every sentence in KB
        for sen_idx, sen in enumerate(self.KB):
            del_elem = []
            for elem_idx, element in enumerate(sen):
                if (element[1], element[2]) in self.KB0.keys():
                    if (self.KB0[(element[1], element[2])] and element[0])\
                        or (not self.KB0[(element[1], element[2])] and not element[0]):
                        del_sen.append(sen_idx)
                        break
                    else:
                        del_elem.append(elem_idx)
            
            ## delete element which has already exist in KB0
            if del_elem != []:
                del_elem.reverse()
                self.check_dec_order(del_elem)
                for idx in del_elem:
                    del self.KB[sen_idx][idx]

        ## delete sentence which has no longer needed since it always true
        if del_sen != []:
            del_sen.reverse()
            self.check_dec_order(del_sen)
            for idx in del_sen:
                del self.KB[idx]

    ## add global constraint
    def add_global_constraint(self):
        tot_mines, tot_cells = self.mines_num, self.x_size*self.y_size
        true_elements, false_elements = [], []

        ## iterate every cell which hasn't exist KB0
        for y_idx in range(self.y_size):
            for x_idx in range(self.x_size):
                if (x_idx, y_idx) in self.KB0.keys():
                    tot_cells -= 1
                    if self.KB0[(x_idx, y_idx)]:
                        tot_mines -= 1
                else:
                    true_elements.append([True, x_idx, y_idx])
                    false_elements.append([False, x_idx, y_idx])

        ## if there're too many empty cells, break it
        if tot_cells >= 10:
            return

        pos_literals = list(itertools.combinations(true_elements, tot_cells-tot_mines+1))
        neg_literals = list(itertools.combinations(false_elements, tot_mines+1))

        ## add new sentence to KB
        for sen in pos_literals:
            self.insert_KB(list(sen))
        for sen in neg_literals:
            self.insert_KB(list(sen))

    ## process the board
    def process(self, Env):
        prev_KB_len, prev_KB0_len, cnt = -1, -1, 0
        with_global_constraint = False
        success = True
        while len(self.KB):
            ## if the length of KB0 and KB hasn't change for continuous 5 times
            ## add global constraint, or break it
            if prev_KB0_len == len(self.KB0) and prev_KB_len == len(self.KB):
                cnt += 1
                if cnt > 5:
                    if not with_global_constraint:
                        cnt = 0
                        with_global_constraint = True
                        self.add_global_constraint()
                    else:
                        success = False
                        break
            else:
                prev_KB0_len = len(self.KB0)
                prev_KB_len = len(self.KB)
            
            ## sort the KB by the number of length of sentence in increasing order
            self.KB = sorted(self.KB, key=lambda x: len(x))

            ## if the length of first sentence is only 1, expand it
            if len(self.KB[0]) == 1:
                flag, x, y = self.KB[0][0][0], self.KB[0][0][1], self.KB[0][0][2]
                self.KB0[(x, y)] = flag
                self.board[y][x][0] = True

                if not flag: ## if it is not mine
                    mines_cnt = Env.get_sur_mines_num(x, y)
                    self.board[y][x][1] = mines_cnt
                    self.gen_clause(x, y, mines_cnt)
                else:
                    self.board[y][x][1] = -1

                del self.KB[0]  ## delete this sentence
            else:
                ## if the length of sentences are all greater of equal to 2, matching it
                self.matching()
            
            ## update KB since we have new KB0
            self.update_KB()

        return success