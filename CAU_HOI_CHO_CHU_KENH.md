# Câu hỏi chờ chủ kênh trả lời

Trả lời trực tiếp trong chat hoặc sửa file này (ghi "TRẢ LỜI: ..." dưới câu hỏi). Phiên sau đọc trước khi làm.

## Đang chờ
| # | Ngày | Câu hỏi | Vì sao cần |
|---|---|---|---|
| 6b | 30/09 | Chạy bước gộp thư mục máy chủ kênh vào repo (docs/09) — cần làm trên máy Windows | Để nguồn kiến thức chung có đủ công cụ hậu kỳ |
| 8 | 30/09 | Nhịp đăng: 2 video/ngày (11:30, 19:30) hay ít hơn? ~200 credit Flow/video | Lịch + ngân sách |
| 14 | 30/09 | Bỏ người kể — nhưng Tuấn Thủy vẫn **xuất hiện nói thẳng vào máy** ở đầu (câu mở) và cuối (góc nhìn, mẹo, câu hỏi, 2 câu kết) như bản v3 đang làm, được không? Hay bỏ hẳn Tuấn Thủy khỏi video? | Tài liệu kênh yêu cầu Tuấn Thủy mở/kết; chủ kênh nói "không phải là người kể nữa" |
| 15 | 30/09 | Nếu Veo đọc tiếng Việt không chuẩn: phương án dự phòng là lồng tiếng OmniVoice **riêng từng nhân vật** (cần 1 đoạn giọng mẫu ~10 s cho mỗi nhân vật) — đồng ý không? Có sẵn giọng mẫu nào? | Rủi ro lớn nhất của kiểu thoại |
| 10 | 30/09 | Tên series ("Sổ Tay Sầu Riêng Tuấn Thủy", đánh số tập) — dùng hay không? | Nhận diện |

## Đã trả lời
| # | Câu hỏi | Trả lời (30/09/2026) |
|---|---|---|
| 1 | Bật chia sẻ video mẫu | Đã bật; mạng cloud chặn Drive nên chủ kênh **tải file trực tiếp vào phiên** → đã phân tích (docs/02b) |
| 2 | Tuấn Thủy hay Tuấn Thúy | **Nông Sản Tuấn Thủy** |
| 3 | Duyệt lời 3 kịch bản | "Sửa" → đã làm v2, chờ chi tiết (#3b) |
| 4 | Thêm nhân vật mới | **Đồng ý** — Chú Tư, Út Nhỏ, Anh Sáu Tài, Bà Năm Cân |
| 5 | Kịch bản 30/09-A viết lại? | (chưa trả lời riêng — gộp vào #3b) |
| 6 | Một nguồn kiến thức | **Dùng chung một nguồn kiến thức mới** → repo GitHub (docs/09) |
| 9 | Người mua phụ vô danh | Đã thay bằng Út Nhỏ, không còn cần hỏi |
| 3b | Sửa kịch bản gì | Không nêu thêm (mục 4 để trống) → áp dụng các quyết định 11–13, viết lại v3 |
| 7 | Chữ lớn trên màn hình | Đã làm trong `tools/dung_video_v3.py` (không cần sửa Remotion) |
| 11 | Nhịp cắt | **(a) cắt + phóng to trong clip** → `cat` trong canh.json + `dung_video_v3.py` |
| 12 | Phụ đề karaoke | **Có** → 2–3 chữ IN HOA, chữ đang nói vàng #F2CD41 |
| 16 | Làm thử clip S01 | Chủ kênh chọn **NSTT-20261001-B làm video đầu tiên** và nhờ Claude làm thử S01 trên Flow → Claude KHÔNG vào được Flow (cần tài khoản Google của chủ kênh, mạng cloud chặn) → đã gửi hướng dẫn 2 bước (ảnh Út Nhỏ + prompt S01), chờ chủ kênh gửi clip |
| 13 | Nhân vật nói hay câm | **Nhân vật có thoại, không còn người kể** → kịch bản v3 |
