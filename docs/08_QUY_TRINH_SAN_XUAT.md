# 08 — Quy trình sản xuất (bản 4, từ 30/09/2026: nhân vật tự thoại)

| Bước | Việc | Chạy ở đâu | Đầu ra |
|---|---|---|---|
| B1 | Chọn chủ đề (docs/05), viết `canh.json` kiểu `thoai` (docs/03 mục 6) | Cloud hoặc máy | `kich_ban/<ma>/canh.json` |
| B1b | `python tools/kiem_tra_kich_ban.py kich_ban/<ma>/canh.json --md` → phải `OK` | Cloud hoặc máy | `kich_ban.md` |
| — | Chủ kênh **DUYỆT LỜI** | | |
| B2 | **Chủ kênh chốt 30/09: tạo clip trên Google Flow** bằng điều khiển máy tính hoặc **Claude in Chrome** (tiện ích trên máy chủ kênh — phiên cloud KHÔNG vào được Flow). Dùng **quản lý Nhân vật của Flow** để đồng bộ nhân vật; model **Veo 3.1 Lite (Lower Priority)** để tiết kiệm credit; 16:9, 8 s, x1. Hướng dẫn từng bước + nhân vật từng cảnh ở đầu trang duyệt (Artifact) mục "Tạo clip trên Google Flow". (Phương án dự phòng không dùng: Gemini API `tools/tao_clip_veo_api.py`, tốn tiền riêng.) Cũ: dán `prompt_flow` từng cảnh; nhân vật mới cần ảnh tham chiếu trước (`thuong_hieu/nhan_vat_moi.md`). **Làm thử S01 trước**, nghe tiếng Việt có ổn không rồi mới làm tiếp | Máy chủ kênh (Chrome) | `clip_veo/Sxx.mp4` |
| B3 | `python tools/moc_tu_whisper.py kich_ban/<ma>/canh.json` — kiểm tra Veo nói đúng lời + đúng tiếng Việt, lấy mốc từng chữ | Máy (faster-whisper) | `tu_thoai/Sxx.json`, `clip_veo/kiem_tra_thoai.json` |
| B3b | Cảnh "TẠO LẠI" → tạo lại clip trên Flow → chạy lại B3 | Máy | |
| B4 | Xem từng clip: trang phục đúng, không chữ lạ/logo/huy hiệu, khẩu hình khớp. Mặt lệch → thêm `tam_x`; đoạn thừa → `dung` | Máy | sửa canh.json |
| B5 | `python tools/dung_video_v3.py kich_ban/<ma>/canh.json --logo thuong_hieu/logo/logo_nstt_400.png` (`--nhap` để xem nhanh) | Máy hoặc cloud (chỉ cần ffmpeg) | `ban_dung/<ma>.mp4` 1080×1920, −14 LUFS, phụ đề karaoke |
| B6 | `seo.md`, `trang_thai.md` = CHỜ DUYỆT, gửi chủ kênh | | |
| B7 | Đăng — CHỈ khi có chữ DUYỆT; bật nhãn AI | Máy | |

- **Bỏ** bước giọng OmniVoice UV07 (không còn người kể). OmniVoice chỉ dùng lại nếu chủ kênh chọn phương án dự phòng
  "lồng tiếng từng nhân vật" (CAU_HOI #15).
- `tools/hau_ky_nstt.py` + Remotion (máy) là quy trình cũ cho kịch bản người kể; kịch bản v3 dùng `dung_video_v3.py`.
- Chi phí Flow: ~20 clip × 10 credit = 200 credit/video + tạo lại (thoại dễ lỗi hơn → dự trù 30–50%).
- Font phụ đề mặc định "Arial" (Windows có sẵn, đủ dấu tiếng Việt); đổi bằng `--font`.
