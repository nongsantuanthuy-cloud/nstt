---
name: nstt-san-xuat-video
description: Sản xuất video drama sầu riêng ~2 phút cho kênh "Nông Sản Tuấn Thủy" (NSTT) — chọn chủ đề, viết canh.json, prompt Google Flow với dàn nhân vật cố định, giọng UV07, hậu kỳ, SEO, gửi duyệt. Dùng khi chủ kênh yêu cầu làm video mới, sửa lời/cảnh, dựng lại, hoặc hỏi quy trình NSTT.
---

# Sản xuất video NSTT (bản trong repo — nguồn kiến thức chung)

1. `git pull`. Đọc `CLAUDE.md`, nhật ký mới nhất trong `nhat_ky/`, `CAU_HOI_CHO_CHU_KENH.md`.
2. Tài liệu gốc: `docs/01` thương hiệu + nhân vật (9 nhân vật, tên Flow không dấu), `docs/03` khung 2 phút theo giây,
   `docs/04` SEO, `docs/05` kho chủ đề, `docs/06` từ điển, `docs/08` quy trình, `docs/09` nguồn kiến thức chung.
3. Viết `kich_ban/<ma>/canh.json` (mã `NSTT-YYYYMMDD-A|B`) → chạy
   `python3 tools/kiem_tra_kich_ban.py kich_ban/<ma>/canh.json --md` phải `OK`. Tiền phải cộng trừ đúng (ghi trong `bang_tinh`).
4. `seo.md`, `trang_thai.md` = "CHỜ DUYỆT LỜI". Gửi chủ kênh tóm tắt tiếng Việt.
5. Sau "DUYỆT LỜI": trên máy chủ kênh làm Flow → `kiem_tra_tieng_noi.py` → `tao_giong_omnivoice.py` (UV07) → `hau_ky_nstt.py`.
   Nhân vật mới chưa có ảnh Flow → tạo theo `thuong_hieu/nhan_vat_moi.md` trước.
6. Gửi video, chờ "DUYỆT". **Không bao giờ tự đăng khi chưa duyệt; không in/gửi token.**
7. Cuối phiên: nhật ký + cập nhật docs + commit + push.

Cấm: nhạc nền · nhân vật nói (lip-sync) · giọng khác UV07 · tên thật người/kho/doanh nghiệp · `Chu Ba`, `Ong Sau Cu`,
nón Bảy Lợi có huy hiệu · viết "Tuấn Thúy".
Thiếu thông tin → hỏi chủ kênh + ghi `CAU_HOI_CHO_CHU_KENH.md`. Đủ thông tin → làm đến hết, trả file thật.
