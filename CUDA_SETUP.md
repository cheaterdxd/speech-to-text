# 🎮 Hướng dẫn cài đặt CUDA cho GTX 1050 Ti

## 📋 Thông tin GPU

**NVIDIA GTX 1050 Ti**:
- Compute Capability: **6.1** (Pascal architecture)
- CUDA Cores: 768
- VRAM: 4GB GDDR5
- Hỗ trợ CUDA: 8.0 - 12.x

## ✅ Phiên bản CUDA khuyến nghị

Cho GTX 1050 Ti, các phiên bản tốt nhất:

| CUDA Version | PyTorch | Khuyến nghị |
|--------------|---------|-------------|
| **CUDA 11.8** | ✅ Stable | **Khuyến nghị nhất** |
| CUDA 12.1 | ✅ Mới nhất | OK |
| CUDA 11.7 | ✅ Stable | OK |

**Lý do chọn CUDA 11.8**:
- ✅ Hỗ trợ tốt GTX 1050 Ti
- ✅ PyTorch có build sẵn
- ✅ Ổn định, ít bug
- ✅ Tương thích faster-whisper

## 🚀 Cài đặt nhanh

### Bước 1: Kiểm tra driver NVIDIA

```bash
nvidia-smi
```

**Yêu cầu**: Driver >= 450.x

Nếu chưa có driver:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nvidia-driver-535
sudo reboot
```

### Bước 2: Cài đặt CUDA Toolkit 11.8

```bash
# Download CUDA 11.8
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run

# Cài đặt (chỉ toolkit, không cài driver)
sudo sh cuda_11.8.0_520.61.05_linux.run --toolkit --silent --override

# Thêm vào PATH
echo 'export PATH=/usr/local/cuda-11.8/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc

# Kiểm tra
nvcc --version
```

### Bước 3: Cài đặt PyTorch với CUDA 11.8

```bash
# Activate virtual environment
source speechtotext/bin/activate

# Cài PyTorch với CUDA 11.8
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Kiểm tra
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0))"
```

**Kết quả mong đợi**:
```
CUDA available: True
GPU: NVIDIA GeForce GTX 1050 Ti
```

### Bước 4: Test với Whisper

```python
from faster_whisper import WhisperModel

# Load model trên GPU
model = WhisperModel("base", device="cuda", compute_type="float16")

# Test
segments, info = model.transcribe("test.mp3")
print("✅ GPU working!")
```

## 🔧 Troubleshooting

### Lỗi: "CUDA out of memory"

GTX 1050 Ti chỉ có 4GB VRAM, có thể không đủ cho model lớn.

**Giải pháp**:
```python
# Dùng model nhỏ hơn
model = WhisperModel("base", device="cuda", compute_type="float16")  # OK
model = WhisperModel("small", device="cuda", compute_type="float16") # OK
model = WhisperModel("turbo", device="cuda", compute_type="float16") # ❌ Quá lớn!

# Hoặc dùng int8 để tiết kiệm VRAM
model = WhisperModel("small", device="cuda", compute_type="int8")
```

### Lỗi: "CUDA driver version is insufficient"

Driver cũ, cần update:
```bash
sudo apt install nvidia-driver-535
sudo reboot
```

### Lỗi: "libcudart.so not found"

CUDA chưa được thêm vào PATH:
```bash
export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH
```

## 📊 Hiệu năng dự kiến

**GTX 1050 Ti với CUDA 11.8**:

| Model | CPU (turbo) | GPU (GTX 1050 Ti) | Speedup |
|-------|-------------|-------------------|---------|
| base | 2 phút | 20 giây | 6x |
| small | 3 phút | 30 giây | 6x |
| turbo | 6 phút | ❌ Out of memory | - |

**Khuyến nghị**: Dùng **small model** với GPU cho balance tốt nhất.

## 🎯 Cấu hình tối ưu cho GTX 1050 Ti

```python
# app.py
model = WhisperModel(
    "small",  # Vừa đủ cho 4GB VRAM
    device="cuda", 
    compute_type="float16"  # Hoặc int8 nếu cần tiết kiệm VRAM
)

segments, info = model.transcribe(
    filepath,
    beam_size=1,  # Giảm VRAM usage
    language="vi",
    vad_filter=True
)
```

**Kết quả dự kiến**:
- File 30 phút: **30-40 giây** (so với 6 phút trên CPU)
- Speedup: **~10x**

## 📝 Checklist cài đặt

- [ ] Kiểm tra nvidia-smi
- [ ] Cài CUDA 11.8 toolkit
- [ ] Thêm CUDA vào PATH
- [ ] Cài PyTorch với CUDA 11.8
- [ ] Test torch.cuda.is_available()
- [ ] Test Whisper với GPU
- [ ] Benchmark so sánh CPU vs GPU

---

Sau khi benchmark CPU xong, tôi sẽ giúp bạn cài đặt CUDA và test GPU! 🚀
