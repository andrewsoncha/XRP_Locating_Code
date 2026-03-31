import matplotlib.pyplot as plt
import numpy as np
from math import radians, cos, sin

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

if __name__ == '__main__':
    angleList = []
    distList = []
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
    print(zip(angleList, distList))
    cartesianList = [polarToCartesian(pair) for pair in zip(angleList, distList)]
    plotCartesian(cartesianList)
    #plotPolar(angleList, distList)

