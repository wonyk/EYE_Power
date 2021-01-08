import cv2
import numpy as np
import time
from concurrent_videocapture import ConcurrentVideoCapture

# Credits for openCV documentation
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
params = cv2.SimpleBlobDetector_Params()

# change params settings t0 use size as a filter
# Might add other filters such as color or circular too.
params.maxArea = 1500
params.filterByArea = True
detector = cv2.SimpleBlobDetector_create(params)


def start():
    # im = cv2.imread('face1.jpg')
    # img = cv2.resize(im, (720, 960))
    cap = ConcurrentVideoCapture(0)
    # cap = cv2.VideoCapture(0)
    cv2.namedWindow('image')
    threshold_value = 65
    cv2.createTrackbar('threshold', 'image', threshold_value, 255, nothing)

    while True:
        init = time.time()
        _, frame = cap.read()
        face = detect_faces(frame, face_cascade)
        if face is not None:
            # Then proceed to look for eyes
            # The function will return left eye and right eye irregardless of whether it can
            # detect or not. So we will handle the errors later
            eyes = detect_eyes(face, eye_cascade)
            # print(eyes)
            # left and right parsed separately
            for eye in eyes:
                if eye is not None:
                    threshold_value = cv2.getTrackbarPos(
                        'threshold', 'image')
                    eye = remove_others(eye)
                    kp = process_eye_using_blob(eye, threshold_value, detector)
                    # print(kp)
                    eye = cv2.drawKeypoints(
                        eye, kp, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        cv2.imshow('image', frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break
        fps = 1/(time.time() - init)
        print('Fps: {}'.format(fps))
    cap.release()
    cv2.destroyAllWindows()


def nothing(x):
    pass


def detect_faces(img, cascade):
    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_coord = cascade.detectMultiScale(grey_img, 1.3, 5)
    # The coords are in (x, y, w, h) where x and y are the coordinates and
    # w and h are the width and height of the identifed face respectively

    # Handle multiple faces by selecting the largest one
    if len(face_coord) > 1:
        largest = [0, 0, 0, 0]
        for coord in face_coord:
            # The 3rd index is the width
            if (coord[3] > largest[3]):
                largest = coord.copy()
        # Convert i to a 2D np array for further processing
        largest = np.array([largest], np.int64)
    elif len(face_coord) == 1:
        largest = face_coord
    else:
        return None
    for (x, y, w, h) in largest:
        # print(x, y)
        return img[y:y + h, x:x + w]
        # return grey_img[y:y + h, x:x + w]


def detect_eyes(img, cascade):
    # Using the default values recommended in the OpenCV tutorial
    grey_face = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = cascade.detectMultiScale(grey_face, 1.3, 5)
    height, width, channels = img.shape
    left = None
    right = None

    for (x, y, w, h) in eyes:
        # Remove falsely identified eyes below half the face...
        if y > height / 2:
            pass
        # Determine left and right side using the width of face...
        elif x + w < width / 2:
            left = img[y:y + h, x:x + w]
        else:
            right = img[y:y + h, x:x + w]
    return left, right


def remove_others(img):
    height, width, channels = img.shape
    other = int(height / 5)
    img = img[other:height-other, 0:width]
    return img


def process_eye_using_blob(img, threshold_value, detector):
    _, img = cv2.threshold(
        img, threshold_value, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=4)
    img = cv2.medianBlur(img, 5)
    kp = detector.detect(img)
    return kp


start()
