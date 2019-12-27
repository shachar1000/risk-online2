from matplotlib import pyplot as plt
import random


def makeRand(seed):
    multiplier = 47272
    wrap = 0x7FFFFFFF
    seed = seed % wrap
    def inner():
        seedX = seed * multiplier % wrap
        return seedX
    return inner


def makeRandInt(seed):
    generator = makeRand(seed)
    def inner(N):
        return generator() % N
    return inner

def makeRandFloat(seed):
    wrap = 0x7FFFFFFF
    generator = makeRand(seed)
    def inner():
        return (generator() - 1.0) / (wrap - 1.0)
    return inner

def mixp(p, q, t):
    #plt.plot([p[0], q[0]], [p[1], q[1]], 'ro')
    return [
        q[0] * (1-t) + p[0] * t,
        q[1] * (1-t) + p[1] * t
    ]
    # replace q with p to change the vertex where we start measuring to cut
    # for example with q[0] * (1-t) we start from q

def recursiveSubdivision(level, quad, randFloat, seed):
    a, b, p, q = quad["a"], quad["b"], quad["p"], quad["q"]
    if (level <= 0):
        return {
            "line": [a, b],
            "quads": [level, a, p, b, q]
        }

    ap = mixp(a, p, 0.5)
    bp = mixp(b, p, 0.5)
    aq = mixp(a, q, 0.5)
    bq = mixp(b, q, 0.5)

    # division = random.uniform(0, 1)
    divisionSpan = 0.9
    division = 1 * (1 - divisionSpan) + randFloat() * divisionSpan

    #print(division)

    center = mixp(p, q, division)

    quad1 = {"a": a, "b": center, "p": ap, "q": aq}
    quad2 = {"a": center, "b": b, "p": bp, "q": bq}

    newSeed = makeRandInt(seed)(0x7fffffff)

    results1 = recursiveSubdivision(level -1, quad1, makeRandFloat(newSeed), newSeed)
    results2 = recursiveSubdivision(level-1, quad2, makeRandFloat(newSeed), newSeed)

    return {
        "line": results1["line"] + results2["line"][1:],
        "quads": results1["quads"] + ([level, a, p, b, q]+results2["quads"])
    }

def refineQuads(quads):
    quadsFinal = []
    prev = 0
    for i in range(len(quads)):
        if isinstance(quads[i], int) and i != 0:
            quadsFinal.append(quads[prev+1:i]) # +1 to remove level
            quadsFinal[-1].append(quads[prev+1]) # add first point so we close the quad
            prev = i
    return quadsFinal

def displayQuads(quadsFinal):
    for quad in quadsFinal:
        plt.plot([point[0] for point in quad], [point[1] for point in quad]) # quad[1:] if we include the level in the array for opacity

def displayLine(line):
    plt.plot([point[0] for point in line],[point[1] for point in line])

myQuad = {"a":[150, 150], "b": [450, 120], "p": [300, 50], "q": [350, 250]}
recursive = recursiveSubdivision(6, myQuad, makeRandFloat(1), 1)

line = recursive["line"]
quads = recursive["quads"]

quadsFinal = refineQuads(quads)
displayQuads(quadsFinal)
displayLine(line)
plt.show()
