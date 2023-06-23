import cv2
import numpy as np

# Define the tracker class
class CentroidTracker:
    def __init__(self, max_disappeared=50):
        self.next_object_id = 0
        self.objects = {}
        self.disappeared = {}
        self.max_disappeared = max_disappeared

    def register(self, centroid):
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, centroids):
        if len(centroids) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1

                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)

            return self.objects

        new_object_ids = list(self.objects.keys())
        new_centroids = list(self.objects.values())

        for centroid in centroids:
            distances = []
            for obj_centroid in new_centroids:
                distances.append(self.distance(centroid, obj_centroid))

            min_distance = min(distances)
            obj_id = new_object_ids[distances.index(min_distance)]

            self.objects[obj_id] = centroid
            self.disappeared[obj_id] = 0

            new_object_ids.remove(obj_id)
            new_centroids.remove(centroid)

        for object_id in new_object_ids:
            self.disappeared[object_id] += 1

            if self.disappeared[object_id] > self.max_disappeared:
                self.deregister(object_id)

        return self.objects

    @staticmethod
    def distance(a, b):
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


# Open video file or camera stream
video_path = 'videoProvaLancio.mp4'  # Set to 0 for live camera feed
cap = cv2.VideoCapture(0)

# Initialize the centroid tracker
tracker = CentroidTracker()

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (320, 240))

    if not ret:
        break

    # Perform object detection on the frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Threshold of blue in HSV space
    
    lower_blue = np.array([120, 120, 0])
    upper_blue = np.array([255, 255, 255])
        # preparing the mask to overlay
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
        # The black region in the mask has the value of 0,
        # so when multiplied with original image removes all non-blue regions
    result = cv2.bitwise_and(frame, frame, mask = mask)
      #  cv2.imshow('frame', frame)
      #  cv2.imshow('mask', mask)
    #result = cv2.resize(result, (0,0), fx= 0.5, fy=0.5)
    result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    cv2.imshow(" ", result)
    #frame_gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    (thresh, img_m) = cv2.threshold(result, 127, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(img_m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  
    items = sorted(contours, key=cv2.contourArea, reverse= False) #sorting degli elementi


    item = items[-1]
    print(cv2.contourArea(item))
    x,y,w,h= cv2.boundingRect(item)
    cX = int((x+(x+w))/2)
    cY = int((y+(y+h))/2)

    # Extract object centroids from the detection results
    centroids = []
    # ... Your code to extract centroids here ...
    centroids.append((cX, cY))
    # Update the centroid tracker
    tracked_objects = tracker.update(centroids)

    # Draw bounding boxes and object IDs on the frame
    for object_id, centroid in tracked_objects.items():
        x, y = centroid
        cv2.circle(frame, (int(x), int(y)), 4, (0, 255, 0), -1)
        cv2.putText(frame, str(object_id), (int(x) - 10, int(y) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Display the frame
    cv2.imshow('Rocket Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()
