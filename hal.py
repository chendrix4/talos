import cv2
import argparse
import sys

"""
Theory of Operation

Detection
    - Gives initial bounding box
    - Determines if no target found
    - Can still run on its own if tracker is failing
Tracking
    - Takes bounding box from detector and tracks
    - Can run on its own if detector is failing
        - As long as it is successful, continues to run without detector
"""

# Command line argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("tracker", help="KCF, TLD, Boosting, MedianFlow, MIL, GOTURN",
                               type=str,
                               default="KCF")
parser.add_argument("-f", help="xml file for detection trainer",
                          default="haarcascade_frontalface_default.xml")
parser.add_argument("-v", help="Show video",
                          action="store_true")
args = parser.parse_args()

# Instantiate tracker, detection and camera
tracker = None
haar = cv2.CascadeClassifier('lib/python3.6/site-packages/cv2/data/' + args.f)
cam  = cv2.VideoCapture(0)

# Operational error handling
MAX_MISSED = 10
missed_detections = 0
failed_track = False
x=0; y=0; w=0; h=0;

while 1:
    
    # Get next frame
    ret, frame = cam.read()
    if not ret:
        break

    # Detection - must run first
    # This determines initial target location as well as
    # prevents stationary targets from staying "hidden"
    faces = haar.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                                  scaleFactor=1.1,
                                  minNeighbors=5)

    # Get targets
    # If faces found and not already tracking, get location
    # If no faces found, there may be no one in frame (missed += 1)
    if len(faces) > 0 and not tracking:
        x,y,w,h = faces[0]
        missed_detections = 0
    else:
        missed_detections += 1

    cv2.waitKey(1)

    # Show frame over target
    # Green for found target, Red if no target found
    if args.v:
        frame_color = (0,
                       255*(missed_detections < MAX_MISSED),
                       255*(missed_detections >= MAX_MISSED))
        cv2.rectangle(frame, (x,y), (x+w,y+h), frame_color, 2)
        cv2.imshow('', frame)

    # Run another detection scan if missed MAX_MISSED times
    if missed_detections >= MAX_MISSED:
        continue
    
    # Config tracker
    target = (x,y,w,h)
    if tracker == None:
        tracker = getattr(cv2, f'Tracker{args.tracker}_create')()
        tracker.init(frame, target)

    # Track for 10 frames
    for f in range(10):

        _, frame = cam.read()
        tracking, target = tracker.update(frame)
        if not tracking:
            break
        
        # draw new frame
        x,y,w,h = list(map(int,bbox))
        center = (int(x+w/2),int(y+h/2))
        if args.v:
            cv2.rectangle(frame,
                          (x,y), (x+w,y+h),
                          (0, 255*(missed < MAX_MISSED), 255*(missed >= MAX_MISSED)),
                          2)
            cv2.imshow('',frame)

        cv2.waitKey(1)
    
cam.release()
cv2.destroyAllWindows()
