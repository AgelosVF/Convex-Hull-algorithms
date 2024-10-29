import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

def quickhull(points):
    hull=ConvexHull(points)
    return hull

def printHull(points):
    hull=quickhull(points)
    #print the vertices of the convex hull

    print("The vertices of the convex hull are: ")
    j=0
    for i in hull.vertices:
        j+=1
        vertexCoordinates=points[i]
        print("\t",vertexCoordinates)
    print(j,"in total")
    #plot the convex hull
    fig=plt.figure()
    
    plt.plot(points[:,0],points[:,1],'o')

    #add the rest of the points
    #'o' means the points aren't connected

    #mark the edges of the convex hull
    for edge in hull.simplices:
        plt.plot(points[edge,0],points[edge,1],'k-',marker='o',mec='r') 
        #'k-' means the line (edge) is black 
        #marked='o' means the points are circled
        #mec='r' means the color is red
        
     
    #SET LABELS AND TITLE 
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(' Convex Hull using Quickhull')
    plt.show()

points=np.random.rand(100,2)*10
printHull(points)
