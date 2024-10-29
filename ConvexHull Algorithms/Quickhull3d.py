import numpy as np
from mpl_toolkits.mplot3d import Axes3D
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
    ax=fig.add_subplot(111,projection='3d')
    ax.plot_trisurf(points[:,0],points[:,1],points[:,2],triangles=hull.simplices,alpha=0.3)

    #add the rest of the points
    ax.plot(points[:,0],points[:,1],points[:,2],'o')
    #'o' means the points aren't connected

    #mark the edges of the convex hull
    for edge in hull.simplices:
        ax.plot(points[edge,0],points[edge,1],points[edge,2],'k-',marker='o',mec='r') 
        #'k-' means the line (edge) is black 
        #marked='o' means the points are circled
        #mec='r' means the color is red
        
     
    #SET LABELS AND TITLE 
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Convex Hull using Quickhull')
    plt.show()

points=np.random.rand(80,3)*10
printHull(points)
