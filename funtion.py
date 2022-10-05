# 此文件为功能函数
from scipy import spatial
import numpy as np
import exts as db


def like(a, b):
    # 求余弦相似度算法
    res = 1 - spatial.distance.cosine(a, b)
    return res


def count(user, video, num):
    a = user[0]  # a是提取出人物的标签信息
    uscore = a[2:]
    n = 0
    c = []
    while True:
        c.append(video[n][1:])
        n = n + 1
        if n == num:
            break
    d = np.zeros((num, 2))  # d用于储存视频标签以及其对应的分数
    n = 1
    print(c)
    for i in c:
        j = like(uscore, i[1:])
        d[n-1][0] = n
        d[n-1][1] = j
        n = n + 1
    # print(d)
    return d
