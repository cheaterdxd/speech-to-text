from flask import Flask, request, jsonify, send_from_directory
from faster_whisper import WhisperModel
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'ogg', 'flac', 'aac'}
MAX_FILE_SIZE = 300 * 1024 * 1024  # 300MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Whisper model
print("Loading Whisper model...")
model = WhisperModel("turbo", device="cpu", compute_type="int8")
print("Model loaded successfully!")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process audio
        print(f"Processing {filename}...")
        start_time = time.time()
        
        segments, info = model.transcribe(filepath, beam_size=5, language="vi")
        
        # Collect results
        results = []
        full_text = ""
        
        for segment in segments:
            segment_data = {
                'start': round(segment.start, 2),
                'end': round(segment.end, 2),
                'text': segment.text.strip()
            }
            results.append(segment_data)
            full_text += segment.text.strip() + " "
        
        processing_time = round(time.time() - start_time, 2)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'language': info.language,
            'language_probability': round(info.language_probability, 2),
            'segments': results,
            'full_text': full_text.strip(),
            'processing_time': processing_time
        })
    
    except Exception as e:
        # Clean up file if it exists
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True') == 'True'
    
    print("\n" + "="*50)
    print("🎙️  Speech-to-Text Web Server")
    print("="*50)
    print(f"Server running at: http://localhost:{port}")
    print("Press Ctrl+C to stop")
    print("="*50 + "\n")
    app.run(debug=debug, host='0.0.0.0', port=port)
