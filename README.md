# 🎙️ Speech-to-Text Web Application

Ứng dụng web chuyển đổi file audio thành văn bản sử dụng AI (Faster Whisper).

## ✨ Tính năng

- 🎵 Hỗ trợ nhiều định dạng audio: MP3, WAV, M4A, OGG, FLAC, AAC
- 📤 Upload file lên đến 300MB
- 🌐 Nhận diện ngôn ngữ tự động (hỗ trợ tiếng Việt)
- ⏱️ Hiển thị kết quả với timestamp chi tiết
- 🎨 Giao diện hiện đại, dark mode
- 📋 Copy kết quả dễ dàng

## 🚀 Cài đặt Local

### Yêu cầu
- Python 3.8+
- pip

### Các bước

1. Clone repository:
```bash
git clone <your-repo-url>
cd speech-to-text
```

2. Tạo virtual environment:
```bash
python3 -m venv speechtotext
source speechtotext/bin/activate  # Linux/Mac
# hoặc
speechtotext\Scripts\activate  # Windows
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

4. Chạy ứng dụng:
```bash
python app.py
```

5. Mở trình duyệt tại: `http://localhost:5000`

## 🌐 Deploy lên Render.com

Xem hướng dẫn chi tiết trong file [DEPLOY.md](DEPLOY.md)

## 📝 Sử dụng

1. Truy cập web app
2. Kéo thả hoặc chọn file audio
3. Click "Transcribe Audio"
4. Xem kết quả với timestamp và full text

## 🛠️ Công nghệ

- **Backend**: Flask
- **AI Model**: Faster Whisper (turbo)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Render.com

## 📄 License

MIT License
