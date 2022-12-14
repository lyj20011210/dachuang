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
    # print(flag)
    res = (1 - spatial.distance.cosine(user, video)) / flag
    # print(res)
    return res  # 返回指定用户与指定视频的单个评分值


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
        score = like(uscore, videotag[n][2:])  # 将该用户与该视频的评分矩阵算出来
        d[n][0] = videotag[n][1]
        d[n][1] = score
        n = n + 1
        if n == num:
            break
    return d


def getScoreMatrix():
    userbaseMatrix = user_based_recommend()
    ScoreMatrix = count()  # score-matrix是最终算出来的评分矩阵,后续评分的处理都该放入score-matrix中
    ScoreMatrix = sorted(ScoreMatrix, key=(lambda x: x[1]), reverse=True)

    return ScoreMatrix


# 以下是基于用户的协同过滤算法

# 定义一个全局的data空字典
global data
data={}
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
    data=d
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
        predict = np.mat(np.zeros((m, 2)))
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
            predict[x, 0] = i
            predict[x, 1] = score
            x = x + 1

    return predict