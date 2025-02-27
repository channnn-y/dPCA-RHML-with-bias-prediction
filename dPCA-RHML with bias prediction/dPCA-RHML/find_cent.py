
# 寻找真实聚类中心
import numpy as np

def cal_pairwise_dist(x):
    '''
    计算距离
    '''
    sum_x = np.sum(np.square(x), 1)
    dist = np.add(np.add(-2 * np.dot(x, x.T), sum_x).T, sum_x)
    return dist



def find_c(cent,data):
    nears = [] # 与聚类中心最近的点的编号
    for j in range(len(cent)):

        dis = cal_pairwise_dist(np.array([data[0],cent[j]]))[0][1]
        near_i=0
        for i in range(len(data)):
            dist = cal_pairwise_dist(np.array([data[i],cent[j]]))[0][1]
            if dist<dis:
                near_i = i
                dis = dist
        nears.append(near_i)

    centers = []
    for i in nears:
        centers.append(data[i])
    centers = np.array(centers)
    return centers



