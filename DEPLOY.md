# 🚀 Hướng dẫn Deploy lên Render.com

## Bước 1: Chuẩn bị GitHub Repository

### 1.1. Khởi tạo Git (nếu chưa có)
```bash
cd /home/letuan/code/speech-to-text
git init
git add .
git commit -m "Initial commit: Speech-to-Text web app"
```

### 1.2. Tạo repository trên GitHub
1. Truy cập https://github.com/new
2. Đặt tên repository: `speech-to-text` (hoặc tên bạn muốn)
3. Chọn **Public** hoặc **Private**
4. **KHÔNG** chọn "Initialize with README" (vì đã có sẵn)
5. Click **Create repository**

### 1.3. Push code lên GitHub
```bash
# Thay <your-username> bằng username GitHub của bạn
git remote add origin https://github.com/<your-username>/speech-to-text.git
git branch -M main
git push -u origin main
```

---

## Bước 2: Deploy lên Render.com

### 2.1. Tạo tài khoản Render
1. Truy cập https://render.com
2. Click **Get Started** hoặc **Sign Up**
3. Đăng ký bằng GitHub account (khuyến nghị) hoặc email

### 2.2. Tạo Web Service mới

1. Sau khi đăng nhập, click **New +** → **Web Service**

2. **Connect GitHub Repository**:
   - Click **Connect account** nếu chưa kết nối GitHub
   - Cho phép Render truy cập repositories
   - Tìm và chọn repository `speech-to-text` của bạn

3. **Cấu hình Web Service**:
   
   | Trường | Giá trị |
   |--------|---------|
   | **Name** | `speech-to-text` (hoặc tên bạn muốn) |
   | **Region** | Singapore (gần Việt Nam nhất) |
   | **Branch** | `main` |
   | **Root Directory** | (để trống) |
   | **Runtime** | `Python 3` |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `gunicorn app:app` |
   | **Instance Type** | **Free** |

4. **Environment Variables** (Tùy chọn):
   - Click **Add Environment Variable**
   - Thêm: `DEBUG` = `False` (để tắt debug mode ở production)

5. Click **Create Web Service**

### 2.3. Đợi Deploy

- Render sẽ tự động:
  - Clone repository
  - Cài đặt dependencies
  - Tải Whisper model (~2-3GB)
  - Khởi động server

- **Thời gian deploy lần đầu**: 10-15 phút (do phải tải model)
- Theo dõi logs để xem tiến trình

### 2.4. Truy cập ứng dụng

Sau khi deploy thành công:
- URL sẽ có dạng: `https://speech-to-text-xxxx.onrender.com`
- Click vào URL để mở ứng dụng

---

## ⚠️ Lưu ý quan trọng

### 1. **Free Tier Limitations**
- Server sẽ **sleep sau 15 phút không hoạt động**
- Lần truy cập đầu tiên sau khi sleep sẽ mất ~30-60 giây để wake up
- Giới hạn 750 giờ/tháng (đủ dùng cho project cá nhân)

### 2. **Model Size**
- Whisper turbo model ~2-3GB
- Render free tier có 512MB RAM → có thể gặp vấn đề
- **Giải pháp**: Nâng cấp lên paid plan ($7/tháng) hoặc dùng model nhỏ hơn

### 3. **Thay đổi model nếu cần**
Nếu gặp lỗi memory, sửa trong `app.py`:
```python
# Thay vì turbo
model = WhisperModel("turbo", device="cpu", compute_type="int8")

# Dùng base (nhẹ hơn)
model = WhisperModel("base", device="cpu", compute_type="int8")
```

---

## 🔄 Update ứng dụng

Mỗi khi bạn thay đổi code:

```bash
git add .
git commit -m "Mô tả thay đổi"
git push
```

Render sẽ **tự động deploy lại** khi phát hiện commit mới!

---

## 🆘 Troubleshooting

### Lỗi: "Out of memory"
- Nâng cấp lên paid plan
- Hoặc dùng model nhỏ hơn (base thay vì turbo)

### Deploy quá lâu
- Lần đầu phải tải model (~10-15 phút)
- Lần sau sẽ nhanh hơn (~2-3 phút)

### Server sleep
- Đây là hành vi bình thường của free tier
- Nâng cấp lên paid để server chạy 24/7

---

## 💰 Chi phí

- **Free tier**: $0/tháng
  - 750 giờ/tháng
  - 512MB RAM (có thể không đủ cho turbo model)
  - Server sleep sau 15 phút

- **Starter plan**: $7/tháng
  - Server chạy 24/7
  - 512MB RAM
  - Không giới hạn giờ

- **Standard plan**: $25/tháng
  - 2GB RAM (đủ cho turbo model)
  - Server chạy 24/7

---

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Xem logs trên Render dashboard
2. Kiểm tra GitHub repository đã push đầy đủ
3. Đọc Render docs: https://render.com/docs

Chúc bạn deploy thành công! 🎉
