from flask import Flask, render_template, jsonify, url_for, request
import json
from flask_mysqldb import MySQL
import numpy as np
import matplotlib.pyplot as plt
from perlin import perlinClass
import voronoi
from voronoi import improveVoronoi, centroids
import sys
import io
import base64
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from matplotlib import path
import math

sys.setrecursionlimit(1000000000)

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'eaea7265'
app.config['MYSQL_DB'] = 'risk'

mysql = MySQL(app)

@app.route("/")
def index():
    database()
    return render_template('index.html')

@app.route("/test", methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        data = {"data": "success"}
        response = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
        return response

@app.route('/dbdisplay')
def dbdisplay():
    cur = mysql.connection.cursor()
    query = "SELECT * FROM territories;"
    cur.execute(query)
    data = cur.fetchall() # all rows
    num_fields = len(cur.description)
    field_names = [i[0] for i in cur.description]
    return render_template('dbdisplay.html', data=data, field_names=field_names)

# import random
# def cubes(cubes1, cubes2):
#     cubes = [{"number": random.randint(1, 6), "player": 1 if i < cubes1 else 2} for i in range(cubes1+cubes2)]
#     numbers = [cube['number'] for cube in cubes]
#     for count, cubeNum in enumerate(numbers):
#         for j in range(0, len(cubes)-count-1):
#             if numbers[j] < numbers[j+1]:
#                 i = j #swap adjacent elements
#                 numbers[i:i+2] = numbers[i+1:i-1:-1]
#                 cubes[j], cubes[j+1] = cubes[j+1], cubes[j]
# cubes(3, 2)



array = [[2, 3],
[1],
[1, 4, 5],
[3, 6],
[3],
[4]]

#Neigbors = ', '.join(str(x) for x in array[count] for sublist, count in enumerate(array))
def database():
    cur = mysql.connection.cursor()
    cur.execute("TRUNCATE TABLE territories")
    for i in range(len(array)):
        Neigbors = ', '.join(str(item) for item in array[i])
        cur.execute("INSERT INTO territories(Neigbors, Num) VALUES (%s, %s)", (Neigbors, i+1))
    mysql.connection.commit()
    cur.close()

done = False
covered = []
def checkContiguity(array, start, end, previous): #previous x that called the recursion
    covered.append(start)
    global done
    if (done):
        return
    for c, x in enumerate(array[start-1]):
        if x is not previous and done is False and x not in covered:
            print(x)
            if (x == end):
                done = True
                print("OK")
                return
            elif len(array[x-1]) is not 0:
                if not (len(array[x-1]) is 1 and array[x-1][0] is start):
                    checkContiguity(array, x, end, start)
def createGrid():
    lin = np.linspace(0,2,10,endpoint=False)
    #10 spaces between 0 and 1
    y,x = np.meshgrid(lin,lin)
    perlinGrid = perlinClass(x,y)
    print(perlinGrid.perlinGrid)


    w = len(perlinGrid.perlinGrid[0])
    h = len(perlinGrid.perlinGrid)

    neighborsPerlin = []
    for y in range(len(perlinGrid.perlinGrid)):
        for x in range(len(perlinGrid.perlinGrid[y])):
            neighbors = [(x+a[0], y+a[1]) for a in
                                [(-1,0), (1,0), (0,-1), (0,1)]
                                if ( (0 <= x+a[0] < w) and (0 <= y+a[1] < h))]
            neighborsPerlin.append(neighbors)
    #neighborsPerlin = list(x for y in neighborsPerlin for x in y)
    lenX = [len(array) for array in neighborsPerlin]
    neighborsPerlin = [(10*tuple[1])+tuple[0]+1 for array in neighborsPerlin for tuple in array]
    neighborsPerlin = [neighborsPerlin[sum(lenX[0:i]):sum(lenX[0:i+1])] for i in range(len(lenX))]

    print(neighborsPerlin)
    checkContiguity(neighborsPerlin, 4, 30, 4)

@app.route('/voronoi')
def perlinVoronoi():
    plt.clf()
    P = np.random.random((200,2))
    polys = voronoi.voronoiPolygons(P)
    #voronoi.displayVoronoi(polys)
    for i in range(10):
        polys = improveVoronoi(polys)

    centroidsP = centroids(polys)

    lin = np.linspace(0,3,100,endpoint=False)
    #10 spaces between 0 and 1
    y,x = np.meshgrid(lin,lin)
    perlinGrid = perlinClass(x,y)

    points = perlinGrid.points
    plt.plot(points[:,0], points[:,1], 'ro')
    plt.imshow(perlinGrid.perlinGrid)

    def fig_to_base64():
        img = io.BytesIO()
        plt.savefig(img, format='png',
                    bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue())

    encoded = fig_to_base64()
    perlin_html = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))

    polyPlayer = [0]*len(polys)

    # for count, poly in enumerate(polys):
    #     for i in range(len(points)):
    #         polygon = Polygon(poly)
    #         if polygon.contains(Point(points[i]/100)):
    #             polyPlayer[count] = 1

    for countC, centroid in enumerate(centroidsP):
        minDist = 10000000
        indexP = 0
        for countP, point in enumerate(points):
            distance =  math.sqrt( ((centroid[0]-(points[countP][0]/100))**2)+((centroid[1]-(points[countP][1]/100))**2) )
            if (distance < minDist):
                minDist = distance
                indexP = countP
        app.logger.info(minDist)
        polyPlayer[countC] = perlinGrid.perlinGrid[int(points[indexP][1])-1][int(points[indexP][0])-1]

    voronoi_html = voronoi.displayVoronoi(polys, random=False, players=polyPlayer)
    return perlin_html+voronoi_html

if __name__ == "__main__":
    app.run(debug=True)
