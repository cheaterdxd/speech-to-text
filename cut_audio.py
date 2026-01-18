#!/usr/bin/env python3
"""
Script đơn giản để cắt file audio theo số giây mong muốn
Sử dụng: python cut_audio.py <input_file> <start_time> <end_time> [output_file]
"""

import sys
import os
from pydub import AudioSegment

def cut_audio(input_file, start_seconds, end_seconds, output_file=None):
    """
    Cắt file audio từ start_seconds đến end_seconds
    
    Args:
        input_file: Đường dẫn file audio đầu vào
        start_seconds: Thời điểm bắt đầu (giây)
        end_seconds: Thời điểm kết thúc (giây)
        output_file: Đường dẫn file đầu ra (tùy chọn)
    """
    # Kiểm tra file tồn tại
    if not os.path.exists(input_file):
        print(f"❌ Lỗi: File '{input_file}' không tồn tại!")
        return False
    
    # Tạo tên file output nếu không được cung cấp
    if output_file is None:
        name, ext = os.path.splitext(input_file)
        output_file = f"{name}_cut_{start_seconds}s-{end_seconds}s{ext}"
    
    try:
        print(f"📂 Đang đọc file: {input_file}")
        
        # Load audio file
        audio = AudioSegment.from_file(input_file)
        duration = len(audio) / 1000  # Convert to seconds
        
        print(f"⏱️  Độ dài audio: {duration:.2f} giây")
        
        # Validate thời gian
        if start_seconds < 0:
            print("❌ Lỗi: Thời gian bắt đầu phải >= 0")
            return False
        
        if end_seconds > duration:
            print(f"⚠️  Cảnh báo: Thời gian kết thúc ({end_seconds}s) > độ dài audio ({duration:.2f}s)")
            print(f"    Sẽ cắt đến hết file")
            end_seconds = duration
        
        if start_seconds >= end_seconds:
            print("❌ Lỗi: Thời gian bắt đầu phải < thời gian kết thúc")
            return False
        
        # Cắt audio (pydub sử dụng milliseconds)
        start_ms = start_seconds * 1000
        end_ms = end_seconds * 1000
        
        print(f"✂️  Đang cắt từ {start_seconds}s đến {end_seconds}s...")
        cut_audio_segment = audio[start_ms:end_ms]
        
        # Xuất file
        print(f"💾 Đang lưu file: {output_file}")
        
        # Xác định format để export
        file_ext = output_file.split('.')[-1].lower()
        export_format = file_ext
        
        # m4a cần dùng mp4 container
        if file_ext == 'm4a':
            export_format = 'mp4'
        
        cut_audio_segment.export(output_file, format=export_format)
        
        cut_duration = len(cut_audio_segment) / 1000
        print(f"✅ Hoàn thành! Độ dài đoạn cắt: {cut_duration:.2f} giây")
        print(f"📁 File đã lưu: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        return False

def main():
    # Hiển thị hướng dẫn
    if len(sys.argv) < 4:
        print("🎵 Script cắt audio")
        print("\nCách sử dụng:")
        print("  python cut_audio.py <input_file> <start_time> <end_time> [output_file]")
        print("\nVí dụ:")
        print("  python cut_audio.py audio.mp3 10 30")
        print("  python cut_audio.py audio.mp3 10 30 output.mp3")
        print("\nTham số:")
        print("  input_file  : File audio đầu vào (mp3, wav, m4a, ...)")
        print("  start_time  : Thời điểm bắt đầu (giây)")
        print("  end_time    : Thời điểm kết thúc (giây)")
        print("  output_file : File đầu ra (tùy chọn)")
        sys.exit(1)
    
    # Lấy tham số
    input_file = sys.argv[1]
    
    try:
        start_time = float(sys.argv[2])
        end_time = float(sys.argv[3])
    except ValueError:
        print("❌ Lỗi: Thời gian phải là số!")
        sys.exit(1)
    
    output_file = sys.argv[4] if len(sys.argv) > 4 else None
    
    # Thực hiện cắt
    success = cut_audio(input_file, start_time, end_time, output_file)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
