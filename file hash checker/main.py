from flask import Flask, request, jsonify, render_template
import hashlib
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="templates", static_folder="static")

# Directory to save uploaded files (optional)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML file

@app.route('/check', methods=['POST'])
def check_file():
    if 'file' not in request.files or 'hash' not in request.form:
        return jsonify({'error': 'Missing file or hash'}), 400

    uploaded_file = request.files['file']
    provided_hash = request.form['hash']

    # Save the uploaded file (optional)
    filename = secure_filename(uploaded_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(filepath)

    # Calculate SHA-256 hash of the file
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    calculated_hash = sha256_hash.hexdigest()

    # Compare hashes
    is_authentic = (calculated_hash == provided_hash)

    # Optionally delete the file after checking
    os.remove(filepath)

    return jsonify({'isAuthentic': is_authentic, 'calculatedHash': calculated_hash})

if __name__ == '__main__':
    app.run(debug=True)
