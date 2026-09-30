---
name: nstt-san-xuat-video
description: Sản xuất video drama sầu riêng ~2 phút cho kênh "Nông Sản Tuấn Thủy" (NSTT) — chọn chủ đề, viết canh.json kiểu nhân vật tự thoại, prompt Google Flow/Veo với dàn nhân vật + giọng cố định, kiểm tra thoại bằng Whisper, dựng FFmpeg (cắt góc + phụ đề karaoke), SEO, gửi duyệt. Dùng khi chủ kênh yêu cầu làm video mới, sửa lời/cảnh, dựng lại, hoặc hỏi quy trình NSTT.
---

# Sản xuất video NSTT (bản trong repo — nguồn kiến thức chung, cập nhật 30/09/2026)

1. `git pull`. Đọc `CLAUDE.md`, nhật ký mới nhất trong `nhat_ky/`, `CAU_HOI_CHO_CHU_KENH.md`.
2. Tài liệu: `docs/01` thương hiệu + 9 nhân vật + giọng, `docs/02b` phân tích thật video mẫu,
   `docs/03` mục 6 (chuẩn thoại hiện hành), `docs/04` SEO, `docs/05` chủ đề, `docs/08` quy trình, `docs/09` nguồn chung.
3. Viết `kich_ban/<ma>/canh.json` kiểu `"thoai"` (mã `NSTT-YYYYMMDD-A|B`) → `python3 tools/kiem_tra_kich_ban.py <canh.json> --md` phải `OK`.
   Tiền phải cộng trừ đúng (ghi `bang_tinh`). Mỗi clip ≤ 26 âm tiết, tốt nhất 1 người nói.
4. `seo.md`, `trang_thai.md` = "CHỜ DUYỆT LỜI". Gửi chủ kênh tóm tắt tiếng Việt.
5. Sau "DUYỆT LỜI" (máy chủ kênh): Flow (thử S01 trước) → `tools/moc_tu_whisper.py` → tạo lại cảnh lỗi →
   `tools/dung_video_v3.py --logo ...` → gửi video.
6. Chờ "DUYỆT". **Không bao giờ tự đăng khi chưa duyệt; không in/gửi token.**
7. Cuối phiên: nhật ký + cập nhật docs + commit + push.

Cấm: nhạc nền · logo đài/báo · tên thật người/kho/doanh nghiệp · `Chu Ba`, `Ong Sau Cu`, nón Bảy Lợi có huy hiệu ·
viết "Tuấn Thúy" · lặp lại chi tiết riêng của video mẫu (đạp chân dưới bàn cân, con gái quay video, lấy ngẫu nhiên 10 sọt,
câu "mất chữ tín thì chẳng còn gì").
Thiếu thông tin → hỏi chủ kênh + ghi `CAU_HOI_CHO_CHU_KENH.md`. Đủ thông tin → làm đến hết, trả file thật.
