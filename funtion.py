# 此文件为功能函数
from flask import session
from scipy import spatial
import numpy as np
from exts import db



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
        d[n - 1][0] = n
        d[n - 1][1] = j
        n = n + 1
    # print(d)
    return d


def getScoreMatrix():
    sql = "select * from user_interest where user_name= '" + session.get("name") + "'"
    usertag = db.session.execute(sql)
    usertag = list(usertag)
    sql = "select * from videos_interest"
    videotag = db.session.execute(sql)
    videotag = list(videotag)
    num = db.session.execute("select count(*) from videos_interest")
    num = list(num)
    num = num[0][0]
    ScoreMatrix = count(usertag, videotag, num)
    n = 0
    while True:
        if n == num:
            break
        m = 0
        while True:
            if m + 1 == num:
                break
            if ScoreMatrix[m][1] < ScoreMatrix[m + 1][1]:
                temp = np.zeros(2)
                temp[0] = ScoreMatrix[m][0]
                temp[1] = ScoreMatrix[m][1]
                ScoreMatrix[m] = ScoreMatrix[m + 1]
                ScoreMatrix[m + 1] = [temp[0], temp[1]]
            m = m + 1
        n = n + 1
    return ScoreMatrix
