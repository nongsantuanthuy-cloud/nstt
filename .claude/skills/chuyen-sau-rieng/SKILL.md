---
name: chuyen-sau-rieng
description: Quy trình trọn gói làm 1 video "chuyện sầu riêng" cho kênh Nông Sản Tuấn Thủy (NSTT) — từ kịch bản canh.json, tạo clip Google Flow (Veo 3.1 Lite, Nhân vật Flow) qua Claude in Chrome, kiểm tra lời bằng Whisper, soát khung hình, dựng video dọc 9:16 có phụ đề karaoke + logo trong vùng an toàn TikTok/Reels/Shorts, đến lúc chủ kênh DUYỆT và soạn nội dung đăng. Dùng skill này mỗi khi chủ kênh nói làm video mới, làm tiếp video NSTT-..., tạo/tạo lại cảnh trên Flow, sửa lời thoại, dựng lại, kiểm tra clip, đổi giá trong truyện, chuẩn bị đăng TikTok/Facebook/YouTube, hoặc hỏi "làm tiếp thế nào" — kể cả khi không nhắc tên skill.
---

# Chuyện sầu riêng — quy trình sản xuất video NSTT

Skill này ghi lại cách đã làm thành công video đầu tiên **NSTT-20261001-B** (01/10/2026). Mục tiêu: chủ kênh
(không rành kỹ thuật, nói tiếng Việt) chỉ cần duyệt và nhắn ngắn; Claude làm phần còn lại và trả **file thật**.

Luôn trả lời chủ kênh bằng tiếng Việt, câu ngắn, không thuật ngữ. Gọi "anh/chị".

## 0. Trước khi bắt đầu

1. Thư mục làm việc là repo dự án (hiện tại `C:\Users\ADMIN\Desktop\NSTT`). Đọc `CLAUDE.md`, nhật ký mới nhất
   `nhat_ky/`, `trang_thai.md` của video đang làm, và `docs/01` (thương hiệu, nhân vật, câu cố định).
2. Python trên Windows gọi bằng `py` (không phải `python`). Đặt `$env:PYTHONIOENCODING='utf-8'` khi chạy công cụ.
   Thư viện cần: `py -m pip install imageio-ffmpeg pillow faster-whisper`.
3. Quyết định đã chốt — **không hỏi lại**: tên kênh Nông Sản Tuấn Thủy, hotline/Zalo 0392.547.547, màu
   #024815 + #F2CD41, nhân vật tự thoại (Veo tạo tiếng), **không chữ lớn nền xanh trên video**, không nhạc nền,
   không bao giờ đăng khi chưa có chữ **"DUYỆT <mã video>"**.

## 1. Kịch bản (`kich_ban/<mã>/canh.json`)

- Khung 20 cảnh: HOOK → CAU_MO → BOI_CANH → VONG_LAP → LEO_THANG → DINH_DIEM → HOA_GIAI → GOC_NHIN → MEO →
  CAU_HOI_2_PHE → KET_1 → KET_2 (chi tiết `docs/03` mục 6).
- Câu cố định (chủ kênh chốt 01/10/2026, đã nằm trong `tools/kiem_tra_kich_ban.py`):
  - Mở: "Chào cả nhà, chuyện nghề sầu riêng hôm nay, Tuấn Thủy lại kể mọi người nghe."
  - Kết 1 (dài 29 âm tiết → **tách 2 cảnh** cùng `phan: KET_1`): "Có hàng cần bán, bà con cứ tham khảo Nông Sản
    Tuấn Thủy xem sao nha." + "Mình cùng trao đổi rõ ràng, thuận mua vừa bán, ai cũng vui."
  - Kết 2: "Cảm ơn bà con đã tin tưởng và hẹn gặp lại trong những vườn sầu riêng."
- Mỗi clip 8 giây chứa tối đa **26 âm tiết** (Veo nói ~3,6 âm tiết/giây), tối đa 2 lượt thoại. Số viết bằng chữ.
  Không viết tắt "NSTT" trong lời (Veo đọc từng chữ cái).
