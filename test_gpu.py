#!/usr/bin/env python3
"""
Quick test script để kiểm tra GPU hoạt động với Whisper
"""

from faster_whisper import WhisperModel
import time
import sys

def test_gpu():
    print("="*60)
    print("🧪 Testing GPU with Faster Whisper")
    print("="*60)
    
    # Check CUDA
    try:
        import torch
        print(f"\n✅ PyTorch installed")
        print(f"   CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
            print(f"   CUDA version: {torch.version.cuda}")
    except ImportError:
        print("❌ PyTorch not installed")
        return
    
    if not torch.cuda.is_available():
        print("\n❌ CUDA not available, cannot test GPU")
        return
    
    # Test với file audio
    if len(sys.argv) < 2:
        print("\n⚠️  No audio file provided")
        print("Usage: python test_gpu.py <audio_file>")
        return
    
    audio_file = sys.argv[1]
    
    # Test CPU
    print(f"\n{'='*60}")
    print("🖥️  Testing CPU (turbo model)")
    print("="*60)
    
    model_cpu = WhisperModel("turbo", device="cpu", compute_type="int8")
    
    start = time.time()
    segments_cpu, info_cpu = model_cpu.transcribe(audio_file, beam_size=5, language="vi")
    cpu_time = time.time() - start
    
    cpu_segments = list(segments_cpu)
    print(f"✅ CPU done in {cpu_time:.2f}s")
    print(f"   Segments: {len(cpu_segments)}")
    
    # Test GPU
    print(f"\n{'='*60}")
    print("🎮 Testing GPU (small model)")
    print("="*60)
    
    model_gpu = WhisperModel("small", device="cuda", compute_type="int8")
    
    start = time.time()
    segments_gpu, info_gpu = model_gpu.transcribe(audio_file, beam_size=5, language="vi")
    gpu_time = time.time() - start
    
    gpu_segments = list(segments_gpu)
    print(f"✅ GPU done in {gpu_time:.2f}s")
    print(f"   Segments: {len(gpu_segments)}")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 RESULTS")
    print("="*60)
    print(f"CPU time: {cpu_time:.2f}s")
    print(f"GPU time: {gpu_time:.2f}s")
    print(f"Speedup: {cpu_time/gpu_time:.2f}x")
    print(f"\n🏆 GPU is {cpu_time/gpu_time:.2f}x faster!")

if __name__ == "__main__":
    test_gpu()
