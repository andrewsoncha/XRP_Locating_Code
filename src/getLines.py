import matplotlib.pyplot as plt
import numpy as np
from math import radians, cos, sin
from scipy.spatial import ConvexHull
import sys

def plotCartesian(ax, cartesianList, color='b'):
    ax.scatter([pair[0] for pair in cartesianList], [pair[1] for pair in cartesianList], color=color)

def polarToCartesian(polarCoor):
    angle = polarCoor[0]
    pos = polarCoor[1]
    dist = polarCoor[2]
    return (pos[0] + dist*cos(angle), pos[1] + dist*sin(angle))

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
    file_path = sys.argv[1]
    print('opening file_path: ', file_path)
    with open(file_path, 'r') as file:
        for line in file:
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
    cartesianList = [(x*10, y*10) for (x, y) in cartesianList]
    maxR = max([np.sqrt(x**2+y**2) for (x, y) in cartesianList])

    # Filter clustered Points
    filteredPoints = set(cartesianList)
    pointN = len(cartesianList)
    for i in range(pointN):
        for j in range(i+1, pointN):
            pointI = cartesianList[i]
            pointJ = cartesianList[j]
            dist = ((pointI[0]-pointJ[0])**2 + (pointI[1]-pointJ[1])**2)**0.5
            print('pointI: ', pointI, '   pointJ: ', pointJ, '      dist: ', dist)
            if dist < 200:
                filteredPoints.discard(cartesianList[j])
                print('discarded!', cartesianList[j])
    cartesianList = list(filteredPoints)

    hull = ConvexHull(cartesianList)

    for simplex in hull.simplices:
        plt.plot(cartesianList[simplex, 0], cartesianList[simplex, 1], 'k-')
    
    '''
    print('maxR: ', maxR)
    hough = Hough(maxR)
    for (x, y) in cartesianList:
        hough.vote(x, y)
    plt.imshow(hough.accumulator)
    lines = hough.getLineParameters(12)
    '''

    fig = plt.figure()
    ax = fig.add_subplot()
    # plotCartesian(ax, cartesianList1, color='b')
    # plotCartesian(ax, cartesianList2, color='red')

    plotCartesian(ax, cartesianList, color='b')

    '''
    LINE_LENGTH = 4800

    for (i_theta, i_rho, _) in lines:
            theta = i_theta
            a = np.cos(theta)
            b = np.sin(theta)

            rho = i_rho 
            print('theta: ', theta, 'rho: ', rho)
            print('a: ', a, '   b: ', b)

            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + LINE_LENGTH * (-b))
            y1 = int(y0 + LINE_LENGTH * (a))
            x2 = int(x0 - LINE_LENGTH * (-b))
            y2 = int(y0 - LINE_LENGTH * (a))

            xList = np.linspace(x1, x2, num=100)
            yList = np.linspace(y1, y2, num=100)
            ax.plot(xList, yList)
            # ax.plot(yList, xList)
    '''

    plt.show()
    #plotPolar(angleList, distList)

