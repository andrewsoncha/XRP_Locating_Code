import matplotlib.pyplot as plt
import numpy as np
from math import radians, cos, sin

def plotCartesian(ax, cartesianList, color='b'):
    ax.scatter([pair[0] for pair in cartesianList], [pair[1] for pair in cartesianList], color=color)

def polarToCartesian(polarCoor):
    angle = polarCoor[0]
    pos = polarCoor[1]
    dist = polarCoor[2]
    return (pos[0] + dist*cos(angle), pos[1] + dist*sin(angle))

class Hough:
    def __init__(self, maxR, rN = 20, angleN = 50):
        self.angleN = angleN
        self.rN = rN
        self.maxR = maxR
        self.angleList = np.linspace(-np.pi/2, np.pi, num=angleN)
        self.accumulator = [[0 for _ in range(rN)] for _ in range(angleN)]
        print(len(self.accumulator), len(self.accumulator[0]))

    def roundR(self, r):
        return self.rN//2 + int(r * self.rN//2 / maxR)

    def vote(self, x, y):
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(x, y)
        for angleI in range(self.angleN):
            angle = self.angleList[angleI]
            result_rI = self.roundR(r * np.cos(angle - theta))
            self.accumulator[angleI][result_rI] = self.accumulator[angleI][result_rI] + 1

    def getLineParameters(self, thresh=5):
        return [(self.angleList[i], (j/self.rN*self.maxR), self.accumulator[i][j]) for i in range(self.angleN) for j in range(self.rN) if self.accumulator[i][j]>=thresh]

if __name__ == '__main__':
    angleList = []
    posList = []
    distList = []
    with open('../testData/spinValuesMove1', 'r') as file:
        for line in file:
            words = line.split()
            angleVal = radians(float(words[0]))

            # (%d, %d)
            firstPosWord = words[1]
            firstPos = int(firstPosWord[1:len(firstPosWord)-1])
            secondPosWord = words[2]
            secondPos = int(secondPosWord[0:len(secondPosWord)-1])
            posVal = (firstPos, secondPos)

            #DistanceVal: %lf
            distVal = float(words[3])
            if distVal > 400:
                continue
            print(f'{angleVal} {posVal} {distVal}')
            angleList.append(angleVal)
            posList.append(posVal)
            distList.append(distVal)

    cartesianList1 = [polarToCartesian(pair) for pair in zip(angleList, posList, distList) if pair[1]==(0,0)]
    cartesianList2 = [polarToCartesian(pair) for pair in zip(angleList, posList, distList) if pair[1]==(5,0)]
    cartesianList = [polarToCartesian(pair) for pair in zip(angleList, posList, distList)]
    maxR = max([np.sqrt(x**2+y**2) for (x, y) in cartesianList])
    print('maxR: ', maxR)
    hough = Hough(maxR)
    for (x, y) in cartesianList:
        hough.vote(x, y)
    lines = hough.getLineParameters(20)

    fig = plt.figure()
    ax = fig.add_subplot()
    plotCartesian(ax, cartesianList1, color='b')
    plotCartesian(ax, cartesianList2, color='red')

    for (i_theta, i_rho, _) in lines:
            theta = i_theta
            a = np.cos(theta)
            b = np.sin(theta)

            rho = i_rho 
            print('theta: ', theta, 'rho: ', rho)

            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 50 * (-b))
            y1 = int(y0 + 50 * (a))
            x2 = int(x0 - 50 * (-b))
            y2 = int(y0 - 50 * (a))

            xList = np.linspace(x1, x2, num=100)
            yList = np.linspace(y1, y2, num=100)
            ax.plot(xList, yList)

    plt.show()
    #plotPolar(angleList, distList)

