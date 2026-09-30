# 08 — Quy trình sản xuất (tóm tắt, bản đầy đủ ở skill `nstt-san-xuat-video` và máy chủ kênh)

| Bước | Việc | Chạy ở đâu | Đầu ra |
|---|---|---|---|
| B1 | Chọn chủ đề (docs/05), viết `canh.json` + `kich_ban.md` | Cloud hoặc máy | `kich_ban/<ma>/` |
| B1b | `python3 tools/kiem_tra_kich_ban.py kich_ban/<ma>/canh.json` | Cloud hoặc máy | báo OK |
| B2 | Tạo clip Google Flow (Veo 3.1 Lite, 16:9, x1, 10 credit/clip); dự án mẫu có sẵn 5 nhân vật | Máy chủ kênh (Chrome) | `clip_veo/Sxx.mp4` |
| B3 | `python tools\kiem_tra_tieng_noi.py` — 100% tiếng Việt, tắt âm gốc cảnh lẫn tiếng nước ngoài | Máy | `kiem_tra_am_thanh.json` |
| B4 | Giọng OmniVoice UV07: `tools\tao_giong_omnivoice.py` (thiếu RAM → `OMNI_DTYPE=bf16`) | Máy | `giong/Sxx.wav` |
| B5 | Hậu kỳ `tools\hau_ky_nstt.py` (Remotion + FFmpeg, 1080×1920, 30fps, −14 LUFS, không nhạc nền) | Máy | `ban_dung/<ma>.mp4` |
| B6 | `seo.md`, `trang_thai.md` = CHỜ DUYỆT, gửi chủ kênh | Cả hai | |
| B7 | Đăng — CHỈ khi có chữ DUYỆT; bật nhãn AI | Máy | |

Chi phí Flow ước tính: 20 cảnh × 10 credit = 200 credit/video (+ ~20–30% tạo lại).
