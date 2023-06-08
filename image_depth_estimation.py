import cv2
import numpy as np
from datetime import datetime

from imread_from_url import imread_from_url

from crestereo import CREStereo

def main() :
	s = datetime.now()
	# Model Selection options (not all options supported together)
	iters = 5            # Lower iterations are faster, but will lower detail. 
						# Options: 2, 5, 10, 20 

	model_shape = (240, 320) # Options: (240,320), (320,480), (360, 640), (480,640), (720, 1280)

	version = "combined" # The combined version does 2 passes, one to get an initial estimation and a second one to refine it.
						# Options: "init", "combined"

	# Initialize model
	model_path = f'models/crestereo_{version}_iter{iters}_{model_shape[0]}x{model_shape[1]}.onnx'
	depth_estimator = CREStereo(model_path)

	left_img_src = input("Left Image (URL or file path) : ")
	right_img_src = input("Right Image (URL or file path) : ")

	# Load images
	if 'https://' in left_img_src or 'http://' in left_img_src : 
		left_img = imread_from_url(left_img_src)
	else :
		left_img = cv2.imread(left_img_src)
	if 'https://' in right_img_src or 'http://' in right_img_src :
		right_img = imread_from_url(right_img_src)
	else :
		right_img = cv2.imread(right_img_src)

	# Estimate the depth
	disparity_map = depth_estimator(left_img, right_img)
	color_disparity = depth_estimator.draw_disparity()
	combined_image = np.hstack((left_img, color_disparity))

	cv2.imwrite("out_iter{0}.jpg".format(iters), combined_image)

	cv2.namedWindow("Estimated disparity", cv2.WINDOW_NORMAL)	
	cv2.imshow("Estimated disparity", combined_image)
	print("elapsed time",(datetime.now()-s).total_seconds())
	
	cv2.waitKey(0)

	cv2.destroyAllWindows()

if __name__ == "__main__" :
	main()
	