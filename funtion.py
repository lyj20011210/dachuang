# 此文件为功能函数
import datetime

import scipy.sparse
from flask import session
from scipy import spatial
import numpy as np
from exts import db


# 此函数用于取特定标签的视频
def selectVideoWithLabel(label: str):
    s = "select * from video_list where video_tag like '" + label + "'"
    # print(s)
    video = db.session.execute(s)
    return video


def like(user, video, num):
    # 求余弦相似度算法
    # user = scipy.sparse.csr_matrix(user)
    # video = scipy.sparse.csr_matrix(video)
    # sql = "select count(*) from label"
    # num = db.session.execute(sql)
    # num = int(list(num)[0][0])
    # print(num)
    video = list(video)
    flag = 1
    # print(num)
    for i in range(num):
        if video[i] == 1 and user[i] == 1:
            flag = flag + 1
    # print(flag)
    res = (1 - spatial.distance.cosine(user, video)) / flag
    # print(res)
    return res  # 返回指定用户与指定视频的单个评分值


def count():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("start count" + time)
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
    # print(uscore)
    n = 0
    d = np.zeros((num, 2))  # d用于储存视频标签以及其对应的分数
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("check1" + time)
    sql = "select count(*) from label"
    num1 = db.session.execute(sql)
    num1 = int(list(num1)[0][0])
    # print(num1)
    while True:
        score = like(uscore, videotag[n][2:], num1)  # 将该用户与该视频的评分矩阵算出来
        d[n][0] = videotag[n][1]
        d[n][1] = score
        n = n + 1
        if n == num:
            break
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("end count" + time)
    return d


# 为了优化首页的访问速度，我新建了一个表格，用于存储用户的视频评分矩阵,发现不需要这个表
# def putScoreMatrixintoDatabase():
#     time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     print("start put" + time)
#     name = session.get("name")
#     ScoreMatrix = count()
#     ScoreMatrix = sorted(ScoreMatrix, key=(lambda x: x[1]), reverse=True)
#     for i in ScoreMatrix:
#         sql = "INSERT INTO ScoreMatrix (name, videoid, score) VALUES ('" + name + "', '" + str(
#             int(i[0])) + "', '" + str(i[1]) + "') ON DUPLICATE KEY UPDATE score = '" + str(i[1]) + "';"
#         # print(sql)
#         db.session.execute(sql)
#         db.session.commit()
#     time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     print("end put" + time)


def getScoreMatrix():
    userbaseMatrix = user_based_recommend()
    print(userbaseMatrix)
    sql = "select videoid,score from ScoreMatrix where name='" + session.get("name") + "'"
    M = count()
    # M = list(db.session.execute(sql))
    # M = np.array(M)
    # print("M")
    # print(M)
    M = sorted(M, key=(lambda x: x[0]), reverse=False)
    if all(x[1] == M[0][1] for x in M):
        M = [[x[0], 0] for x in M]

    if type(userbaseMatrix) != int:
        for i in userbaseMatrix:
            num = int(i[0])
            # print(num)
            M[num][1] = M[num][1] + i[1] / 100
    # ScoreMatrix=count()

    ScoreMatrix = sorted(M, key=(lambda x: x[1]), reverse=True)
    # print("ScoreMatrix:")
    # print(ScoreMatrix)
    return ScoreMatrix


# 以下是基于用户的协同过滤算法

# 定义一个全局的data空字典
global data
data = {}
# 定义一个全局的w相似度矩阵
w = []


def data_deal():
    sql = "select user,videoid,score from giveVideoScore"
    arr = db.session.execute(sql)
    arr = list(arr)
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

    global data
    data = d
    return d


def cos_sim(x, y):
    '''余弦相似性
    input:  x:传递一个字典的key
            y:传递另一个字典的key
    output: x和y之间的余弦相似度
    '''
    # data是处理好二维矩阵的字典

    # vec1、2用来储存x和y共同有的视频的评分
    vec1 = []
    vec2 = []

    min_data = data.get(x)
    max_data = data.get(y)
    # 将较短的字典赋值给min，较长的赋值给max
    if len(min_data) > len(max_data):
        tmp = min_data
        min_data = max_data
        max_data = tmp

    for i in min_data:
        if (i in max_data):
            vec1.append(max_data.get(i))
            vec2.append(min_data.get(i))

    cos_sim1 = 1 - spatial.distance.cosine(vec1, vec2)
    return cos_sim1


def similarity():
    # data是处理好二维矩阵的字典

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


def user_based_recommend():
    '''基于用户相似性为用户user推荐商品
    input:  data(dic):用户视频打分的字典
            w(mat):用户之间的相似度矩阵
            user_id(int):用户的编号
    output: predict(list):推荐列表
    '''
    data_deal()
    w = similarity()
    # lt存储所有用户的id
    lt = list(data.keys())
    user_id = session.get("name")
    # d存储目标用户的字典数据
    if user_id not in lt:
        return 0
    d = data.get(user_id).keys()
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
                if ((j not in d) and (di.get(j) > 6)):
                    not_inter.append(j)

        not_inter = list(set(not_inter))

        # 2、利用user数组、not_inter数组、lt列表+w相似矩阵计算目标用户评分矩阵
        m = len(not_inter)
        x = 0
        predict = np.zeros((m, 2))
        for i in not_inter:
            count = 0
            score = 0
            for j in user:
                video = (data.get(j)).keys()
                lt1 = data.get(j)
                if i in video:
                    count = count + 1
                    score = score + lt1.get(i) * w[s, lt.index(j)]
            score = score / count
            predict[x][0] = i
            predict[x][1] = score
            x = x + 1

    return predict
