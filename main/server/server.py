import os
from flask import Flask, request, jsonify, render_template, send_from_directory, redirect
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
IMAGES_FOLDER = os.path.join(STATIC_DIR, 'images')

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')

os.makedirs(IMAGES_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER

image_filenames = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup():
    for filename in os.listdir(IMAGES_FOLDER):
        file_path = os.path.join(IMAGES_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"[DEBUG] Deleted: {file_path}")

@app.before_first_request
def before_first_request():
    cleanup()

@app.route('/')
def index():
    current_index = 0 if len(image_filenames) > 0 else -1
    return render_template('index.html', image_filenames=image_filenames, current_index=current_index)

@app.route('/image/<int:index>')
def view_image(index):
    if 0 <= index < len(image_filenames):
        return render_template('index.html', image_filenames=image_filenames, current_index=index)
    else:
        return redirect('/')

@app.route('/upload', methods=['POST'])
def upload():
    global image_filenames
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(IMAGES_FOLDER, filename)
        file.save(filepath)
        image_filenames.append(filename)
        print(f"[DEBUG] Saved: {filepath}") 
        return redirect('/')
    return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
