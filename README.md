# CS370Project

Devices
Logitech C920
Raspberry Pi 4
Windows Desktop

Logitech C920 records footage if it detects a change an imagine.
Devices PI Sends an alert to Desktop
Dekstop has an alert.


import cv2

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Draw rectangle around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        print("Face detected!")

    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(10) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
