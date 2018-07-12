import gdal
import time
import sys
import random
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from gdalconst import *

print(sys.argv)         # prints filename as it is the first argument given to console
starttime=time.time()

ds =gdal.Open('/home/shriya/Dropbox/siplab/aviris.tif')
inimage = ds.ReadAsArray()
grnd = gdal.Open('/home/shriya/Dropbox/siplab/ground.tif')
re_grnd= grnd.ReadAsArray()

cols = ds.RasterXSize           #145
rows = ds.RasterYSize		#145
bands = ds.RasterCount		#220

new_cols=rows*cols
new_rows=bands+3                            

rn=np.zeros((new_cols,))
cn=np.zeros((new_cols,))
count=0
for i in range(rows):
    for j in range(cols):
        rn[count]= i             # row numbers at 222
        cn[count]= j             # column numbers at 223
	count+=1             

mat=np.reshape(inimage,(bands,-1))    # conversion from 3D to 2D with shape 223*21025
ground=np.reshape(re_grnd,(1,-1))
ground=np.vstack((ground,rn,cn))   # 1D array form of ground file at 220th row containing class numbers

np.random.seed(0)
indices=np.random.permutation(len(mat.T))
part=int(0.8*new_cols)
mat_train=mat[:,indices[:part]]
mat_test=mat[:,indices[part:]]
ground_train=ground[:,indices[:part]]
ground_test=ground[:,indices[part:]]

k=input("Enter the value of K: ")

knn=KNeighborsClassifier(n_neighbors=k,metric='euclidean',algorithm='auto',p=1)
knn.fit(mat_train.T,ground_train[0,:])
output=knn.predict(mat_test.T)

for i in range(new_cols-part):
	if ground_test[0,i]==0:
            output[i]=0

c=0
for i in range(new_cols-part):
        if output[i]==ground_test[0,i]:
            	c+=1
print c
Accuracy = (c*100.0)/(new_cols-part)                  # as training data shouldnt be used for accuracy calculations
print Accuracy

# for plotting
out= np.zeros((rows,cols))

for i in range(new_cols -part):                                                   # for test data
	out[int(ground_test[1,i]),int(ground_test[2,i])]=int(output[i])
for i in range(part):
	out[int(ground_train[1,i]),int(ground_train[2,i])]=int(ground_train[0,i])  # class numbers of training data acc original indices

endtime=time.time()
print 'the program took '+str(endtime-starttime)+' seconds'

from matplotlib import pyplot as plt
plt.imshow(out, interpolation='nearest')
plt.show()


