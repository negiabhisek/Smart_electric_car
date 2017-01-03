__author__ = 'Abhisek Negi'

import numpy as np
import cv2


class CollectTrainingData(object):
    
	def __init__(self):
		self.collect_image()

	def collect_image(self):

		saved_frame = 0
		total_frame = 0

		# collect images for training
		print 'Start collecting images...'
		e1 = cv2.getTickCount()
		image_array = np.zeros((1, 38400))

		# stream video frames one by one
		try:
			cap = cv2.VideoCapture(0)
			print cap.set(1,10)
			#cap.set(cv2.CV_CAP_PROP_CONVERT_RGB , false)
			#cap.set(CV_CAP_PROP_FPS, 10)
			stream_bytes = ' '
			frame = 1
			while cap.isOpened():
				if True:
					ret, img = cap.read()
					img = cv2.resize(img, (320, 120)) 
					image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
					# select lower half of the image
					roi = image[120:240, :]

					# save streamed images
					cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)
					#cv2.imshow('roi_image', roi)
					cv2.imshow('image', image)

					# reshape the roi image into one row array
					temp_array = image.reshape(1, 38400)

					#get the data back and check
					ig = temp_array.copy()
					img2 = ig.reshape(120,320)
					print img2.shape
					cv2.imshow("image",img2)

					frame += 1
					total_frame += 1

					
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
		finally:
			cap.release()
			cv2.destroyAllWindows()

if __name__ == '__main__':
    CollectTrainingData()
