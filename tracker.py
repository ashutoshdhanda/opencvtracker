# python 3.9.7
# opencv 4.5.3
# opencv-contrib-python 4.5.3
# Color blue for nuerona boxes
# Color green for tracker boxes


# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import pickle
import sys

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())

# initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations
OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.legacy.TrackerCSRT_create,
	"kcf": cv2.legacy.TrackerKCF_create,
	#"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.legacy.TrackerMIL_create,
	"goturn" : cv2.TrackerGOTURN
	#"tld": cv2.TrackerTLD_create,
	#"medianflow": cv2.TrackerMedianFlow_create,
	#"mosse": cv2.TrackerMOSSE_create
}
# initialize OpenCV's special multi-object tracker
trackers = cv2.legacy.MultiTracker_create()
videofile_name = args["video"]
full_string_size = len(videofile_name)
name_string = videofile_name[:full_string_size-4]
#print(name_string)
pickle_str = name_string+'.pkl'
detecciones=pickle.load(open(pickle_str,'rb'))


# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(1.0)
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])

# loop over frames from the video stream
while True:
	# grab the current frame, then handle if we are using a
	# VideoStream or VideoCapture object
	frame = vs.read()
	frame = frame[1] if args.get("video", False) else frame
	# check to see if we have reached the end of the stream
	if frame is None:
		break
	# resize the frame (so we can process it faster)
	frame = cv2.resize(frame, (416, 416),interpolation=cv2.INTER_LINEAR)

	# grab the updated bounding box coordinates (if any) for each
	# object that is being tracked
	(success, boxes) = trackers.update(frame)
	#print(type(boxes))
	#print(boxes)
	# loop over the bounding boxes and draw them on the frame
	for box in boxes:
		#print("drawing tracking box")
		(x, y, w, h) = [int(v) for v in box]
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

	#pop out the first detection from detections (poping is permanently reducing detections list size by 1)

	deteccionesctuales=detecciones.pop(0)


	if len(boxes)==0:
		if deteccionesctuales:
			for deteccionactual in deteccionesctuales:
				x=int(deteccionactual[2][0])
				y=int(deteccionactual[2][1])
				w=int(deteccionactual[2][2])
				h=int(deteccionactual[2][3])
				l = int((x - w / 2) )
				r = int((x + w / 2) )
				t = int((y - h / 2))
				b = int((y + h / 2))
				#print("drawing neurona box")
				#cv2.rectangle(frame,(l,t),(r,b),(0,0,255), 1)
				frame = cv2.resize(frame, (416, 416),interpolation=cv2.INTER_LINEAR)
				box1 = (l,t,r,b)
				tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
				trackers.add(tracker, frame, box1)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break
	#time.sleep(0.1)

if not args.get("video", False):
	vs.stop()
# otherwise, release the file pointer
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()

