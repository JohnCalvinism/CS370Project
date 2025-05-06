from flask import Flask, request

app = Flask(__name__)

@app.route('/alert', methods=['POST']) 

def alert(): 
    data = request.json 
    print("Alert received:", data) # Add code to display a notification or log the event return "Alert received", 200
    return "Alert received", 200

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000)

