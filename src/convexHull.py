import matplotlib.pyplot as plt
import numpy as np
from math import radians, cos, sin, sqrt
from scipy.spatial import ConvexHull

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
    with open('../testData/3dPrintRoom', 'r') as file:
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
    cartesianList = [(x, y) for (x, y) in cartesianList]
    maxR = max([np.sqrt(x**2+y**2) for (x, y) in cartesianList])

    # Filter clustered Points
    pointN = len(cartesianList)
    pointAndDist = dict(zip(range(pointN), [maxR]*pointN))
    for i in range(pointN):
        for j in range(pointN):
            if i == j:
                continue
            pointI = cartesianList[i]
            pointJ = cartesianList[j]
            dist = sqrt((pointI[0]-pointJ[0])**2 + (pointI[1]-pointJ[1])**2)
            # if pointI not in pointAndDist:
            #    print('i: ', i, 'pointI: ', pointI, '      dist: ', dist)
            #    pointAndDist[i] = dist
            if pointAndDist[i] > dist:
                print('i: ', i, 'pointI: ', pointI, '      dist: ', dist)
                pointAndDist[i] = dist
                
            # if pointJ not in pointAndDist:
            #     print('j: ', j, 'pointJ: ', pointJ, '      dist: ', dist)
            #     pointAndDist[j] = dist
            if pointAndDist[j] > dist:
                print('j: ', j, 'pointJ: ', pointJ, '      dist: ', dist)
                pointAndDist[j] = dist

    print(pointAndDist)

    filteredPoints = [cartesianList[i] for i in range(pointN) if pointAndDist[i] < 15]

    hull = ConvexHull(filteredPoints)
   
    fig = plt.figure()
    ax = fig.add_subplot()

    plotCartesian(ax, cartesianList, color='r')
    # plotCartesian(ax, cartesianList1, color='yellow')
    # plotCartesian(ax, cartesianList2, color='green')
    plotCartesian(ax, filteredPoints, color='b')

    for simplex in hull.simplices:
        print(simplex)
        xCoors = [filteredPoints[simplex[0]][0], filteredPoints[simplex[1]][0]]
        yCoors = [filteredPoints[simplex[0]][1], filteredPoints[simplex[1]][1]]
        print('xCoors: ', xCoors)
        print('yCoors: ', yCoors)
        ax.plot(xCoors, yCoors, 'k-')
 
    plt.show()
