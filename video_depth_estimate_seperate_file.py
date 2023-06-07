import cv2
import numpy as np
import glob
from crestereo import CREStereo, CameraConfig

def main() :
	# Initialize video
	left_vid = cv2.VideoCapture(input("Left Video file Path : "))
	right_vid = cv2.VideoCapture(input("Right Video file Path : "))

	# Model options (not all options supported together)
	iters = 10          # Lower iterations are faster, but will lower detail. 
						# Options: 2, 5, 10, 20 

	input_shape = (320, 480)   # Input resolution. 
						# Options: (240,320), (320,480), (380, 480), (360, 640), (480,640), (720, 1280)

	version = "combined" # The combined version does 2 passes, one to get an initial estimation and a second one to refine it.
						# Options: "init", "combined"

	model_path = f'models/crestereo_{version}_iter{iters}_{input_shape[0]}x{input_shape[1]}.onnx'
	depth_estimator = CREStereo(model_path, max_dist = 2)

	cv2.namedWindow("Estimated depth", cv2.WINDOW_NORMAL)	
	while left_vid.isOpened() and right_vid.isOpened():
		try:
			# Read frame from the video
			ret, left = left_vid.read()
			ret2, right = right_vid.read()
			if not ret:	
				break
		except:
			continue

		# Estimate the depth
		disparity_map = depth_estimator(left, right)
		color_depth = depth_estimator.draw_depth()
		combined_image = np.hstack((left, color_depth))

		cv2.imshow("Estimated depth", combined_image)

		key = cv2.waitKey(1) & 0xFF
		# Press key q or esc to stop
		if key == ord('q') or key == 27: # 27 = esc key
			break

	left_vid.release()
	right_vid.release()
	cv2.destroyAllWindows()

if __name__ == "__main__" :
	main()
