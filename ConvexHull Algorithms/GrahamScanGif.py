import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy import linalg

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
    return det # if det<0 it's right if det>0 it's left

def graham(Points):
    sortedPoints=Points[Points[:,0].argsort()] 
    Lup=[]
    framesArray=[]
    Lup.append(sortedPoints[0].copy())
    framesArray.extend([np.vstack(Lup)])
    Lup.append(sortedPoints[1].copy())
    framesArray.extend([np.vstack(Lup)])
    LupEnd=1#used to keep track of the end of the array
    size=len(Points)
    for i in range(2,size):
        Lup.append(sortedPoints[i].copy())
        framesArray.extend([np.vstack(Lup)])
        LupEnd+=1
        test=isRight(Lup[LupEnd-2], Lup[LupEnd-1], Lup[LupEnd])
        while test>0 :
            del Lup[LupEnd-1]
            framesArray.extend([np.vstack(Lup)])
            LupEnd-=1
            #at least 2 
            if LupEnd<2:
                break    
        test=isRight(Lup[LupEnd-2], Lup[LupEnd-1], Lup[LupEnd])
    LdownEnd=LupEnd
    Lup.append(sortedPoints[-2].copy())
    framesArray.extend([np.vstack(Lup)])
    LdownEnd+=1
    #size-1 last item of PointsLeksikografika -> size-3 3rd from last
    for i in range((size - 3),-1,-1): #go in reverse from the 3rd last
        Lup.append(sortedPoints[i].copy())
        framesArray.extend([np.vstack(Lup)])
        LdownEnd+=1
        test=isRight(Lup[LdownEnd-2], Lup[LdownEnd-1], Lup[LdownEnd])
        while test>0 :
            del Lup[LdownEnd-1]
            framesArray.extend([np.vstack(Lup)])
            LdownEnd-=1
            #at least 2 
            if LdownEnd<2:
                break
            test=isRight(Lup[LdownEnd-2], Lup[LdownEnd-1], Lup[LdownEnd])
    
    return framesArray



def update(frame):
    ax.clear()
    ax.plot(frame[:, 0], frame[:, 1], '-k',mec='r')

    ax.set_title("Convex Hull using Gaham's scan step by step")
    # Plot additional points in every frame
    ax.plot(additional_points[:, 0], additional_points[:, 1], 'ro')






# Create list of points
additional_points =np.array([[1,2],[2,2],[4,5],[3,2],[5,5],[6,8],[5,1],[2,0]])
convexFrames=graham(additional_points)
# Create an empty figure and axis
fig, ax = plt.subplots()
# Define the update function

# Create the animation
animation = FuncAnimation(fig, update, frames=convexFrames, interval=500,repeat=False)
# Show the animation
plt.show()
