import cv2
import threading
from deepface import DeepFace

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0
face_match = False
reference_image_paths = [
    'images/het.jpeg',
    'images/het2.jpg',
    'images/het1.jpg'
]
reference_images = [cv2.imread(img_path) for img_path in reference_image_paths]


def check_face(frame):
    global face_match

    try:
        result = DeepFace.verify(frame, reference_images[0])
        if result['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        face_match = False


while True:
    ret, frame = cap.read()

    if not ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face,
                                 args=(frame,)).start()
            except ValueError:
                pass

            counter += 1

            if face_match:
                cv2.putText(frame, 'Face Matched', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, 'Face Not Matched', (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow('video', frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cv2.destroyAllWindows()
