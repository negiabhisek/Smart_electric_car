_author__ = 'Abhisek Negi'

import cv2
import numpy as np
import glob

print 'Loading training data...'
e0 = cv2.getTickCount()

# load training data
image_array = np.zeros((1, 240*120))
label_array = np.zeros((1, 4), 'float')
training_data = glob.glob('training_data_temp/*.npz')

fourcc = fourcc = cv2.cv.CV_FOURCC(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (240,120))

for single_npz in training_data:
    with np.load(single_npz) as data:
	print "one"
        print data.files
        train_temp = data['train']
        print train_temp.shape
    image_array = np.vstack((image_array, train_temp))

train = image_array[1:, :]
print train.shape

e00 = cv2.getTickCount()
time0 = (e00 - e0)/ cv2.getTickFrequency()
print 'Loading image duration:', time0
count=0
for i in train:
	i = i
	count = count+1
	img = i.reshape(120,240)
	print count,img
	#cv2.imwrite(str(count)+".jpg",img)
	cv2.imshow("image",img)
	#out.write(img)
	k = cv2.waitKey(0) & 0xff
	if k == 27:
		break

cv2.destroyAllWindows()
