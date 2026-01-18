#!/usr/bin/env python3
"""
Script benchmark để test hiệu năng với các cấu hình khác nhau
"""

from faster_whisper import WhisperModel
from pydub import AudioSegment
import time
import os
import sys

def preprocess_audio(input_path):
    """Tiền xử lý audio: convert to 16kHz mono WAV"""
    print(f"📂 Preprocessing {input_path}...")
    audio = AudioSegment.from_file(input_path)
    
    # Convert to mono
    audio = audio.set_channels(1)
    
    # Downsample to 16kHz
    audio = audio.set_frame_rate(16000)
    
    # Normalize
    audio = audio.normalize()
    
    # Export to WAV
    output_path = "temp_preprocessed.wav"
    audio.export(output_path, format="wav")
    
    print(f"✅ Preprocessed: {os.path.getsize(output_path) / 1024 / 1024:.2f}MB")
    return output_path

def benchmark_config(audio_path, config_name, model_size, device, compute_type, 
                     beam_size, vad_filter, use_preprocessing):
    """Test một cấu hình cụ thể"""
    print(f"\n{'='*60}")
    print(f"🧪 Testing: {config_name}")
    print(f"{'='*60}")
    
    # Preprocessing nếu cần
    if use_preprocessing:
        processed_path = preprocess_audio(audio_path)
    else:
        processed_path = audio_path
    
    # Load model
    print(f"📥 Loading model: {model_size} ({device}, {compute_type})...")
    model_load_start = time.time()
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    model_load_time = time.time() - model_load_start
    print(f"✅ Model loaded in {model_load_time:.2f}s")
    
    # Transcribe
    print(f"🎙️  Transcribing (beam_size={beam_size}, VAD={vad_filter})...")
    transcribe_start = time.time()
    
    if vad_filter:
        segments, info = model.transcribe(
            processed_path,
            beam_size=beam_size,
            language="vi",
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )
    else:
        segments, info = model.transcribe(
            processed_path,
            beam_size=beam_size,
            language="vi"
        )
    
    # Collect results
    segment_count = 0
    total_text = ""
    for segment in segments:
        segment_count += 1
        total_text += segment.text.strip() + " "
    
    transcribe_time = time.time() - transcribe_start
    
    # Cleanup
    if use_preprocessing and os.path.exists(processed_path):
        os.remove(processed_path)
    
    # Results
    print(f"\n📊 Results:")
    print(f"   Language: {info.language} ({info.language_probability:.2%})")
    print(f"   Segments: {segment_count}")
    print(f"   Text length: {len(total_text)} chars")
    print(f"   ⏱️  Transcribe time: {transcribe_time:.2f}s")
    print(f"   Total time: {model_load_time + transcribe_time:.2f}s")
    
    return {
        'config': config_name,
        'model_load_time': model_load_time,
        'transcribe_time': transcribe_time,
        'total_time': model_load_time + transcribe_time,
        'segments': segment_count,
        'text_length': len(total_text)
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python benchmark.py <audio_file>")
        print("Example: python benchmark.py test_30p.mp3")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    if not os.path.exists(audio_file):
        print(f"❌ File not found: {audio_file}")
        sys.exit(1)
    
    file_size = os.path.getsize(audio_file) / 1024 / 1024
    print(f"\n🎵 Audio file: {audio_file}")
    print(f"📦 Size: {file_size:.2f}MB")
    
    results = []
    
    # Config 1: Baseline (current)
    results.append(benchmark_config(
        audio_file,
        "Baseline (turbo, no VAD, no preprocessing)",
        model_size="turbo",
        device="cpu",
        compute_type="int8",
        beam_size=5,
        vad_filter=False,
        use_preprocessing=False
    ))
    
    # Config 2: With VAD
    results.append(benchmark_config(
        audio_file,
        "With VAD (turbo + VAD)",
        model_size="turbo",
        device="cpu",
        compute_type="int8",
        beam_size=5,
        vad_filter=True,
        use_preprocessing=False
    ))
    
    # Config 3: With Preprocessing
    results.append(benchmark_config(
        audio_file,
        "With Preprocessing (turbo + preprocessing)",
        model_size="turbo",
        device="cpu",
        compute_type="int8",
        beam_size=5,
        vad_filter=False,
        use_preprocessing=True
    ))
    
    # Config 4: VAD + Preprocessing (RECOMMENDED)
    results.append(benchmark_config(
        audio_file,
        "VAD + Preprocessing (RECOMMENDED)",
        model_size="turbo",
        device="cpu",
        compute_type="int8",
        beam_size=5,
        vad_filter=True,
        use_preprocessing=True
    ))
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📈 BENCHMARK SUMMARY")
    print(f"{'='*60}\n")
    
    baseline_time = results[0]['transcribe_time']
    
    print(f"{'Config':<45} {'Time':<10} {'Speedup':<10}")
    print(f"{'-'*60}")
    
    for result in results:
        speedup = baseline_time / result['transcribe_time']
        print(f"{result['config']:<45} {result['transcribe_time']:>6.2f}s   {speedup:>5.2f}x")
    
    print(f"\n🏆 Best config: {min(results, key=lambda x: x['transcribe_time'])['config']}")
    print(f"⚡ Max speedup: {max(results, key=lambda x: baseline_time / x['transcribe_time'])['config']}")

if __name__ == "__main__":
    main()
