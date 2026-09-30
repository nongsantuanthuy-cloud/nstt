# 03 — Cấu trúc kịch bản 2 phút (theo từng khung)

Cập nhật 30/09/2026 (bản 2 — thêm hồi HÓA GIẢI, vòng lặp mở, hook hành động).

## 1. Khung thời gian chuẩn (~120 s, 19–20 cảnh, mỗi cảnh 1 clip Veo 8 s, lời 5,5–7 s)
| # | Phần (`phan`) | Giây | Mục đích | Quy tắc hình |
|---|---|---|---|---|
| 1 | `HOOK` | 0–6 | Con số + mâu thuẫn trong 1 câu | Hành động + tiếng động mạnh ngay khung đầu (cân kêu, sọt rơi); cận |
| 2 | `CAU_MO` | 6–12 | Câu mở cố định | `Nguoi Ke` đi tới, gật đầu, miệng khép |
| 3–5 | `BOI_CANH` | 12–30 | Ai, ở đâu, vì sao tin nhau | Vườn đẹp, trái đẹp, bắt tay |
| 6 | `VONG_LAP` | 30–36 | "Nhưng…" — gieo nghi ngờ, giữ người xem qua mốc 30 s | Cận chi tiết đáng ngờ (màn hình cân không đọc được, ánh mắt) |
| 7–10 | `LEO_THANG` | 36–60 | Sự việc xấu đi, 2 phe căng | Kho/bãi cân đang hoạt động, biểu cảm mạnh, không lời thoại |
| 11–12 | `DINH_DIEM` | 60–74 | Lật tẩy + **bảng tính lời lỗ** (tối đa 2 cảnh) | B-roll sọt/cân; số hiện chữ lớn khi hậu kỳ |
| 13–14 | `HOA_GIAI` | 74–88 | Hai bên ngồi lại, phe "xấu" có lý do; giải pháp công bằng | Ngồi ghế nhựa đỏ, bắt tay, cười |
| 15 | `GOC_NHIN` | 88–94 | Tuấn Thủy rút ra bài học, không phán xét ai | `Nguoi Ke` trầm ngâm cạnh cây |
| 16–17 | `MEO` | 94–107 | 1–2 mẹo cụ thể làm được ngay | `Nguoi Ke` / `Em Tuan` làm mẫu |
| 18 | `CAU_HOI_2_PHE` | 107–113 | Câu hỏi 2 phe → bình luận | Nhân vật chính nhìn xa |
| 19 | `KET_1` | 113–120 | Câu kết 1 cố định | `Nguoi Ke` + `Em Tuan` xếp sọt |
| 20 | `KET_2` | 120–126 | Câu kết 2 cố định | `Nguoi Ke` gật đầu, đi xa |

Giới hạn cứng: tổng ≤ 2:58 (Shorts ≤ 3 phút). Mục tiêu 1:55–2:10.

## 2. Quy tắc viết lời
- Mỗi câu 18–27 âm tiết (≈ 5,5–7 s với UV07). Công cụ `tools/kiem_tra_kich_ban.py` ước tính.
- **Số viết bằng chữ**: "mười ba triệu rưỡi", "ba nghìn ký". Không có chữ số trong `loi`.
- Tiền cộng trừ phải đúng → ghi phép tính trong `bang_tinh` và kiểm lại.
- Không tên thật kho/người/doanh nghiệp/địa danh cấp xã. Chỉ "Đắk Lắk", "vườn Cô Hai", "kho Bảy Lợi".
- Văn mộc mạc: "bà con", "dạt", "ép giá", "bầm trầy", "toang", "sập giá", "chốt kèo".
- Không chửi, không miệt thị vùng miền, không kêu gọi tẩy chay. Phe "xấu" luôn có 1 lý do thật.
- Đổi 1 câu → đọc lại câu trước/sau để mạch truyện khớp.
- Tuấn Thủy xưng "Tuấn Thủy", gọi khán giả "bà con".

## 3. Quy tắc prompt Flow (Veo 3.1 Lite, 16:9, x1)
```
Photorealistic cinematic footage, warm earthy brown-golden color grade, 35mm film look, shallow depth of field, realistic human motion. Setting: <bối cảnh cụ thể>. <Tên Flow + mô tả nguyên văn + hành động>. Sound: <âm thanh ASMR>. No dialogue, no music, no on-screen text.
```
- Có nhân vật → thêm "mouth closed" / "Mouths closed, body language only".
- Có điện thoại/cân → "Phone screen not visible" / "Scale display not readable".
- Hành động phải có chuyển động (tránh lỗi "Không tạo được âm thanh").

## 4. Định dạng `canh.json`
```json
{
  "ma_video": "NSTT-YYYYMMDD-A",
  "chu_de": "...",
  "tieu_de_tam": "...",
  "ghi_chu": "...",
  "bang_tinh": { "ten_dong": "phép tính = kết quả", "...": "..." },
  "canh": [
    {
      "so": "S01",
      "phan": "HOOK",
      "boi_canh": "vuon | kho | bai_can",
      "nhan_vat": ["Co Hai"],
      "loi": "Lời đọc, số viết bằng chữ.",
      "chu_man_hinh": "(tùy chọn) chữ lớn hiện khi hậu kỳ, ví dụ 13.500.000đ",
      "prompt_flow": "Photorealistic ... No dialogue, no music, no on-screen text."
    }
  ]
}
```
`boi_canh` dùng để mượn tiếng nền sạch khi clip có tiếng nước ngoài. `bai_can` = bãi cân/sân vườn có xe tải
(nếu `hau_ky_nstt.py` chỉ hiểu `vuon`/`kho` thì map `bai_can` → `vuon`). `chu_man_hinh` là trường mới —
cần bổ sung vào `hau_ky/src/NsttVideo.tsx` (xem CAU_HOI).

## 5. Bản 3 (30/09/2026) — bài học từ phân tích thật video mẫu (docs/02b)
Đã áp dụng ngay (không cần đổi công cụ):
- Giây 0 phải là **hành động xung đột** (chặn xe, đặt bao lên cân, điện thoại rung) — không mở bằng cảnh tĩnh.
- Mỗi video có **1 bằng chứng nhìn thấy được** (bao phân, phiếu cân, giấy cọc, tin nhắn) và **1 lần lật ngược** nhẹ.
- Phe "tưởng xấu" được cho lý do / hóa ra không xấu (video mẫu: thương lái ngay thẳng, thủ phạm là người thứ ba).
- Câu chốt đạo lý ngắn trước phần góc nhìn.
- Không logo đài/báo, không viết tắt số ("2T"), phụ đề lấy đúng từ `loi`.

ĐỀ XUẤT chờ chủ kênh (cần sửa hậu kỳ trên máy — CAU_HOI #11, #12):
- **Nhịp cắt 2–3 s**: video mẫu 50 cảnh/116 s; NSTT 20 cảnh × 6 s. Cách rẻ: trong mỗi clip Veo 8 s, hậu kỳ cắt 2–3 đoạn
  + phóng to (toàn → cận mặt → đặc tả), không tốn thêm credit. Cách đắt: thêm clip đặc tả vật chứng (~+5 clip/video = +50 credit).
- **Phụ đề karaoke** 2–3 chữ IN HOA, chữ trắng viền đen, từ đang đọc đổi vàng #F2CD41, đặt ~75% chiều cao.
