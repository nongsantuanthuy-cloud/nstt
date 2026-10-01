# Dựng, soát và đăng

## Thông số video (chuẩn chung TikTok / Reels / Shorts)
| Mục | Giá trị |
|---|---|
| Khung | 1080×1920, 9:16, 30 fps, H.264 yuv420p ~5 Mbps |
| Tiếng | AAC 48 kHz, −14 LUFS, không nhạc nền |
| Thời lượng | 110–135 s (01-B: 124,6 s). Shorts nhận ≤ 3 phút; Reels có thể giới hạn → làm bản ~90 s nếu Facebook từ chối |
| Phụ đề | Karaoke 2–3 chữ IN HOA, chữ đang nói vàng #F2CD41, chân y = 1245 |
| Logo | `logo_nstt_400.png` thu 150 px tại (36, 290) |
| Chữ lớn nền xanh | Không dùng (chủ kênh chốt 01/10/2026); muốn bật: `--hien-chu-lon` |

## Vùng bị giao diện app che (công cụ `tools/vung_an_toan.py`)
- Trên 14% (270 px): tab, nút LIVE, chữ "Reels" → logo phải nằm dưới.
- Dưới 35% với Reels (từ y ≈ 1248), ~22% với TikTok/Shorts → phụ đề chân y ≤ 1245 để hợp cả 3.
- Cột nút bên phải ~140 px từ 40% đến 85% chiều cao → phụ đề lề 150 px mỗi bên.
- Nếu chủ kênh muốn phụ đề sát đáy hơn: xuất 2 bản (TikTok/Shorts ~75–77% chiều cao; Reels giữ 65%) —
  **chỉ làm khi chủ kênh yêu cầu**.

## Soát sau khi dựng
```powershell
$ff = py -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"
& $ff -hide_banner -loglevel error -y -i <video> -vf "fps=1,scale=160:-1,tile=12x5" -frames:v 1 soat.jpg        # 60 s đầu
& $ff -hide_banner -loglevel error -y -ss 60 -i <video> -vf "fps=1,scale=160:-1,tile=12x5" -frames:v 1 soat2.jpg
& $ff -hide_banner -i <video> -af ebur128=framelog=quiet -f null -   # dòng "I:" ≈ −14 LUFS
```
Xem: người đang nói có trong khung dọc không; phụ đề không che mặt; logo không đè chữ.

## Nội dung đăng (từ seo.md)
- Tiêu đề riêng cho TikTok (cảm xúc, có emoji), Facebook Reels (câu chuyện + con số), YouTube Shorts
  (câu hỏi + "| Nông Sản Tuấn Thủy").
- Mô tả chung: tóm tắt có số, 1 mẹo, câu hỏi 2 phe kêu gọi bình luận, hotline/Zalo 0392.547.547,
  dòng "⚠️ Câu chuyện mô phỏng, hình ảnh tạo bằng AI, nhân vật không có thật.", hashtag
  `#nongsantuanthuy #saurieng #giasaurieng #thuonglai #daklak`.
- Bình luận ghim = câu hỏi 2 phe (khớp lời cảnh CAU_HOI_2_PHE).
- Nhắc bật nhãn AI: TikTok "nội dung do AI tạo", YouTube "nội dung bị thay đổi hoặc tổng hợp", Facebook "Nhãn AI".
- Kiểm mô tả khớp kịch bản (01-B từng ghi "Mười ngày sau" trong khi truyện là "nửa tháng").
