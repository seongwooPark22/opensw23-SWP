import cv2
import numpy as np
import yt_dlp
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
	left_vid_src = input("Left Video (URL or file path) : ")
	if 'https://' in left_vid_src or 'http://' in left_vid_src : 
		left_vid = cv2.VideoCapture(load_youtube_video(left_vid_src))
	else :
		left_vid = cv2.VideoCapture(left_vid_src)

	right_vid_src = input("Right Video (URL or file path) : ")

	if 'https://' in right_vid_src or 'http://' in right_vid_src : 
		right_vid = cv2.VideoCapture(load_youtube_video(right_vid_src))
	else :
		right_vid = cv2.VideoCapture(right_vid_src)
	
	# Model options (not all options supported together)
	iters = 10          # Lower iterations are faster, but will lower detail. 
						# Options: 2, 5, 10, 20 

	input_shape = (320, 480)   # Input resolution. 
						# Options: (240,320), (320,480), (380, 480), (360, 640), (480,640), (720, 1280)

	version = "combined" # The combined version does 2 passes, one to get an initial estimation and a second one to refine it.
						# Options: "init", "combined"
	max_distance = 10
	model_path = f'models/crestereo_{version}_iter{iters}_{input_shape[0]}x{input_shape[1]}.onnx'
	depth_estimator = CREStereo(model_path, max_dist = max_distance)

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