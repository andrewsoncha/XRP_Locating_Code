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
    print(zip(angleList, posList, distList))
    cartesianList1 = [polarToCartesian(pair) for pair in zip(angleList, posList, distList) if pair[1]==(0,0)]
    cartesianList2 = [polarToCartesian(pair) for pair in zip(angleList, posList, distList) if pair[1]==(5,0)]
    fig = plt.figure()
    ax = fig.add_subplot()
    plotCartesian(ax, cartesianList1, color='b')
    plotCartesian(ax, cartesianList2, color='red')
    plt.show()
    #plotPolar(angleList, distList)

