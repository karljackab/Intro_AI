import model
import pandas as pd
import numpy as np
from tqdm import tqdm

#############################
tree_num = 30
max_feature = None
max_depth = 2
boostrap = True
criterion = 'gini'

experiment_num = 1
data = 'ionosphere'   ## iris wine ionosphere
#############################

def read_data(data='iris'):
    return pd.read_csv(f'{data}.csv')

print('=====================================')
print(f'Data {data}')
print(f'tree_num {tree_num}')
print(f'max_feature {max_feature}')
print(f'max_depth {max_depth}')
print(f'boostrap {boostrap}')
print(f'criterion {criterion}')
print(f'experiment_num {experiment_num}')
print('=====================================')
data = read_data(data)

avg_acc = 0.
for _ in tqdm(range(experiment_num)):
    msk = np.random.rand(len(data)) < 0.8
    train_data, test_data = data[msk], data[~msk]
    random_forest = model.RandomForest(tree_num, max_feature, boostrap, criterion, max_depth)
    random_forest.fit(train_data)
    acc = random_forest.score(test_data)
    # print(f'Accuracy: {acc}')
    avg_acc += acc
print(f'Average accuracy: {avg_acc/experiment_num}')