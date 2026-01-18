from faster_whisper import WhisperModel
import time

# Cấu hình model
# Với 4GB VRAM, chúng ta dùng model "turbo" hoặc "medium" 
# compute_type="int8" giúp chạy mượt và tương thích tốt
model_size = "turbo" 

print(f"Đang tải model {model_size}...")
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Đường dẫn file audio của bạn (thay bằng tên file thật)
audio_file = "test.m4a"

print("Đang xử lý...")
start_time = time.time()

# beam_size=5 là mức cân bằng giữa tốc độ và độ chính xác
segments, info = model.transcribe(audio_file, beam_size=5, language="vi")

print(f"Phát hiện ngôn ngữ: {info.language} với xác suất {info.language_probability:.2f}")

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

end_time = time.time()
print(f"\nHoàn thành trong: {end_time - start_time:.2f} giây")