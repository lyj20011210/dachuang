import pandas as pd
import torch
import torch.nn as nn



class NeuralCF(nn.Module):
    def __init__(self, userIds, movieIds):
        super(NeuralCF, self).__init__()
        self.userEmb = nn.Embedding(userIds, 64)
        self.movieEmb = nn.Embedding(movieIds, 64)
        self.sequential = nn.Sequential(
            nn.Linear(128, 96),
            nn.ReLU(),
            nn.Linear(96, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        left = torch.LongTensor(x[:, 0].numpy())
        right = torch.LongTensor(x[:, 1].numpy())
        left = self.userEmb(left)
        right = self.movieEmb(right)
        x = torch.cat([left, right], dim=1)
        x = self.sequential(x)
        x = torch.squeeze(x)
        return x


from sklearn.metrics import accuracy_score


# 定义损失函数
def criterion(outputs, labels):
    return nn.BCELoss()(outputs, labels)


# 计算准确率
def getAccuracy(outputs, labels):
    output = list()
    for i in outputs:
        if i < 0.5:
            output.append(0)
        else:
            output.append(1)
    return accuracy_score(labels, output)


# 训练
from tqdm.auto import tqdm
import gc


def train_one_epoch(epoch, model, dataLoader, optimizer):
    model.train()
    steps = len(dataLoader)
    bar = tqdm(enumerate(dataLoader), total=len(dataLoader))
    dataset_size = 0
    running_loss = 0
    for step, (x, y) in bar:
        batch_size = x.shape[0]
        outputs = model(x)
        y = torch.FloatTensor(y.numpy())
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        running_loss += (loss.item() * batch_size)
        dataset_size += batch_size
        epoch_loss = running_loss / dataset_size

        bar.set_description(f'Epoch: [{epoch}/{10}]')
        bar.set_postfix(Epoch=epoch, Train_loss=epoch_loss)
    gc.collect()
    return running_loss


# 准确率验证
def valid_one_epoch(epoch, model, dataLoader):
    model.eval()
    bar = tqdm(enumerate(dataLoader), total=len(dataLoader))
    total_accuracy = 0
    item = 0
    for step, (x, y) in bar:
        item += 1
        batch_size = x.shape[0]
        outputs = model(x)
        total_accuracy += getAccuracy(outputs, y)
        bar.set_description(f'Epoch: [{epoch}/{10}]')
        bar.set_postfix(Epoch=epoch, Accuracy=total_accuracy / item)
    gc.collect()
    return total_accuracy


# if __name__ == '__main__':
#     # 6041和3953分别为用户id数和电影id数
#     model = NeuralCF(6041, 3953)
#     optimizer = torch.optim.Adam(model.parameters(), lr=config['lr'], weight_decay=config['weight_decay'])
#     for epoch in range(1, config['epochs'] + 1):
#         train_one_epoch(epoch, model, train_loader, optimizer)
#         valid_one_epoch(epoch, model, test_loader)
#     torch.save(model.state_dict(), "./models/test.pt")
