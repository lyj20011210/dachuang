# 此文件为功能函数
from flask import session
from scipy import spatial
import numpy as np
from exts import db


def like(user, video):
    # 求余弦相似度算法
    sql = "select count(*) from label"
    num = db.session.execute(sql)
    num = int(list(num)[0][0])
    video = list(video)
    flag = 1
    for i in range(num):
        if video[i] == 1 and user[i] == 1:
            flag = flag + 1
    # for i in range(num):
    #     video[i] = video[i] * (video[i] / flag)
    print(flag)
    res = (1 - spatial.distance.cosine(user, video)) / flag
    print(res)
    return res


def count():
    sql = "select * from user_interest where user_name= '" + session.get("name") + "'"
    usertag = db.session.execute(sql)
    usertag = list(usertag)
    sql = "select * from videos_interest"
    videotag = db.session.execute(sql)
    videotag = list(videotag)
    num = db.session.execute("select count(*) from videos_interest")
    num = list(num)
    num = num[0][0]

    a = usertag[0]  # a是提取出人物的标签信息
    uscore = a[2:]  # 得到人物标签矩阵
    n = 0
    d = np.zeros((num, 2))  # d用于储存视频标签以及其对应的分数
    while True:
        score = like(uscore, videotag[n][2:])
        d[n][0] = videotag[n][1]
        d[n][1] = score
        n = n + 1
        if n == num:
            break
    # print(d)
    return d
    # while True:
    #     c.append(video[n][1:])
    #     n = n + 1
    #     if n == num:
    #         break
    # d = np.zeros((num, 2))  # d用于储存视频标签以及其对应的分数
    # n = 1
    # print(c)
    # for i in c:
    #     j = like(uscore, i[1:])
    #     d[n - 1][0] = n
    #     d[n - 1][1] = j
    #     n = n + 1
    # # print(d)
    # return d


def getScoreMatrix():
    # num = db.session.execute("select count(*) from videos_interest")#是全部视频的数量
    ScoreMatrix = count()  # score-matrix是最终算出来的评分矩阵,后续评分的处理都该放入score-matrix中
    ScoreMatrix = sorted(ScoreMatrix, key=(lambda x: x[1]), reverse=True)
    print(ScoreMatrix)
    print("ScoreMatrix")
    print(ScoreMatrix)
    # n = 0
    # while True:#通过
    #     if n == num:
    #         break
    #     m = 0
    #     while True:
    #         if m + 1 == num:
    #             break
    #         if ScoreMatrix[m][1] < ScoreMatrix[m + 1][1]:  # 对评分矩阵进行排序
    #             temp = np.zeros(2)
    #             temp[0] = ScoreMatrix[m][0]
    #             temp[1] = ScoreMatrix[m][1]
    #             ScoreMatrix[m] = ScoreMatrix[m + 1]
    #             ScoreMatrix[m + 1] = [temp[0], temp[1]]
    #         m = m + 1
    #     n = n + 1
    return ScoreMatrix


# 以下是基于用户的协同过滤算法

def data_deal(data):
    '''
    input: a=[[111,201,4],
       [111,202,3],
       [111,203,4]]
    output: a={'111':{'201':4,'202':3,'203':4}}
    '''
    d = {}
    for i in arr:
        d[i[0]] = {}

    for i in arr:
        d[i[0]][i[1]] = i[2]

    return d


def cos_sim(x, y):
    '''余弦相似性
    input:  x:传递一个字典的key
            y:传递另一个字典的key
    output: x和y之间的余弦相似度
    '''
    # vec1、2用来储存x和y共同有的视频的评分
    vec1 = []
    vec2 = []

    min = data.get(x)
    max = data.get(y)
    # 将较短的字典赋值给min，较长的赋值给max
    if (len(min) > len(max)):
        tmp = min
        min = max
        max = tmp

    for i in min:
        if (i in max):
            vec1.append(max.get(i))
            vec2.append(min.get(i))

    cos_sim1 = 1 - spatial.distance.cosine(vec1, vec2)
    return cos_sim1


def similarity(data):
    '''计算矩阵中任意两行之间的相似度
    input:  data(mat):任意矩阵
    output: w(mat):任意两行之间的相似度
    '''
    m = len(data)
    w = np.mat(np.zeros((m, m)))
    lt = list(data.keys())

    for i in range(len(lt)):
        for j in range(i + 1, len(lt)):
            w[i, j] = cos_sim(lt[i], lt[j])
            w[j, i] = w[i, j]

    return w


def user_based_recommend(user_id):
    '''基于用户相似性为用户user推荐商品
    input:  data(dic):用户视频打分的字典
            w(mat):用户之间的相似度矩阵
            user_id(int):用户的编号
    output: predict(list):推荐列表
    '''
    # d存储目标用户的字典数据
    d = data.get(user_id).keys()
    # lt存储所有用户的id
    lt = list(data.keys())
    # s表示用户所处位置
    if lt.count(user_id):
        s = lt.index(user_id)
    # user数组用来存储相似度高的用户位置
    user = []
    for i in range(len(w)):
        if (w[s, i] > 0.7):
            user.append(lt[i]);

    # 1、找到用户user_id没有互动过的视频，对没有互动过的视频进行选取，大于3分才推荐
    not_inter = []
    for i in user:
        di = data.get(i)
        video = di.keys()
        for j in video:
            if ((j not in d) and (di.get(j) > 3)):
                not_inter.append(j)

    return list(set(not_inter))


def top_k(predict, k):
    '''为用户推荐前k个商品
    input:  predict(list):排好序的商品列表
            k(int):推荐的商品个数
    output: top_recom(list):top_k个商品
    '''
    top_recom = []
    len_result = len(predict)
    if k >= len_result:
        top_recom = predict
    else:
        for i in range(k):
            top_recom.append(predict[i])
    return top_recom
