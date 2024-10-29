import numpy as np
from scipy import linalg
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt

def isBetween(A,B,pointBetween):
    if euclidean(A,B)==(euclidean(A,pointBetween)+euclidean(pointBetween,B)):
        return 1
    else:
        return 0
def isRight(A,B,C):
    check=np.array_equal(A,C)
    if check:
        return 0
    check=np.array_equal(B,C)
    if check:
        return 0
    testA=np.insert(A,0,1)    
    testB=np.insert(B,0,1)
    testC=np.insert(C,0,1)


    array=np.array([testA,testB,testC])
    #array=[[1,Ax,Ay],
    #       [1,Bx,By],
    #       [1,Cx,Cy]]
    det=linalg.det(array)
    return det # if det<0 it's right if det>0 it's left

#giftwrapping algorithm
def giftWrapping(points):
    #find the point in points with the smallest x coordinate
    localpoints=np.array(points)
    pointsLength=len(localpoints)
    if pointsLength<3:
        print("Need at least 3 points for a convex hull")
        return -1

    #find the point with the smallest x coordinate
    r0=np.copy(localpoints[0])
    for i in range(pointsLength):
        if localpoints[i][0]<r0[0]:
            r0=np.copy(localpoints[i])
        elif localpoints[i][0]==r0[0]:
            if localpoints[i][1]<r0[1]:
                r0=np.copy(localpoints[i])
    convexHull=np.array([r0])

    r=np.copy(r0)
    notChoosenPoints=np.copy(localpoints)
    while(True):
        u=notChoosenPoints[0]

        for i in range(pointsLength):
            if isRight(r,u,localpoints[i])<0:
                u=np.copy(localpoints[i])
            elif isRight(r,u,localpoints[i])==0: #in case the points are in the same line
                if isBetween(r,localpoints[i],u)==1:
                    u=np.copy(localpoints[i])
        r=np.copy(u)
        notChoosenPoints=notChoosenPoints[~np.all(notChoosenPoints==r,axis=1)] #remove the choosen point from the list
        if np.all(r==r0):
            break
        convexHull=np.append(convexHull,[r],axis=0)#add the point to the convex hull

    convexHull=np.append(convexHull,[r0],axis=0)
    return convexHull

def printConvexHull(points):
    convexHull=giftWrapping(points)
    #print the list of the points in convex hull
    print("The edges of the convex hull are: ")
    j=0
    for i in convexHull[:-1]:
        print(j+1,":",i)
        j+=1
    print(j,"in total")
    #add all the points to the plot
    plt.plot(points[:,0],points[:,1],'o')

    #plot the convex hull
    plt.plot(convexHull[:,0],convexHull[:,1],'-k',marker='o',mec='r')

    #annotate the convex hull
    k=1
    for i in convexHull[:-1]:
        plt.annotate(k,i)
        k+=1
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title("Convex Hull using GiftWrapping") 
    plt.show()


# Provided data points
points_x = [632, 1330, 3051, 5040, 5883, 8130, 9280, 9613, 9422, 8996, 8020, 8467, 6735, 4674, 2519, 973, 1205, 1929, 3203, 5345]
points_y = [1588, 1097, 470, 1077, 2766, 3629, 2836, 4963, 6363, 7327, 7611, 9720, 9183, 7865, 7692, 9797, 6005, 5812, 6301, 2923]

# Combine points_x and points_y into a single array of (x, y) pairs
points = np.array(list(zip(points_x, points_y)))

print(points)

printConvexHull(points)
        
    

        