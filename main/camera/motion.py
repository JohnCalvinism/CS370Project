import cv2
import time
import os
import requests

def main():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    if not cap.isOpened(): 
        print("Error: Could not open camera.") 
        exit()

    print("Camera opened successfully. Press 'Esc' to exit.")

    prev_face = None
    prev_position = None
    face_counter = 0
    face_detected = False
    saved_images = []

    alert_url = "http://localhost:5000/alert" # Replace with the desktop/rasp pi IP address

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        current_face = None
        new_face_detected = False

        for (x, y, w, h) in faces:
            current_face = (x, y, w, h)

            if prev_face is None or abs(prev_face[0] - x) > 100 or abs(prev_face[1] - y) > 100:
                color = (0, 255, 0)
                prev_face = current_face
                prev_position = (x, y)
                face_counter += 1

                face_image = frame[y:y + h, x:x + w]
                face_filename = f"face_{face_counter}.jpg"
                full_filename = f"full_image_{face_counter}.jpg"
                
                cv2.imwrite(face_filename, face_image)
                cv2.imwrite(full_filename, frame)

                saved_images.append(face_filename)
                saved_images.append(full_filename)

                face_detected = True
                new_face_detected = True

                try: 
                    response = requests.post(alert_url, json={"alert": "Face detected", "face_id": face_counter}) 
                    print(f"Alert sent: {response.status_code}") 
                except Exception as e: 
                    print(f"Failed to send alert: {e}")

            else:
                if prev_position and (abs(prev_position[0] - x) > 5 or abs(prev_position[1] - y) > 5):
                    color = (0, 0, 255)
                else:
                    color = (255, 0, 0)

            prev_position = (x, y)

        if len(faces) == 0:
            prev_face = None

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        cv2.imshow('Face Detection', frame)

        key = cv2.waitKey(1)

        if key == 27:
            for img in saved_images:
                if os.path.exists(img):
                    os.remove(img)
                    print(f"Deleted: {img}")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
