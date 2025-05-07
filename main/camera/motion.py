import cv2
import time
import os
import uuid
import requests

def iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    xi1 = max(x1, x2)
    yi1 = max(y1, y2)
    xi2 = min(x1 + w1, x2 + w2)
    yi2 = min(y1 + h1, y2 + h2)
    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)

    box1_area = w1 * h1
    box2_area = w2 * h2
    union_area = box1_area + box2_area - inter_area

    return inter_area / union_area if union_area != 0 else 0

def main():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Camera opened successfully. Press 'Esc' to exit.")

    prev_position = None
    face_counter = 0
    seen_faces = []
    saved_images = []

    url = "http://192.168.68.52:5000/upload"  # Replace with server IP

    cv2.waitKey(500)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to read frame from camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            is_new_face = True
            color = (255, 0, 0)  # Default rectangle color: blue

            for (sx, sy, sw, sh) in seen_faces:
                if iou((x, y, w, h), (sx, sy, sw, sh)) > 0.5:
                    is_new_face = False
                    break

            if is_new_face:
                seen_faces.append((x, y, w, h))
                face_counter += 1
                color = (0, 255, 0)  # New face: green

                face_image = frame[y:y + h, x:x + w]
                unique_id = uuid.uuid4().hex
                face_filename = f"face_{unique_id}.jpg"
                full_filename = f"full_image_{unique_id}.jpg"

                cv2.imwrite(face_filename, face_image)
                cv2.imwrite(full_filename, frame)

                saved_images.extend([face_filename, full_filename])

                try:
                    with open(full_filename, 'rb') as f:
                        files = {'file': (full_filename, f, 'image/jpeg')}
                        response = requests.post(url, files=files, timeout=5)
                        print(f"Uploaded: {full_filename}, Response: {response.status_code}")

                    with open(face_filename, 'rb') as f:
                        files = {'file': (face_filename, f, 'image/jpeg')}
                        response = requests.post(url, files=files, timeout=5)
                        print(f"Uploaded: {face_filename}, Response: {response.status_code}")

                except Exception as e:
                    print(f"Failed to upload images: {e}")

            else:
                if prev_position and (abs(prev_position[0] - x) > 5 or abs(prev_position[1] - y) > 5):
                    color = (0, 0, 255)  # Movement detected: red

            prev_position = (x, y)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        if len(faces) == 0:
            prev_position = None

        cv2.imshow('Face Detection', frame)

        key = cv2.waitKey(1)
        if key == 27:  # Esc key
            print("Exiting and cleaning up...")
            for img in saved_images:
                if os.path.exists(img):
                    os.remove(img)
                    print(f"Deleted: {img}")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
