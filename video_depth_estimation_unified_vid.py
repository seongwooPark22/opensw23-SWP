import cv2
import yt_dlp
import numpy as np
import glob
from crestereo import CREStereo, CameraConfig

def load_youtube_video(URL):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(URL, download=False)
        
    vlist = []
    for f in info['formats'][::-1] :
        if f['vcodec'] != 'none' :
            if f['format_note'] in ['144p', '360p', '720p', '1080p']:
                vlist.append(f['url'])
    return vlist[0]

def main() : 
	# Initialize video
	# cap = cv2.VideoCapture("video.mp4")
	videoPath = input("Stereo Video (URL or file path) : ")
	swap_side = input("Swap left and right(y/n) : ")
	
	if 'https://' in videoPath or 'http://' in videoPath : 
		cap = cv2.VideoCapture(load_youtube_video(videoPath))
	else :
		cap = cv2.VideoCapture(videoPath)

	start_time = 0 # skip first {start_time} seconds
	
	cap.set(cv2.CAP_PROP_POS_FRAMES, start_time*30)

	# Model options (not all options supported together)
	iters = 5            # Lower iterations are faster, but will lower detail. 
						# Options: 2, 5, 10, 20 

	input_shape = (320, 480)   # Input resolution. 
						# Options: (240,320), (320,480), (380, 480), (360, 640), (480,640), (720, 1280)

	version = "combined" # The combined version does 2 passes, one to get an initial estimation and a second one to refine it.
						# Options: "init", "combined"

	# Camera options: baseline (m), focal length (pixel) and max distance
	# TODO: Fix with the values witht the correct configuration for YOUR CAMERA
	camera_config = CameraConfig(0.12, 0.5*input_shape[1]/0.72) 
	max_distance = 10

	# Initialize model
	model_path = f'models/crestereo_{version}_iter{iters}_{input_shape[0]}x{input_shape[1]}.onnx'
	depth_estimator = CREStereo(model_path, camera_config=camera_config, max_dist=max_distance)

	cv2.namedWindow("Estimated depth", cv2.WINDOW_NORMAL)	
	while cap.isOpened():

		try:
			# Read frame from the video
			ret, frame = cap.read()
			if not ret:	
				break
		except:
			continue

		# Extract the left and right images
		fs = frame.shape[1]//2
		left_img  = frame[:,:fs]
		right_img = frame[:,fs:fs*2]

		# Estimate the depth
		if swap_side == 'y' :
			left_img, right_img = right_img, left_img
		
		disparity_map = depth_estimator(left_img, right_img)
		color_depth = depth_estimator.draw_depth()
		combined_image = np.hstack((left_img, color_depth))

		cv2.imshow("Estimated depth", combined_image)

		# Press key q to stop
		if cv2.waitKey(1) == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

if __name__ == "__main__" :
	main()