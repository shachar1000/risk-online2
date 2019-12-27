import random
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import math

class NoiseEdge():
    def __init__(self, polys, centroids):
        self.polys = polys
        self.centroids = centroids
        self.new = []



        self.cMaxX = max(list(map(lambda centroid: centroid[0], centroids)))
        self.pMaxX = max(list(map(lambda poly: poly[0], polys)))
        self.cMaxY = max(list(map(lambda centroid: centroid[1], centroids)))
        self.pMaxY = max(list(map(lambda poly: poly[1], polys)))

        print(self.cMaxX)



        self.noiseEdge(polys, centroids)
        linePairs = [line for pair in self.new for line in pair]
        newDots = [dot for line in linePairs for dot in line]
        new_k = []
        for elem in newDots:
            if not (elem in new_k):
                new_k.append(elem)
        newDots = new_k
        # sort by x or sort by y?

        if self.cMaxY > self.pMaxY:
            newDots = sorted(newDots , key=lambda k: [k[0], k[1]]) # sort by x
        else:
            newDots = sorted(newDots , key=lambda k: [k[1], k[0]]) # sort by y

        self.newDots = newDots

    def adjacent(self, list, n):
        groups = [list[i:i + n] for i in range(len(list) + 1 - n)]
        groups.append([list[0], list[::-1][0]])
        return groups


    def noiseEdge(self, polys, centroids, count=0):

        polygon = [polys[0], centroids[0], polys[1], centroids[1]]
        sides = self.adjacent(polygon, 2)

        means = [[    (sides[y][0][coor]+sides[y][1][coor])  /  2 for coor in range(2)] for y in range(len(sides))]

        # means = []
        # for i in range(len(sides)): # which side
        #     means.append([])
        #     for y in range(len(sides[i])-1): # which point
        #         for coor in range(len(sides[i][y])): # which
        #             means[i].append((sides[i][y][coor]+sides[i][y+1][coor])/2)
        # if count > 0:
        # distance = [(abs(centroids[1][coor] - centroids[0][coor])*0.4) for coor in range(2)] # x and y dist between points (centroids)
        # largestPoint = []
        m = (centroids[1][1] - centroids[0][1]) / (centroids[1][0] - centroids[0][0])
        b = centroids[1][1] - (m*centroids[1][0]) #b=y-mx
        # randomPointY = random.uniform(centroids[0][1], centroids[1][1])
        # randomPointX = (randomPointY - b) / m
        if self.cMaxY > self.pMaxY:
            print("lol")
            distance = abs(polys[0][1]-polys[1][1]) # y distance between polys
            if polys[1][1] > polys[0][1]:
                randomPointY = random.uniform(polys[0][1], polys[1][1]+0.2)
            else:
                randomPointY = random.uniform(polys[1][1]+0.2, polys[0][1])


            randomPointX = (randomPointY - b) / m

        elif self.cMaxY < self.pMaxY:
            print("lolololol")
            distance = abs(polys[0][0]-polys[1][0])
            if polys[1][0] < polys[0][0]:
                randomPointX = random.uniform(polys[1][0], polys[0][0])
            else:
                randomPointX = random.uniform(polys[0][0], polys[1][0])

            randomPointY = (m*randomPointX)+b





        randomPoint = [randomPointX, randomPointY]


        print(randomPoint)
        # else:
        #randomPoint = [centroids[0][0]+(abs(centroids[1][0] - centroids[0][0])*0.5), centroids[0][1]+(abs(centroids[1][1] - centroids[0][1])*0.5)]
        plt.plot(randomPoint[0], randomPoint[1], 'ro')
        #newCentroids = [means[(i-1)*2:i*2] for i in range(1, 3)] # array of 2 arrays of polys for each new polygon
        newCentroids = [[means[0], means[3]], [means[1], means[2]]]
        newPolys = [[randomPoint, polys[0]],[randomPoint, polys[1]]]
        if count < 2:
            count = count + 1
            self.noiseEdge(newPolys[0], newCentroids[0], count)
            self.noiseEdge(newPolys[1], newCentroids[1], count)
        else: # if count = n
            # print(newPolys)
            self.new.append(newPolys)


    def random_color(self, str=True, alpha=0.5):
        rgb = [random.randint(0, 255) for i in range(3)]
        if str:
            return "rgba"+str(tuple(rgb+[alpha]))
        else:
            return list(np.array(rgb)/255) + [alpha]

    def display(self):

        poly = [self.centroids[0], self.polys[0], self.centroids[1], self.polys[1]]
        axes = plt.subplot(1,1,1)
        plt.axis([-0, 10, -0, 10])
        p = matplotlib.patches.Polygon(poly, facecolor=self.random_color(str=False, alpha=1))
        axes.add_patch(p)

        for i in range(len(self.newDots)-1):
            plt.plot([self.newDots[i][0], self.newDots[i+1][0]], [self.newDots[i][1], self.newDots[i+1][1]], 'k-', lw=0.7)

        # x = [dot[0] for dot in newDots]
        # y = [dot[1] for dot in newDots]

        #plt.scatter(x, y, zorder=10)

        plt.show()
if __name__ == '__main__':
    #additional = NoiseEdge([[3, 3], [3, 0]], [[0, 1.5], [6, 1.5]], 0)


    additional = NoiseEdge([[8, 5], [4, 6]],  [[4, 3], [8, 18]])
    print(additional.cMaxY)
    #
    # print(random.uniform(1,0))
    #
    #
    #
    # print(additional.newDots)
    additional.display()
