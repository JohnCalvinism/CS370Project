Setup Virtual Environment

Source venv/bin/activate

pip freeze > requirements.txt

pip install -r requirements.txt

saving for now... will delete

from flask import Flask, request

app = Flask(__name__)

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    print("Alert received:", data)
    # Add code to display a notification or log the event
    return "Alert received", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

requirements.txt
requests==2.26.0
flask==2.0.1

motion.py
if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    print("Camera opened successfully. Press 'Esc' to exit.")

    alert_url = "http://<desktop_or_pi_ip>:5000/alert" # Replace with the desktop/rasp pi IP address
    
try:
                    response = requests.post(alert_url, json={"alert": "Face detected", "face_id": face_counter})
                    print(f"Alert sent: {response.status_code}")
                except Exception as e:
                    print(f"Failed to send alert: {e}")
