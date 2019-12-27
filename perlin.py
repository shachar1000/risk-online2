import numpy as np
import matplotlib.pyplot as plt


class perlinClass():
    def __init__(self, x, y):
        self.perlinGrid = self.perlin(x, y)
        self.perlinGrid = self.partition(3, self.perlinGrid)
        self.points = self.points(20, 20)

    def perlin(self, x, y, seed=3748):
        # permutation table
        np.random.seed(seed)
        p = np.arange(256,dtype=int)
        np.random.shuffle(p)
        p = np.stack([p,p]).flatten()
        # coordinates of the top-left
        xi = x.astype(int)
        yi = y.astype(int)
        # internal coordinates
        xf = x - xi
        yf = y - yi
        # fade factors
        u = fade(xf)
        v = fade(yf)
        # noise components
        n00 = gradient(p[p[xi]+yi],xf,yf)
        n01 = gradient(p[p[xi]+yi+1],xf,yf-1)
        n11 = gradient(p[p[xi+1]+yi+1],xf-1,yf-1)
        n10 = gradient(p[p[xi+1]+yi],xf-1,yf)
        # combine noises
        x1 = lerp(n00,n10,u)
        x2 = lerp(n01,n11,u) # FIX1: I was using n10 instead of n01
        return lerp(x1,x2,v) # FIX2: I also had to reverse x1 and x2 here

    def partition(self, numPlayers, perlinGrid):
        minX = min(perlinGrid.flatten())
        maxX = max(perlinGrid.flatten())
        print(minX)
        print(maxX)
        numPlayers = 3
        rangeVector = [[minX+((maxX-minX)/numPlayers)*(n), minX+(((maxX-minX)/numPlayers)*(n+1))] for n in range(numPlayers)]
        print(rangeVector)
        for y in range(len(perlinGrid)):
            for x in range(len(perlinGrid[0])):
                pixel = perlinGrid[y][x]
                for i in range(numPlayers):
                    if ((rangeVector[i][0] <= pixel) and (pixel <= rangeVector[i][1])):
                        perlinGrid[y][x] = round(rangeVector[i][0], 5)
                        # round so we dont get 1.699999 and 1.69991000 for instance
        print(perlinGrid[0][0])
        return perlinGrid

    def points(self, numX, numY):
        stepX = 100/numX
        stepY = 100/numY
        return np.array([np.array([100/numX*x, 100/numY*y]) for y in range(int(len(self.perlinGrid)/stepY)+1) for x in range(int(len(self.perlinGrid[y])/stepX)+1)])


def lerp(a,b,x):
    "linear interpolation"
    return a + x * (b-a)

def fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def gradient(h,x,y):
    "grad converts h to the right gradient vector and return the dot product with (x,y)"
    vectors = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vectors[h%4]
    return g[:,:,0] * x + g[:,:,1] * y

if __name__ == '__main__':
    lin = np.linspace(0,3,100,endpoint=False)
    #10 spaces between 0 and 1
    x, y = np.meshgrid(lin,lin)
    perlinGrid = perlinClass(x,y)

    points = perlinGrid.points
    print(points[-1])

    plt.plot(points[:,0], points[:,1], 'ro')

    plt.imshow(perlinGrid.perlinGrid)
    plt.show()
