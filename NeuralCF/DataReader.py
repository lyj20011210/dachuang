import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import random

config = {
    'batch_size': 128,
    'epochs': 10,
    'weight_decay': 1e-6,
    'num_classes': 2,
    'lr': 2e-5,
    'negative_sum': 200
}
# 数据加载
data = pd.read_csv('dataset/giveVideoScore.csv',
                   sep=',',
                   usecols = [2, 3],
                   engine='python')
dataList = data.groupby(by='userid').agg({'videoid': list})
dataList['userid'] = dataList.index
dataList.reset_index(drop=True)
videoids = data.videoid.unique()
movie_nums = len(data['videoid'].unique())

# 负采样
negative = dict()
for userid in dataList['userid']:
    negatives = list()
    while len(negatives) < config['negative_sum']:
        videoid = random.randint(1, 3952)
        if videoid not in dataList.loc[userid].videoid:
            negatives.append(videoid)
    negative[userid] = negatives
negative = pd.DataFrame.from_dict(negative, orient='index')
negative['userid'] = negative.index
negative['videoid'] = negative.apply(lambda x: [x[i] for i in range(config['negative_sum'])], axis=1)
negative = negative[['userid', 'videoid']]
negative = negative.explode('videoid').reset_index(drop=True)
negative['label'] = 0
negative.head()

data = data.explode('videoid').reset_index(drop=True)
data['label'] = 1
data.head()

# 测试集和训练集划分
print(data)
data = pd.concat([data, negative]).astype(np.int32)
x_train, x_test, y_train, y_test = train_test_split(data.iloc[:, 0:2], data.iloc[:, 2], test_size=0.15,
                                                    random_state=2022)
x_test.shape

# 数据配置
from torch.utils.data import DataLoader, Dataset


class MovieDataset(Dataset):
    def __init__(self, x, y):
        super(MovieDataset, self).__init__()
        self.x = x
        self.y = y

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]

    def __len__(self):
        return len(self.x)


import torch

train_dataset = MovieDataset(torch.tensor(x_train.values), torch.tensor(y_train.values))
test_dataset = MovieDataset(torch.tensor(x_test.values), torch.tensor(y_test.values))
train_loader = DataLoader(train_dataset, batch_size=config['batch_size'], shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=config['batch_size'])