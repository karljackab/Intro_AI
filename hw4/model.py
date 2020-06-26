import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from collections import Counter
import matplotlib.pyplot as plt
import random
import utils

class DecisionTree():
    def __init__(self, criterion='gini', max_depth=None, max_features=None):
        if criterion != 'gini' and criterion != 'entropy':
            raise Exception('DecisionTree key error: criterion myst be "gini" \
                            or "entropy"')

        self.criterion = criterion
        self.max_depth = max_depth
        self.tree = []  # each element would be
                        # [split_feature, split_value, larger_goto_idx, 
                        #  others_goto_idx, category]
        self.max_features = max_features
        if self.max_features is not None:
            self.max_features = int(self.max_features)

    def check_terminate(self, y):
        first = None
        for i in y:
            if first is None:
                first = i
            elif first != i:
                return False
        return True

    def fit(self, x, y):
        if type(y) == pd.core.frame.DataFrame:
            y = y['0']

        self.tree.append([])
        self.split(x, y, 1, 0)

    def pickup_feature_names(self, keys):
        if self.max_features is None or len(keys) < self.max_features:
            return keys
        else:
            return random.sample(list(keys.to_numpy()), self.max_features)

    def split(self, x, y, depth, tree_idx):
        if (self.max_depth is not None and depth > self.max_depth) or self.check_terminate(y.to_numpy()):
            cnt = Counter(y.to_numpy())
            self.tree[tree_idx] = \
                [None, None, None, None, cnt.most_common(1)[0][0]]
            return

        while True:
            feature_names = self.pickup_feature_names(x.keys())

            best_split_feature = None
            best_split_value = None
            best_criteria = None

            for feature_name in feature_names:
                feature = x[feature_name].sort_values().to_numpy()
                for idx in range(1, len(feature)):
                    split_value = (feature[idx-1]+feature[idx])/2
                    larger_y, others_y = y[x[feature_name] > split_value], y[x[feature_name] <= split_value]
                    larger_n, others_n = len(larger_y), len(others_y)
                    if self.criterion == 'gini':
                        new_gini = larger_n*utils.gini(larger_y.to_numpy()) + others_n*utils.gini(others_y.to_numpy())
                        new_gini /= (larger_n+others_n)
                        if best_criteria is None or new_gini < best_criteria:
                            best_criteria = new_gini
                            best_split_feature = feature_name
                            best_split_value = split_value
                    elif self.criterion == 'entropy':
                        after_entropy = larger_n*utils.entropy(larger_y.to_numpy()) + others_n*utils.entropy(others_y.to_numpy())
                        after_entropy /= (larger_n+others_n)
                        if best_criteria is None or after_entropy < best_criteria:
                            best_criteria = after_entropy
                            best_split_feature = feature_name
                            best_split_value = split_value

            larger_y, others_y = y[x[best_split_feature] > best_split_value], y[x[best_split_feature] <= best_split_value]
            larger_n, others_n = len(larger_y), len(others_y)
            if self.criterion == 'gini':
                init_criteria = utils.gini(y.to_numpy())
                new_gini = larger_n*utils.gini(larger_y.to_numpy()) + others_n*utils.gini(others_y.to_numpy())
                new_gini /= (larger_n+others_n)
            elif self.criterion == 'entropy':
                init_criteria = utils.entropy(y.to_numpy())
                after_entropy = larger_n*utils.entropy(larger_y.to_numpy()) + others_n*utils.entropy(others_y.to_numpy())
                after_entropy /= (larger_n+others_n)
            
            if (x[best_split_feature] > best_split_value).sum() == 0 or \
                    (x[best_split_feature] <= best_split_value).sum() == 0:
                continue
            else:
                break

        greater_idx = len(self.tree)
        others_idx = greater_idx+1
        self.tree[tree_idx] = [best_split_feature, best_split_value, greater_idx, others_idx, None]
        self.tree.append([])
        self.tree.append([])
        self.split(x[x[best_split_feature] > best_split_value], larger_y, depth+1, greater_idx)
        self.split(x[x[best_split_feature] <= best_split_value], others_y, depth+1, others_idx)

    def predict_single(self, x):
        # self.tree: [split_feature, split_value, larger_goto_idx, others_goto_idx, category]
        cur_tree_idx = 0
        while self.tree[cur_tree_idx][4] is None:
            if x[self.tree[cur_tree_idx][0]] > self.tree[cur_tree_idx][1]:
                cur_tree_idx = self.tree[cur_tree_idx][2]
            else:
                cur_tree_idx = self.tree[cur_tree_idx][3]
        return self.tree[cur_tree_idx][4]

    def predict(self, x):
        pred_y = []
        for _, row in x.iterrows():
            pred_y.append(self.predict_single(row))
        return pred_y

    def score(self, x, y, return_pred_y=False):
        pred_y = self.predict(x)
        tot_n, acc_n = len(pred_y), 0
        y = y.to_numpy()
        for i in range(tot_n):
            if y[i] == pred_y[i]:
                acc_n += 1
        if return_pred_y:
            return acc_n/tot_n, pred_y
        else:
            return acc_n/tot_n

class RandomForest():
    def __init__(self, n_estimators, max_features, boostrap=True, criterion='gini', max_depth=None):
        self.n_tree = n_estimators
        self.boostrap = boostrap
        self.trees = []
        for _ in range(n_estimators):
            self.trees.append(DecisionTree(criterion=criterion, max_depth=max_depth, max_features=max_features))

    def fit(self, base_x):
        for tree_idx in range(self.n_tree):
            if self.boostrap:
                new_x = base_x.sample(n=len(base_x), replace=True)
            else:
                new_x = base_x
            new_y = new_x['y']
            new_x = new_x.loc[:, new_x.columns != 'y']

            self.trees[tree_idx].fit(new_x, new_y)

    def predict(self, x):
        res = None
        for i in range(self.n_tree):
            pred = self.trees[i].predict(x)
            pred = np.array(pred).reshape(-1, 1)
            if res is None:
                res = pred
            else:
                res = np.concatenate((res, pred), axis=1)
        return [Counter(res[i]).most_common(1)[0][0] for i in range(len(x))]

    def score(self, data, return_pred_y=False):
        y = data['y']
        x = data.loc[:, data.columns != 'y']
        pred_y = self.predict(x)
        tot_n, acc_n = len(pred_y), 0
        y = y.to_numpy()
        for i in range(tot_n):
            if y[i] == pred_y[i]:
                acc_n += 1
        if return_pred_y:
            return acc_n/tot_n, pred_y
        else:
            return acc_n/tot_n
