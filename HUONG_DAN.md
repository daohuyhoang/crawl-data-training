# 📖 HƯỚNG DẪN SỬ DỤNG

## 🚀 Bắt đầu nhanh

### Bước 1: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

**Lưu ý:** Lần đầu chạy sẽ tải model PhoBERT (~540MB), cần kết nối internet.

---

### Bước 2: Cào dữ liệu từ Facebook

```bash
python fb_scraper.py
```

**Làm gì:**
1. Nhập link bài viết Facebook (ví dụ: link review quán ăn)
2. Đợi 30 giây để đăng nhập Facebook (nếu cần)
3. Chương trình sẽ tự động cào bình luận
4. Dữ liệu lưu vào file `crawled_fb.csv`

**Ví dụ link:**
- Link bài viết fanpage: `https://www.facebook.com/vnexpressnews/posts/...`
- Link bài viết group: `https://www.facebook.com/groups/123456/posts/...`

---

### Bước 3: Gán nhãn tự động

```bash
python auto_label_bert.py
```

**Làm gì:**
- Đọc dữ liệu từ `crawled_fb.csv`
- Dùng AI (PhoBERT) gán nhãn tự động
- Lưu vào `labeled_data_bert.csv`
- Xóa dữ liệu đã xử lý khỏi `crawled_fb.csv`

**Nhãn:**
- 0 = Tiêu cực (dở, tệ, chán...)
- 1 = Khác (bình thường, không rõ...)
- 2 = Tích cực (ngon, tốt, hay...)

---

### Bước 4: Train model

```bash
python train.py
```

**Làm gì:**
- Đọc dữ liệu từ `labeled_data_bert.csv`
- Train model phân loại sentiment
- Lưu model vào `sentiment_model.pkl`

**Kết quả:** Hiển thị độ chính xác và báo cáo chi tiết.

---

### Bước 5: Dự đoán (Test model)

```bash
python predict.py
```

**Làm gì:**
- Nhập câu bất kỳ
- Model dự đoán sentiment
- Hiển thị kết quả và độ tin cậy

**Ví dụ:**
```
Nhập câu: Quán này ngon lắm!
→ Tích cực (83.6%)

Nhập câu: Dở quá, không bao giờ quay lại
→ Tiêu cực (74.2%)
```

---

## 🔄 Quy trình hoàn chỉnh

```
1. Cài đặt
   pip install -r requirements.txt

2. Cào dữ liệu
   python fb_scraper.py
   (Nhập link Facebook)

3. Gán nhãn
   python auto_label_bert.py

4. Train model
   python train.py

5. Test
   python predict.py
```

---

## 💡 Lệnh hữu ích

### Kiểm tra trạng thái
```bash
python check_status.py
```
Xem có bao nhiêu dữ liệu, model đã train chưa.

### Xem mẫu dữ liệu
```bash
python view_samples.py
```
Xem các bình luận đã gán nhãn.

### Chạy tự động (Cào + Gán nhãn)
```bash
python run_pipeline.py
```
Chọn chế độ 3 để chạy tự động cả 2 bước.

---

## ❓ Câu hỏi thường gặp

**Q: Cào không được dữ liệu?**
- Đảm bảo đã đăng nhập Facebook
- Đợi đủ 30 giây
- Thử link bài viết khác (fanpage công khai)

**Q: Lỗi khi gán nhãn?**
- Chạy: `pip install torch transformers`
- Lần đầu sẽ tải model (~540MB)

**Q: Model dự đoán sai?**
- Cần thêm dữ liệu (ít nhất 500-1000 bình luận)
- Chạy lại: `python train.py`

**Q: Muốn train lại model?**
- Cào thêm dữ liệu
- Chạy: `python auto_label_bert.py`
- Chạy: `python train.py`

---

## 📁 File quan trọng

| File | Mô tả |
|------|-------|
| `crawled_fb.csv` | Dữ liệu mới cào (tạm thời) |
| `labeled_data_bert.csv` | Dữ liệu đã gán nhãn (chính) |
| `sentiment_model.pkl` | Model đã train |

**Lưu ý:** Chỉ backup file `labeled_data_bert.csv`, các file khác có thể tạo lại.

---

## 🎯 Ví dụ thực tế

### Ví dụ 1: Phân tích review quán ăn

```bash
# 1. Cào review từ fanpage quán ăn
python fb_scraper.py
# Nhập: https://www.facebook.com/quananngon/posts/123456

# 2. Gán nhãn
python auto_label_bert.py

# 3. Train
python train.py

# 4. Test
python predict.py
# Nhập: "Quán này ngon, giá rẻ"
# → Tích cực
```

### Ví dụ 2: Cào nhiều lần

```bash
# Lần 1: Cào 100 bình luận
python fb_scraper.py
python auto_label_bert.py

# Lần 2: Cào thêm 100 bình luận
python fb_scraper.py
python auto_label_bert.py

# Train với 200 bình luận
python train.py
```

---

## 🆘 Cần trợ giúp?

1. Chạy `python check_status.py` để xem trạng thái
2. Đọc file `WORKFLOW.md` để hiểu chi tiết
3. Xem file `PROJECT_SUMMARY.md` để biết tổng quan

---

**Chúc bạn thành công! 🎉**
