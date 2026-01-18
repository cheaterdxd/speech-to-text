from flask import Flask, request, jsonify, send_from_directory
from faster_whisper import WhisperModel
from pydub import AudioSegment
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
# Thử sử dụng GPU với model "turbo" (theo yêu cầu)
# Nếu hết VRAM (4GB có thể không đủ), sẽ tự động fallback về CPU
try:
    import torch
    if torch.cuda.is_available():
        print(f"✅ GPU detected: {torch.cuda.get_device_name(0)}")
        try:
            # Thử load turbo trên GPU
            model = WhisperModel("turbo", device="cuda", compute_type="int8")
            print("✅ Model TURBO loaded on GPU!")
        except Exception as gpu_error:
            print(f"⚠️  GPU VRAM insufficient for turbo ({gpu_error})")
            print("   Fallback to CPU with turbo model...")
            model = WhisperModel("turbo", device="cpu", compute_type="int8")
            print("✅ Model TURBO loaded on CPU")
    else:
        print("⚠️  No GPU detected, using CPU")
        model = WhisperModel("turbo", device="cpu", compute_type="int8")
        print("✅ Model TURBO loaded on CPU")
except Exception as e:
    print(f"⚠️  Error: {e}, fallback to CPU")
    model = WhisperModel("turbo", device="cpu", compute_type="int8")
    print("✅ Model TURBO loaded on CPU (fallback)")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_audio(input_path):
    """Tiền xử lý audio: convert to 16kHz mono WAV để tối ưu tốc độ"""
    try:
        audio = AudioSegment.from_file(input_path)
        
        # Convert to mono (giảm 50% dữ liệu)
        audio = audio.set_channels(1)
        
        # Downsample to 16kHz (Whisper chỉ cần 16kHz)
        audio = audio.set_frame_rate(16000)
        
        # Normalize volume
        audio = audio.normalize()
        
        # Export to WAV
        output_path = input_path.rsplit('.', 1)[0] + '_preprocessed.wav'
        audio.export(output_path, format="wav")
        
        return output_path
    except Exception as e:
        print(f"Preprocessing warning: {str(e)}")
        return input_path  # Fallback to original if preprocessing fails

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    import uuid
    filepath = None
    
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
        
        # Tạo tên file unique với UUID để tránh conflict
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}_{int(time.time())}.{file_extension}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save file
        file.save(filepath)
        
        # Preprocess audio (phương án 6: tối ưu hóa)
        print(f"Preprocessing {original_filename}...")
        preprocessed_path = preprocess_audio(filepath)
        
        # Process audio
        print(f"Transcribing {original_filename}...")
        start_time = time.time()
        
        # Phương án 3: Bật VAD filter để skip im lặng
        segments, info = model.transcribe(
            preprocessed_path,
            beam_size=5,
            language="vi",
            vad_filter=True,  # Bật VAD
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        
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
        
        # Clean up files
        if preprocessed_path != filepath and os.path.exists(preprocessed_path):
            os.remove(preprocessed_path)
        if filepath and os.path.exists(filepath):
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
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass
        
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🎙️  Speech-to-Text Web Server")
    print("="*50)
    print("Server running at: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
