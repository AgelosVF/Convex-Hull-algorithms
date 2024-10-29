import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

#returns the det of the 3 points if det<0 C is right. if det>0 C is left
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
    det=linalg.det(array)
    return det 

#returns 1 if the line is the tangent of the convex hull right=1 for upper right=0 for lower
def isTangent(line,hull,right):
    #takes as argument a np.array containing 2 points of a line a np.array containing the points of the convex hull
    #and a boolean value indicating if it should check clockwise or counterclockwise
    if right==1:
        #upper tangent of right hull or left
        #line has the left hull point first and right second
        for i in hull:
            check=isRight(line[0],line[1],i)
            if (check > 0):
                return 0
        return 1
    if right==0:
        for i in hull:
            check=isRight(line[0],line[1],i)
            if (check < 0):
                return 0
        return 1
    print("Something whent wrong in isTangent got line:",line,"hull:",hull,"right:",right)

#find the next point clockwise right=0 or counterclockwise right=1
#returns the next point
def nextPoint(line,polygon,right):
    #right==0 means move left right==1 means move right
    if right==0:
        for i in polygon:
            check=isRight(line[0],line[1],i)
            if (check < 0):
                return i
    if right==1:
        for i in polygon:
            check = isRight(line[0],line[1],i)
            if (check > 0):
                return i
    print("Error in nextPoint \n I got line:",line,"polygon:",polygon,"right:",right)


#if the array has less than 6 points return the convex hull else divide it to 2 call self for both halfs and return the merge (dfs)
def Divide(points,length):
    if length < 6:
        hull=ConvexHull(points)
        hullPoints=points[hull.vertices] #they should be in counter clockwise order around the hull
        return hullPoints
    #divide the array to 2 
    halflength=length//2
    leftArr=Divide(points[:halflength],halflength)
    rightArr=Divide(points[halflength:],(length - halflength)) 
    #leftArr has half rounded down and rightArr has half rounded up (in the notes its the oposite)
    return mergeHull(leftArr,rightArr)


#remove the points from the array that are not going edges in the combined convex hull
#returns the filtered array that contains the edges starting from the start point moving counterclockwise to the end point
def filterArrayCC(startPoint,endPoint,array):
    #find the indices of the start and end point in the array
    startIndex=np.where((array == startPoint).all(axis=1))[0][0]
    endIndex=np.where((array == endPoint).all(axis=1))[0][0]

    #check if the end index is before the start index
    if endIndex<startIndex:
        filtererdArray=np.concatenate((array[startIndex:],array[:endIndex+1]))
    else:
        filtererdArray=array[startIndex:endIndex+1]
    
    #the filtered array starts with the start point and ends with the end point while keeping the counter-clockwise order
    return filtererdArray

#take two convex hulls and merge them to one
def mergeHull(leftArr,rightArr):
    #find the rightmost point of the left hull
    leftsRightmost=leftArr[0]
    for i in range(1,len(leftArr)):
        if leftArr[i][0] > leftsRightmost[0]:
            leftsRightmost=leftArr[i]
    #find the rightsLeftmost point of the right hull
    rightsLeftmost=rightArr[0]
    for i in range(1,len(rightArr)):
        if rightArr[i][0] < rightsLeftmost[0]:
            rightsLeftmost=rightArr[i]

    line=np.vstack((leftsRightmost,rightsLeftmost)) #combine the points to a 2D array
    
    #find the upper tangent of the hull
    #for the upper tangent i move counter clockwise since the line starts from the left point and ends to the right
    while ((isTangent(line,leftArr,1)==0) or (isTangent(line,rightArr,1)==0)):
        #while it's not upper tangent to the left hull
        while(isTangent(line,leftArr,1)==0):
            #move counter clockwise to find the next point
            newLeftPoint=nextPoint(line,leftArr,1) 
            line=np.stack((newLeftPoint,line[1]))
        #While it's not upper tangent to the right hull
        while(isTangent(line,rightArr,1)==0):
            #move counter clockwise to find the next point
            newRightPoint=nextPoint(line,rightArr,1)
            line=np.stack((line[0],newRightPoint))
    
    upperTangent=line #upperTangent[0] is the left point and upperTangent[1] is the right point
    
    #find the lower tangent of the hull
    #for the lower tangent i move clockwise since the line starts from the left point and ends to the right
    line=np.vstack((leftsRightmost,rightsLeftmost)) #combine the points to a 2D array
    while ((isTangent(line,leftArr,0)==0) or (isTangent(line,rightArr,0)==0)):
        #while it's not lower tangent to the left hull
        while(isTangent(line,leftArr,0)==0):
            #move clockwise to find the next point
            newLeftPoint=nextPoint(line,leftArr,0) 
            line=np.stack((newLeftPoint,line[1]))
        #While it's not lower tangent to the right hull
        while(isTangent(line,rightArr,0)==0):
            #move clockwise to find the next point
            newRightPoint=nextPoint(line,rightArr,0)
            line=np.stack((line[0],newRightPoint))

    lowerTangent=line #lowerTangent[0] is the left point and lowerTangent[1] is the right point
    #need combine the left and right hull
    # the points in the arrays are in counter clockwise order
    #and i want to reserve that order
    #so i go from the left upper to the left lower
    #from left lower to right lower
    #from right lower to right upper
    #and from right upper to left upper

    #first we filter the left array
    startPoint=upperTangent[0]
    endPoint=lowerTangent[0]

    filteredLeftArray=filterArrayCC(startPoint,endPoint,leftArr)
    #now we have removed the points from the array that arent going vertices in the new convex hull

    #then we filter the right array starting from the lowest point and going counterclockwise to the highest point
    startPoint=lowerTangent[1]
    endPoint=upperTangent[1]
    filteredRightArray=filterArrayCC(startPoint,endPoint,rightArr)
    #combine the filtered arrays and return them
    return np.concatenate((filteredLeftArray,filteredRightArray))

def DivAndConq(points):
    sortedPoints=points[np.argsort(points[:,0])]
    lenght=len(sortedPoints)
    plt.plot(points[:,0],points[:,1],'o')
    convexHull=Divide(sortedPoints,lenght)
    convexHull=np.append(convexHull,[convexHull[0]],axis=0)
    
    #print the list of the points in convex
    print("The vertices of the convex hull are: ")
    j=0
    for i in convexHull[:-1]:
        print(j+1,":",i)
        j+=1
    print(j,"in total")

    plt.plot(convexHull[:,0],convexHull[:,1],'-k',marker='o',mec='r')
    #annotate the convex hull
    k=1
    for i in convexHull[:-1]:
        plt.annotate(k,i)
        k+=1

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Convex Hull using Divide and Conquer')
    plt.show()
    return 0



array=np.random.rand(100,2)*10
DivAndConq(array)