- Tiền trong truyện phải cộng trừ đúng → ghi `bang_tinh`. Chủ kênh thích giá **thực tế** (01-B: chốt 65k, kho 45k,
  chợ 40k, hòa giải 50k). Khi đổi một con số, rà lại mọi câu, `chu_man_hinh`, `tieu_de_tam`, `kich_ban.md`, `seo.md`.
- Xưng hô đúng vai: Thắng Lanh xưng "em" với anh Bảy, "con" với Chú Năm. Ưu tiên "hợp đồng" hơn "kèo" ở câu chốt.
- Kiểm tra: `py tools/kiem_tra_kich_ban.py kich_ban/<mã>/canh.json --md` phải in `OK` (`--md` sinh lại kich_ban.md).
- Cho chủ kênh đọc kịch bản: `py tools/xuat_trang_duyet.py <canh.json> -o kich_ban/<mã>/duyet_kich_ban.html`
  rồi gửi file bằng SendUserFile (display render). Chủ kênh sửa lời → sửa cả `thoai[].cau` **và** câu trong
  `prompt_flow` (công cụ kiểm tra bắt lệch), chạy lại kiểm tra.

## 2. Tạo clip trên Google Flow (Claude in Chrome)

Đọc `references/flow.md` trước khi thao tác — có vị trí nút, mẹo tránh bấm nhầm thùng rác, cách tải về, và hàm JS
dựng sẵn (`scripts/flow_helpers.js`).

