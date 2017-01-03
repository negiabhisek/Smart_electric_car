__author__ = "Abhisek Negi"

import numpy as np
import cv2
print(cv2.getBuildInformation())
saved_frame = 0
total_frame = 0

print 'Start collecting images...'
e1 = cv2.getTickCount()
image_array = np.zeros((1, 240*120))
if __name__ == '__main__':
	cap = cv2.VideoCapture(0)
	frame = 1
	while cap.isOpened():
		ret, img = cap.read()
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# resize the image
		roi = cv2.resize(img, (240, 120)) 

		# save streamed images
		cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), img)
		print roi.shape
		# reshape the roi image into one row array
		temp_array = roi.reshape(1, 240*120)
		i = temp_array.copy()
		img = i.reshape(120,240)
		print img
		cv2.imshow("image",img)
		frame += 1
		total_frame += 1

		#cv2.imshow("image",roi)
	
		image_array = np.vstack((image_array, temp_array))
		saved_frame += 1
		k = cv2.waitKey(10) & 0xff
		if k == 27:
		    break
	# save training images and labels
	train = image_array[1:, :]
	# save training data as a numpy file
	np.savez('training_data_temp/test08.npz', train=train)

	e2 = cv2.getTickCount()
	# calculate streaming duration
	time0 = (e2 - e1) / cv2.getTickFrequency()
	print 'Streaming duration:', time0

	print(train.shape)
	
	print 'Total frame:', total_frame
	print 'Saved frame:', saved_frame
	print 'Dropped frame', total_frame - saved_frame

	cap.release()
	cv2.destroyAllWindows()
