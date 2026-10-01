# BÀN GIAO SANG PC — Kênh Nông Sản Tuấn Thủy (01/10/2026)

Tài liệu này để chủ kênh cài Claude Code trên PC Windows và để **Claude Code trên PC làm tiếp** đúng chỗ phiên cloud dừng.
Claude Code trên PC: đọc file này sau `CLAUDE.md`.

## 1. Tình trạng hiện tại
| Việc | Trạng thái |
|---|---|
| Thương hiệu, logo, 9 nhân vật | Xong — `docs/01`, `thuong_hieu/` |
| Phân tích video mẫu (50 cảnh) | Xong — `docs/02b` |
| 3 kịch bản v3 nhân vật tự thoại | Xong, chờ duyệt lời — `kich_ban/NSTT-20261001-A`, `-B`, `NSTT-20261002-A` |
| Video làm đầu tiên | **NSTT-20261001-B (Giá sập, cò định bỏ cọc)** — 19 cảnh |
| Clip S01 của 01-B | Đã tạo trên Flow, đã dựng thử (đẹp, đúng nhân vật). **Chủ kênh chưa xác nhận giọng Việt.** |
| Clip S02–S19 của 01-B | **CHƯA LÀM** ← việc tiếp theo |
| Công cụ dựng video | Xong — `tools/dung_video_v3.py` (đã chạy thật với S01) |
| Công cụ kiểm tra thoại Whisper | Viết xong, chưa chạy thật — `tools/moc_tu_whisper.py` (PC chạy được) |
| Đăng video | KHÔNG đăng khi chưa có chữ "DUYỆT" |

## 2. Quyết định đã chốt (không hỏi lại)
- Tên kênh **Nông Sản Tuấn Thủy**; hotline/Zalo **0392.547.547**; màu xanh #024815 + vàng #F2CD41.
- Nhân vật **tự thoại** (Veo tạo tiếng + khẩu hình), không người kể; Tuấn Thủy nói thẳng vào máy ở đầu/cuối.
- Nhân vật: Tuấn Thủy `Nguoi Ke`, Em Tuấn `Em Tuan`, **Chú Năm `Chu Nam`** (thay Cô Hai), **Út Nhỏ `Ut Nho`** (con gái Chú Năm),
  Thắng Lanh `Thang Lanh`, Bảy Lợi `Bay Loi`, Chú Tư `Chu Tu`, Anh Sáu Tài `Sau Tai`, **Bà Tám Cân `Ba Tam`**.
- Tạo clip trên **Google Flow**, dùng **Nhân vật của Flow**, model **Veo 3.1 Lite (Lower Priority)**, 16:9, x1.
- Hậu kỳ: cắt góc trong clip (toàn/cận/đặc tả), **phụ đề karaoke** 2–3 chữ in hoa (chữ đang nói vàng), logo góc trên, −14 LUFS, không nhạc nền.

## 3. Cài đặt trên PC (chủ kênh làm 1 lần)
1. Cài **Git**: https://git-scm.com (mặc định, bấm Next).
2. Cài **Python 3**: https://python.org — **tích "Add python.exe to PATH"**.
3. Cài **Claude Code** theo hướng dẫn Windows: https://code.claude.com/docs — đăng nhập tài khoản Claude.
4. Cài tiện ích **Claude in Chrome** (Chrome Web Store, nhà phát triển Anthropic) trên Chrome **đã đăng nhập Google Flow**.
5. Mở **PowerShell**, chạy:
```
cd D:\
git clone https://github.com/nongsantuanthuy-cloud/nstt.git nstt
cd nstt
git checkout claude/kind-turing-suxd5o
pip install imageio-ffmpeg pillow faster-whisper
mkdir kich_ban\NSTT-20261001-B\clip_veo
```
6. Chép file clip S01 đã tải từ Flow vào `D:\nstt\kich_ban\NSTT-20261001-B\clip_veo\S01.mp4`.
7. Trong PowerShell (đang ở `D:\nstt`) gõ `claude` để mở Claude Code, rồi gõ `/chrome` để kết nối Chrome.

