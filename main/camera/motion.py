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

    prev_position = None
    face_counter = 0
    seen_faces = []
    saved_images = []

    url = "http://192.168.68.52:5000/upload"  # Desktop IP
    cv2.waitKey(500)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            current_face = (x, y, w, h)
            is_new_face = True
            color = (255, 0, 0)  # Default to blue

            for (sx, sy, sw, sh) in seen_faces:
                if abs(sx - x) < 50 and abs(sy - y) < 50:
                    is_new_face = False
                    break

            if is_new_face:
                seen_faces.append((x, y, w, h))
                face_counter += 1
                color = (0, 255, 0)  # Green for new face

                face_image = frame[y:y + h, x:x + w]
                face_filename = f"face_{face_counter}.jpg"
                full_filename = f"full_image_{face_counter}.jpg"

                cv2.imwrite(face_filename, face_image)
                cv2.imwrite(full_filename, frame)

                saved_images.append(face_filename)
                saved_images.append(full_filename)

                try:
                    with open(full_filename, 'rb') as f:
                        files = {'file': (full_filename, f, 'image/jpeg')}
                        response = requests.post(url, files=files)
                        if response.status_code == 200:
                            print("Image uploaded successfully!")
                except Exception as e:
                    print(f"Failed to send alert: {e}")
            else:
                if prev_position and (abs(prev_position[0] - x) > 5 or abs(prev_position[1] - y) > 5):
                    color = (0, 0, 255)  
                else:
                    color = (255, 0, 0) 

            prev_position = (x, y)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        if len(faces) == 0:
            prev_position = None

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
