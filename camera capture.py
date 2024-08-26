

import cv2

def test_camera(index):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Camera index {index} not available.")
    else:
        ret, frame = cap.read()
        if not ret:
            print(f"Camera index {index} could not read frames.")
        else:
            cv2.imshow(f'Camera {index}', frame)
            print(f"Camera index {index} is available.")
            cv2.waitKey(1000)  # Show the frame for 1 second
        cap.release()

# Check camera indices from 0 to 5
for i in range(6):
    test_camera(i)

cv2.destroyAllWindows()