Tóm tắt:
- Dự án Flow: **NSTT-20260929-MAU** (https://flow.google.com/project/a6c6ab3d-58b1-40e7-bacd-8ba4e09c970f).
  Nhân vật Flow có sẵn: Nguoi Ke, Em Tuan, Chu Nam, Ut Nho, Thang Lanh, Bay Loi. Không dùng Co Hai, Chu Ba, Ong Sau Cu.
- **Luôn kiểm tra model trước khi gửi**: menu cài đặt phải ghi "Veo 3.1 - Lite" và "tốn 10 tín dụng". Flow hay tự
  đổi về "Omni 1.1 Flash" (12 tín dụng) khi mở tab mới.
- Cách duyệt với chủ kênh: video mới → làm **từng cảnh**, gửi clip lên chat, chờ "duyệt"/sửa lời rồi mới làm cảnh
  sau (xem phần 6). Khi chủ kênh nói "làm hết không cần hỏi" thì gửi lần lượt, nghỉ vài giây giữa các lượt.
- Nếu Flow báo **"Chúng tôi nhận thấy có hoạt động bất thường"**: dừng ngay, không thử lách. Lượt đó không tính phí.
  Soạn file `kich_ban/<mã>/tao_lai_<cảnh>.txt` (nhân vật + prompt nguyên văn) để chủ kênh tự tạo tay.
- Ghi tiến độ vào `kich_ban/<mã>/flow_tien_do.md` (cảnh → id clip trong URL `/edit/<id>`). Ghép clip với cảnh bằng
  cách mở clip và đọc câu trong prompt (`says ... "<câu>"`), không đoán theo ảnh thu nhỏ.
- Tải 720p → `scripts/nhan_clip.ps1 -So Sxx` chép file mới nhất trong Downloads thành `clip_veo/Sxx.mp4`.

## 3. Kiểm tra lời thoại (Whisper)

```
py tools/moc_tu_whisper.py kich_ban/<mã>/canh.json --model small --device cpu
```
- Dùng **small + cpu** (máy không có CUDA; mạng tải HuggingFace chậm nên large-v3 không khả thi).
- Cảnh "TẠO LẠI": nghe lại trước khi tạo lại — công cụ đã tự thử lại không VAD, nhưng vẫn có thể là Whisper nghe
  nhầm chữ (S16 khớp 78% nhưng nói đủ câu). Chỉ tạo lại khi lời thật sự sai/thiếu (S11 nói câu khác hẳn).
- Kết quả ghi `tu_thoai/Sxx.json` (mốc từng chữ, chữ theo kịch bản) — phụ đề dùng file này.

## 4. Soát hình và cắt

1. Ảnh lưới 3 khung/clip: `py scripts/luoi_khung.py <mã> <thư mục ra>` rồi xem bằng Read. Loại: sai mặt/áo,
   chữ lạ, người lạ, nón Bảy Lợi có huy hiệu.
2. Đặt đoạn dùng theo mốc Whisper: `py scripts/dat_dung.py <mã>` (0,25 s trước chữ đầu → 0,5 s sau chữ cuối).
   Clip Veo 8 s gần như không có khoảng lặng — bỏ bước này video dài thêm ~35 s. Cảnh kết cuối nên để dài tới
   ~7,5 s cho đoạn bước đi.
3. Góc cắt `cat`: cảnh 2 người đứng 2 bên → đặt tâm vào **người đang nói** (`can@0.3` bên trái, `can@0.6` bên phải).
   Lỗi hay gặp: `dac_ta`/`can` giữa khung rơi vào thùng sầu riêng hay xe máy.

## 5. Dựng video

```
py tools/dung_video_v3.py kich_ban/<mã>/canh.json --logo thuong_hieu/logo/logo_nstt_400.png
```
- Ra `ban_dung/<mã>.mp4`: 1080×1920, 30 fps, H.264, AAC, −14 LUFS, phụ đề karaoke, logo 150 px tại (36, 290),
  chân phụ đề y=1245 (thấp nhất còn an toàn cho Reels). Mặc định **không** hiện chữ lớn nền xanh.
- Soát lại sau khi dựng: tờ ảnh 1 khung/giây (ffmpeg `fps=1,scale=160:-1,tile=12x5`) để bắt góc cắt lệch;
  `py tools/vung_an_toan.py <video> --giay N -o <ảnh>` để xem chữ/logo có lọt vùng bị app che không;
  đo âm lượng bằng ffmpeg `ebur128`.
- Gửi video bằng SendUserFile (display render), nói rõ cảnh nào còn lỗi. Chi tiết: `references/dung_va_dang.md`.

## 6. Làm việc với chủ kênh

- Mỗi lần gửi clip/video: 1 bảng ngắn (nhân vật, lời thoại, thời lượng) + 3 lựa chọn trả lời
  ("Duyệt Sxx" / "Tạo lại Sxx" / "Sửa lời Sxx: …"). Nói thật là Claude **không nghe được tiếng** — nhờ chủ kênh nghe.
- Chủ kênh hay gõ tắt/sai chính tả ("duyet s01" khi đang chờ S04, "kham khảo") — hiểu theo ngữ cảnh, nói rõ đã hiểu
  thế nào, rồi làm. Câu chủ kênh viết vượt 26 âm tiết → đưa phương án (rút gọn / tách cảnh) thay vì tự cắt.
- Khi chủ kênh nói "làm sau khi tôi hỏi lại" → ghi nhận, không làm.
- Việc cần chủ kênh tự làm (đăng nhập GitHub, tắt "Hỏi nơi lưu trước khi tải" của Chrome, đăng bài): hướng dẫn
  từng bước đánh số, chỉ đúng nút cần bấm.

## 7. Sau khi DUYỆT

1. `trang_thai.md` = "ĐÃ DUYỆT — CHỜ ĐĂNG"; soạn nội dung đăng từ `seo.md` (tiêu đề riêng 3 nền tảng, mô tả chung,
   bình luận ghim, nhắc bật nhãn AI). Claude không đăng hộ.
2. Nhật ký `nhat_ky/YYYY-MM-DD.md` (làm gì, kiến thức mới, việc tiếp theo) + cập nhật `docs/` + hồ sơ kênh
   (Claude Docs "Hồ sơ kênh Nông Sản Tuấn Thủy") nếu có thay đổi.
3. Commit trên máy. Shell của Claude không push được (chưa có quyền Git) → nhờ chủ kênh mở **GitHub Desktop → Push
   origin**. Clip `.mp4` không lên Git — nhắc chép `clip_veo/` và `ban_dung/` lên Google Drive.
