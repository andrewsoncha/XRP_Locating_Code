import matplotlib.pyplot as plt
import numpy as np
from math import radians, cos, sin, sqrt
from sklearn.neighbors import NearestNeighbors

def plotPolar(angleList, distList):
    fig = plt.figure()
    ax = fig.add_subplot(polar=True)
    ax.scatter(angleList, distList)
    plt.show()
    print('done plt show')

def plotCartesian(cartesianList):
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.scatter([pair[0] for pair in cartesianList], [pair[1] for pair in cartesianList])
    plt.show()

def polarToCartesian(polarCoor):
    angle = polarCoor[0]
    dist = polarCoor[1]
    return (dist*cos(angle), dist*sin(angle))

def getEuclideanDistance(coor1, coor2):
    return sqrt((coor1[0]-coor2[0])**2 + (coor1[1]-coor2[1])**2)

def evaluateDifference(fromCoorList, toCoorList):
    fromCoorNP = np.array(fromCoorList)
    toCoorNP = np.array(toCoorList)
    nbrs = NearestNeighbors(n_neighbors = 2, algorithm='ball_tree').fit(toCoorList)
    distances, indices = nbrs.kneighbors(fromCoorList)
    distance_list = [distance[1] for distance in distances]
    return sum(distance_list)

def evaluateOffset(fromCoorList, toCoorList, x_offset, y_offset):
    newFromCoorList = [(coor[0]+x_offset, coor[1]+y_offset) for coor in fromCoorList]
    diff_value = evaluateDifference(newFromCoorList, toCoorList)
    print(f'evaluating offset: ({x_offset}, {y_offset})  diff value: {diff_value}')
    return diff_value 

def findBestOffset(fromCoorList, toCoorList, minOffset = -400, maxOffset = 400, smallest=5):
    offsetList = []
    for x_offset in range(minOffset, maxOffset, smallest):
        for y_offset in range(minOffset, maxOffset, smallest):
            offsetList.append((x_offset, y_offset))

    offsetDifference = [evaluateOffset(fromCoorList, toCoorList, offset[0], offset[1]) for offset in offsetList]
    minDifference = min(offsetDifference)
    minIdx = offsetDifference.index(minDifference)
    return offsetList[minIdx]
    
if __name__ == '__main__':
    angleList = []
    distList = []
    cartesianList1 = []
    cartesianList2 = []
    with open('../testData/spinValuesDorm1', 'r') as file:
        for line in file:
            words = line.split()
            angleVal = radians(float(words[0]))
            distVal = float(words[1])
            if distVal > 400:
                continue
            print(f'{angleVal} {distVal}')
            angleList.append(angleVal)
            distList.append(distVal)
            cartesianList1 = [polarToCartesian(pair) for pair in zip(angleList, distList)]
    with open('../testData/spinValuesDorm2', 'r') as file:
        for line in file:
            words = line.split()
            angleVal = radians(float(words[0]))
            distVal = float(words[1])
            if distVal > 400:
                continue
            print(f'{angleVal} {distVal}')
            angleList.append(angleVal)
            distList.append(distVal)
            cartesianList2 = [(polarToCartesian(pair)[0]-100, polarToCartesian(pair)[0]+200) for pair in zip(angleList, distList)]

    print(zip(angleList, distList))
    #plotCartesian(cartesianList)

    print('best offset: ', findBestOffset(cartesianList1, cartesianList2))