## 4. Lệnh dán vào Claude Code trên PC
```
Đọc CLAUDE.md, BAN_GIAO_PC.md và nhật ký mới nhất trong nhat_ky/. Làm tiếp video NSTT-20261001-B:
1) Trong Chrome, mở dự án Google Flow đã làm S01. Kiểm tra mục Nhân vật có đủ Nguoi Ke, Em Tuan, Chu Nam, Ut Nho,
   Thang Lanh, Bay Loi (thiếu Chu Nam/Ut Nho thì tạo từ thuong_hieu/nhan_vat/chu_nam.png, ut_nho.png). Hỏi tôi nếu thiếu nhân vật khác.
2) Tạo lần lượt S02 đến S19 theo kich_ban/NSTT-20261001-B/canh.json: mỗi lần 1 cảnh, nhấn Escape, Video 16:9 x1,
   Veo 3.1 Lite (Lower Priority), chọn đúng nhan_vat của cảnh, dán nguyên văn prompt_flow, tạo, tải 720p,
   lưu thành kich_ban/NSTT-20261001-B/clip_veo/Sxx.mp4.
3) Chạy: python tools/moc_tu_whisper.py kich_ban/NSTT-20261001-B/canh.json  — cảnh "TẠO LẠI" thì tạo lại trên Flow (tối đa 2 lần).
4) Xem khung hình từng clip (sai mặt/áo, chữ lạ, người lạ → tạo lại). Chỉnh "dung" và "cat" (vd "can@0.33") trong canh.json nếu cần.
5) Dựng: python tools/dung_video_v3.py kich_ban/NSTT-20261001-B/canh.json --logo thuong_hieu/logo/logo_nstt_400.png
6) Cập nhật kich_ban/NSTT-20261001-B/trang_thai.md = "CHỜ DUYỆT VIDEO", ghi nhat_ky, commit và push.
Không đăng video. Thiếu thông tin thì hỏi tôi.
```

## 5. Nhân vật từng cảnh — NSTT-20261001-B
| Cảnh | Nhân vật Flow |
|---|---|
| S01, S08, S09, S10 | Ut Nho + Chu Nam |
| S02, S14, S15, S17, S19 | Nguoi Ke |
| S03, S04, S11, S12, S13 | Thang Lanh + Chu Nam |
| S05 | Bay Loi |
| S06 | Thang Lanh + Bay Loi |
| S07 | Thang Lanh |
| S16 | Em Tuan |
| S18 | Nguoi Ke + Em Tuan |

## 6. Kinh nghiệm từ clip S01 (đọc trước khi làm)
- Veo 3.1 Lite trên Flow trả clip **10 giây**; câu nói nằm khoảng giây 3–8; trước đó có thể là tiếng bước chân.
- Tốc độ nói ~3,6 âm tiết/giây. Veo có thể tự cắt sang cận mặt — giữ nguyên, đẹp.
- Cảnh 2 người đứng 2 bên: dùng `"cat": ["toan", "can@0.33", "can@0.55"]` (tâm ngang theo người đang nói).
- Ảnh tham chiếu phải là ảnh 1 người, không chữ chú thích (đã cắt sẵn trong `thuong_hieu/nhan_vat/`).
- Phiên cloud không vào được Flow/Drive (mạng chặn, không có đăng nhập Google) — vì vậy phần Flow chuyển sang PC.

## 7. Còn chờ chủ kênh
- Xác nhận giọng Việt S01 có ổn (nếu không: phương án dự phòng lồng tiếng từng nhân vật — CAU_HOI #15).
- Duyệt lời 2 kịch bản còn lại (01-A, 02-A); tên series (#10); nhịp đăng (#8).
- Ảnh chuẩn cho Chú Tư, Anh Sáu Tài, Bà Tám (cần cho video 01-A, 02-A).
