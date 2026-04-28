import matplotlib.pyplot as plt
import numpy as np
from math import radians, cos, sin, sqrt
from scipy.spatial import ConvexHull
from sklearn.cluster import DBSCAN, HDBSCAN, AgglomerativeClustering
from sklearn import linear_model

def plotCartesian(ax, cartesianList, color='b'):
    ax.scatter([pair[0] for pair in cartesianList], [pair[1] for pair in cartesianList], color=color)

def polarToCartesian(polarCoor):
    angle = polarCoor[0]
    pos = polarCoor[1]
    dist = polarCoor[2]
    return (pos[0] + dist*cos(angle), pos[1] + dist*sin(angle))

def plot(X, labels, probabilities=None, parameters=None, ground_truth=False, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 4))
    labels = labels if labels is not None else np.ones(X.shape[0])
    probabilities = probabilities if probabilities is not None else np.ones(X.shape[0])
    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    # The probability of a point belonging to its labeled cluster determines
    # the size of its marker
    proba_map = {idx: probabilities[idx] for idx in range(len(labels))}
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_index = (labels == k).nonzero()[0]
        for ci in class_index:
            ax.plot(
                X[ci, 0],
                X[ci, 1],
                "x" if k == -1 else "o",
                markerfacecolor=tuple(col),
                markeredgecolor="k",
                markersize=4 if k == -1 else 1 + 5 * proba_map[ci],
            )
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    preamble = "True" if ground_truth else "Estimated"
    title = f"{preamble} number of clusters: {n_clusters_}"
    if parameters is not None:
        parameters_str = ", ".join(f"{k}={v}" for k, v in parameters.items())
        title += f" | {parameters_str}"
    ax.set_title(title)
    plt.tight_layout()

class Hough:
    def __init__(self, maxR, rN = 60, angleN = 50):
        self.angleN = angleN
        self.rN = rN
        self.maxR = maxR
        self.angleList = np.linspace(-np.pi/2, np.pi, num=angleN)
        self.accumulator = [[0 for _ in range(rN)] for _ in range(angleN)]
        # print(len(self.accumulator), len(self.accumulator[0]))

    def roundR(self, r):
        # print(f'roundR({r})')
        # print(f'roundR results: {int(r * (self.rN-1) / maxR)}')
        #return self.rN//2 + int(r * self.rN//2 / maxR)
        return self.rN //2 + int(r * (self.rN//2) / self.maxR)

    def vote(self, x, y):
        r = np.sqrt(x**2 + y**2)
        for angleI in range(self.angleN):
            angle = self.angleList[angleI]
            # result_rI = self.roundR(r * np.cos(angle - theta))
            result_rI = self.roundR(x*np.cos(angle) + y*np.sin(angle))
            # print(f'angle: {angle}   result_rI: {result_rI}')
            self.accumulator[angleI][result_rI] += 1
        print()

    def getLineParameters(self, thresh=5):
        print([(self.angleList[i], (j/self.rN*self.maxR), self.accumulator[i][j]) for i in range(self.angleN) for j in range(self.rN) if self.accumulator[i][j]>=thresh])

        return [(self.angleList[i], ((j-self.rN//2) * self.maxR/(self.rN//2)), self.accumulator[i][j]) for i in range(self.angleN) for j in range(self.rN) if self.accumulator[i][j]>=thresh]

if __name__ == '__main__':
    angleList = []
    posList = []
    distList = []
    with open('../testData/3dPrintRoom', 'r') as file:
        for line in file:
            # "Yaw: {current_yaw:.2f}, Range Distance: {rangeDist:.1f} cm, Robot Position: ({robot_x},{robot_y})" 
            print('line: ', line)
            words = line.split()
            angleVal = radians(float(words[0]))

            # (%d, %d)
            firstPosWord = words[1]
            firstPos = float(firstPosWord[1:len(firstPosWord)-1])
            secondPosWord = words[2]
            secondPos = float(secondPosWord[0:len(secondPosWord)-1])
            posVal = (firstPos, secondPos)

            #DistanceVal: %lf
            distVal = float(words[3])
            if distVal > 400:
                continue
            print(f'{angleVal} {posVal} {distVal}')
            angleList.append(angleVal)
            posList.append(posVal)
            distList.append(distVal)

    '''
    cartesianList1 = [polarToCartesian(pair) for pair in zip(angleList, posList, distList) if pair[1]==(0,0)]
    cartesianList2 = [polarToCartesian(pair) for pair in zip(angleList, posList, distList) if pair[1]!=(0,0)]
    '''
    cartesianList = [polarToCartesian(pair) for pair in zip(angleList, posList, distList)]

    #Remove points too far from origin point
    cartesianList = [(x, y) for (x, y) in cartesianList if np.sqrt(x**2+y**2) < 800]
    cartesianList = np.array(cartesianList)/10
    maxR = max([np.sqrt(x**2+y**2) for (x, y) in cartesianList])

    # Filter clustered Points
    pointN = len(cartesianList)

    #dbs = HDBSCAN(min_cluster_size = 3)
    #dbs.fit(cartesianList)
    clustering = AgglomerativeClustering(linkage='ward', n_clusters=14)
  
    fig = plt.figure()
    ax = fig.add_subplot()

    # plot(cartesianList, dbs.labels_, ax=ax)
    # plot(cartesianList, clustering.labels_, ax=ax)
    labels = clustering.fit_predict(cartesianList)

    for label in set(labels):
        print(label)
        idxs = [idx for idx in range(len(labels)) if labels[idx]==label]
        x_list = np.array(cartesianList[idxs, 0]).reshape(-1, 1)
        y_list = np.array(cartesianList[idxs, 1]).reshape(-1, 1)
        print('c: ', np.random.rand(3))
        ax.scatter(x_list, y_list, c=np.random.rand(3))
        regr = linear_model.LinearRegression()
        print('x_list: ', x_list)
        print('y_list: ', y_list)
        regr.fit(x_list, y_list)
        pred = regr.predict(x_list)
        ax.plot(x_list, pred, color="black", linewidth=3)

    plt.show()
