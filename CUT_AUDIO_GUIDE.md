# 🎵 Hướng dẫn sử dụng Script Cắt Audio

## Cài đặt

Script đã được tạo tại: `/home/letuan/code/speech-to-text/cut_audio.py`

Thư viện `pydub` đã được cài đặt sẵn.

## Cách sử dụng

### Cú pháp cơ bản

```bash
python cut_audio.py <input_file> <start_time> <end_time> [output_file]
```

### Tham số

- `input_file`: File audio đầu vào (mp3, wav, m4a, ogg, flac, ...)
- `start_time`: Thời điểm bắt đầu cắt (giây)
- `end_time`: Thời điểm kết thúc cắt (giây)
- `output_file`: File đầu ra (tùy chọn, nếu không có sẽ tự động tạo tên)

## Ví dụ

### 1. Cắt từ giây thứ 10 đến giây thứ 30

```bash
python cut_audio.py test.m4a 10 30
```

Output: `test_cut_10s-30s.m4a`

### 2. Cắt và đặt tên file output

```bash
python cut_audio.py test.m4a 10 30 intro.m4a
```

Output: `intro.m4a`

### 3. Cắt từ đầu đến giây thứ 15

```bash
python cut_audio.py audio.mp3 0 15
```

### 4. Cắt từ giây thứ 60 đến hết file

```bash
python cut_audio.py audio.mp3 60 999999
```

(Script sẽ tự động cắt đến hết file nếu thời gian > độ dài audio)

## Tính năng

✅ Hỗ trợ nhiều định dạng: MP3, WAV, M4A, OGG, FLAC, AAC, ...  
✅ Tự động kiểm tra file tồn tại  
✅ Tự động validate thời gian  
✅ Tự động tạo tên file output  
✅ Hiển thị thông tin chi tiết  

## Lưu ý

- Thời gian tính bằng **giây** (có thể dùng số thập phân: `10.5`)
- File output sẽ giữ nguyên định dạng của file input
- Nếu thời gian kết thúc > độ dài audio, sẽ tự động cắt đến hết file

## Test thử

```bash
# Activate virtual environment
source speechtotext/bin/activate

# Cắt file test.m4a từ 0-5 giây
python cut_audio.py test.m4a 0 5
```

Xong! 🎉
