# CLAUDE.md — Kênh NÔNG SẢN TUẤN THỦY (NSTT)

Repo này là **nguồn kiến thức DUY NHẤT** của dự án (chủ kênh chốt 30/09/2026 — xem `docs/09`).
Đầu phiên `git pull`, cuối phiên `git push`. Mọi phiên Claude mới PHẢI đọc theo thứ tự:

1. File này.
2. File mới nhất trong `nhat_ky/` (nhật ký phiên trước: làm gì, dở gì, việc tiếp theo).
3. `CAU_HOI_CHO_CHU_KENH.md` — câu hỏi còn treo. Chưa có trả lời thì KHÔNG tự đoán.
4. `docs/` — kiến thức gốc (luôn đúng hơn trí nhớ của model).

## Quyết định đã chốt
- Tên kênh: **Nông Sản Tuấn Thủy** (không viết "Tuấn Thúy").
- Dàn nhân vật 9 người — docs/01. **Cô Hai đã đổi thành Chú Năm** (`Chu Nam`, ảnh chủ kênh, 30/09). Út Nhỏ, Chú Năm dùng ảnh chủ kênh gửi.
- Repo GitHub là nguồn kiến thức chung duy nhất — docs/09.
- **Nhân vật tự thoại, bỏ người kể UV07** (Tuấn Thủy nói thẳng vào máy ở đầu/cuối); cắt + phóng to trong clip;
  phụ đề karaoke — docs/03 mục 6, docs/08.
- **Tạo clip: Google Flow** (Claude in Chrome / điều khiển máy trên máy chủ kênh), **Nhân vật của Flow** để đồng bộ,
  model **Veo 3.1 Lite (Lower Priority)**. Phiên cloud chỉ chuẩn bị kịch bản + trang lệnh và dựng video khi có clip.

## Mục tiêu dự án
Sản xuất tự động video drama ngắn (~2 phút, dọc 9:16) cho Facebook Reels, TikTok, YouTube Shorts
về chuyện thu mua sầu riêng (nhà vườn – thương lái – chủ kho – cò), hình ảnh AI (Google Flow / Veo),
nhân vật tự thoại (Veo tạo tiếng), Tuấn Thủy mở và kết video. Mục đích thương mại: xây uy tín cho thương hiệu thu mua **Nông Sản Tuấn Thủy**,
hotline/Zalo **0392.547.547**.

## Quy tắc làm việc (chủ kênh yêu cầu)
- Thiếu thông tin để làm tự động → HỎI chủ kênh và ghi vào `CAU_HOI_CHO_CHU_KENH.md`.
- Đủ thông tin → tự làm đến hết, trả **kết quả thật** (file thật, không mô tả suông).
- Cần đổi tên / thêm nhân vật để hấp dẫn hơn → ĐỀ XUẤT với chủ kênh, không tự áp dụng.
- Cuối mỗi phiên: ghi `nhat_ky/YYYY-MM-DD.md` + cập nhật kiến thức mới vào `docs/`.
- Không bao giờ tự đăng video khi chưa có chữ **DUYỆT** của chủ kênh cho đúng video đó.
- Không in/gửi token, mật khẩu.

## Bản đồ repo
| Đường dẫn | Nội dung |
|---|---|
| `docs/01_THUONG_HIEU_NHAN_VAT.md` | Thương hiệu, màu, câu mở/kết, dàn nhân vật + mô tả prompt |
| `docs/02_PHAN_TICH_VIDEO_MAU.md` | Phân tích video mẫu + kịch bản mẫu theo từng khung/cảnh |
| `docs/02b_VIDEO_MAU_TUNG_KHUNG.md` | Phân tích THẬT video mẫu: 50 cảnh, lời thoại, phụ đề, âm thanh + ảnh `docs/hinh_video_mau/` |
| `docs/03_CAU_TRUC_KICH_BAN.md` | Khung 2 phút theo từng giây, quy tắc viết lời, định dạng `canh.json` |
| `docs/04_SEO_VA_LICH_DANG.md` | Tiêu đề, mô tả, hashtag, giờ đăng |
| `docs/05_KHO_CHU_DE.md` | Kho chủ đề + trạng thái đã/chưa làm |
| `docs/06_TU_DIEN_NGANH.md` | Từ ngữ ngành sầu riêng dùng trong lời |
| `docs/08_QUY_TRINH_SAN_XUAT.md` | Quy trình Flow → giọng → hậu kỳ → duyệt |
| `docs/09_NGUON_KIEN_THUC_CHUNG.md` | Repo = nguồn duy nhất; cách gộp thư mục máy chủ kênh |
| `thuong_hieu/nhan_vat_moi.md` | Prompt tạo ảnh tham chiếu Flow cho 4 nhân vật mới |
| `.claude/skills/nstt-san-xuat-video/` | Skill dự án (tự nạp) |
| `docs/10_DE_XUAT_NHAN_VAT_THUONG_HIEU.md` | Đề xuất đổi tên / nhân vật (đã chốt 30/09) |
| `kich_ban/<ma_video>/` | `canh.json`, `kich_ban.md`, `seo.md`, `trang_thai.md` |
| `tools/kiem_tra_kich_ban.py` | Kiểm tra `canh.json`: độ dài ước tính, số viết bằng chữ, tên nhân vật, cấu trúc |
| `tools/trich_khung_hinh.py` | Trích khung hình + bảng cảnh từ video mẫu (ffmpeg) |
| `tools/moc_tu_whisper.py` | (máy) Whisper kiểm tra thoại Veo đúng lời/tiếng Việt + mốc từng chữ |
| `tools/xuat_trang_duyet.py` | Xuất trang HTML đọc kịch bản trên điện thoại → xuất bản Artifact (chủ kênh KHÔNG xem được file .md có bảng rộng) |
| `tools/dung_video_v3.py` | Dựng video v3: cắt góc toàn/cận/đặc tả, phụ đề karaoke, chữ lớn, logo, −14 LUFS (chỉ cần ffmpeg) |

## Môi trường
- Máy chủ kênh (Windows): `D:\CLAUDE DU AN NSTT\kenh nstt` — có OmniVoice (giọng UV07), Remotion, Node portable.
- Google Drive: thư mục `NSTT` (id `186KubQ392b4upLEwBkh1n-jO8Tx5ITuk`) — `docs`, `kich_ban`, `thuong_hieu`, `nhat_ky`.
- Phiên cloud KHÔNG chạy được Flow/Whisper (mạng chặn HuggingFace, Drive) → làm kịch bản, prompt, SEO, công cụ, tài liệu;
  chạy được `dung_video_v3.py` nếu chủ kênh tải clip lên phiên.

## Kiểm tra nhanh trước khi giao kịch bản
```
python3 tools/kiem_tra_kich_ban.py kich_ban/<ma>/canh.json
```
Phải báo `OK` (tổng 110–135 giây, không có chữ số trong lời, nhân vật hợp lệ).
