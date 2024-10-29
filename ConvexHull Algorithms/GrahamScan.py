import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt

def isRight(A,B,C):
    check=np.array_equal(A,C)
    if check:
        return 0
    check=np.array_equal(B,C)
    if check:
        return 0
    
    testA=[1] + list(A) 
    testB=[1] + list(B)
    testC=[1] + list(C)


    array=np.array([testA,testB,testC])
    #array=[[1,Ax,Ay],
    #       [1,Bx,By],
    #       [1,Cx,Cy]]
    det=linalg.det(array)
    return det # if det<0 it's right if det>0 it's left

def sortLeks(lista,anapoda=False):
    x=sorted(lista,key=lambda x: x[0],reverse=anapoda)
    return x

def graham(Points):
    PointsLeksikografika=sortLeks(Points)
    Lup=[]
    #add the first 2 points to the array
    Lup.append(PointsLeksikografika[0])
    Lup.append(PointsLeksikografika[1])
    LupEnd=1#used to keep track of the end of the array
    size=len(Points)
    for i in range(2,size):
        Lup.append(PointsLeksikografika[i])
        LupEnd+=1
        test=isRight(Lup[LupEnd-2], Lup[LupEnd-1], Lup[LupEnd])
        while test>0 :
            del Lup[LupEnd-1]
            LupEnd-=1
            #at least 2 
            if LupEnd<2:
                break    
            test=isRight(Lup[LupEnd-2], Lup[LupEnd-1], Lup[LupEnd])

# Instead of making and] Ldown and merging the arrays I will keep updating the Lup with the lower half of the convex hull
    
    LdownEnd=LupEnd#the end of the array. LupEnd will keep track of the end of the upper half
    Lup.append(PointsLeksikografika[-2])#i already have the last point in the array so i add only the second to last
    LdownEnd+=1
    #size-1 last item of PointsLeksikografika -> size-3 3rd from last
    for i in range((size - 3),-1,-1): #go in reverse from the 3rd last
        Lup.append(PointsLeksikografika[i])
        LdownEnd+=1
        test=isRight(Lup[LdownEnd-2], Lup[LdownEnd-1], Lup[LdownEnd])
        while test>0 :
            del Lup[LdownEnd-1]
            LdownEnd-=1
            #at least 2 points in the lower 
            if (LdownEnd - LupEnd) <2 :
                break
            test=isRight(Lup[LdownEnd-2], Lup[LdownEnd-1], Lup[LdownEnd])

    return Lup

def printGraham (Points):
    convex0=graham(Points)
    #make points and convex into an array to use matplotlib
    pointsAr=np.array(Points)
    convex=np.array(convex0)
    #print the list of the points in convex
    print("The vertices of the convex hull are: ")
    j=0
    for i in convex[:-1]:
        print(j+1,":",i)
        j+=1
    print(j,"in total")
    #plot all the points
    plt.plot(pointsAr[:,0],pointsAr[:,1],'o')
    
    #plot the convex hull
    plt.plot(convex[:,0],convex[:,1],'-k',marker='o',mec='r')
    #annotate the convex hull
    k=1
    for i in convex[:-1]:
        plt.annotate(k,i)
        k+=1
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title("Convex Hull using Gaham's scan") 
    plt.show()

points=np.random.rand(100,2)*10
printGraham(points)


