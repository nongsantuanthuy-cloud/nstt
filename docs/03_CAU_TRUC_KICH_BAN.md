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

## 6. Bản 4 — CHUẨN HIỆN HÀNH từ 30/09/2026: nhân vật tự thoại (`"kieu": "thoai"`)
Chủ kênh chốt: (a) cắt + phóng to trong clip · phụ đề karaoke · nhân vật có thoại, bỏ người kể.
Các mục 1–4 ở trên (người kể UV07) chỉ còn để tham khảo cho kịch bản cũ.

**Khung:** giữ thứ tự HOOK → CAU_MO → BOI_CANH → VONG_LAP → LEO_THANG → DINH_DIEM → HOA_GIAI → GOC_NHIN → MEO →
CAU_HOI_2_PHE → KET_1 → KET_2; 18–24 clip. Phần truyện (HOOK→HOA_GIAI) do nhân vật nói với nhau;
phần GOC_NHIN→KET do Tuấn Thủy/Em Tuấn nói thẳng vào máy.

**Quy tắc thoại:**
- 1 clip Veo 8 s = tối đa **26 âm tiết** và tốt nhất **1 người nói** (tối đa 2 lượt). Câu dài → tách clip.
- Văn nói miền Nam–Tây Nguyên tự nhiên: "con", "cô", "má", "nha", "hả", "lẹ", "nè". Số vẫn **viết bằng chữ**.
- Bảng tính lời lỗ do nhân vật nói (Út Nhỏ, Chú Tư, Bà Tám tính giùm) + `chu_man_hinh` hiện số.
- Không lời thoại trong 1 clip → Veo ghi "Nobody speaks." (clip đặc tả/không khí, dùng ~2,5 s).

**Mẫu prompt thoại:**
```
Photorealistic cinematic footage, warm earthy brown-golden color grade, 35mm film look, shallow depth of field, realistic human motion, natural lip-sync. Setting: <bối cảnh>. <Tên Flow + mô tả>, <hành động>. <Tên> says <giọng>: "<câu tiếng Việt>" Then <Tên 2> says <giọng 2>: "<câu>" Sound: <âm thanh nền>. All speech is in Vietnamese only. No music, no subtitles, no on-screen text.
```

**`canh.json` v3 — mỗi cảnh:**
```json
{"so": "S01", "phan": "HOOK", "boi_canh": "bai_can", "nhan_vat": ["Co Hai", "Thang Lanh"],
 "thoai": [{"nv": "Co Hai", "cau": "Bao phân năm chục ký, sao cân chỉ có bốn bảy ký rưỡi vậy con?"}],
 "cat": ["dac_ta", "can"],            // góc hậu kỳ: toan | can | dac_ta — chia đều đoạn dùng
 "chu_man_hinh": "50 KÝ → 47,5 KÝ ?", // tùy chọn
 "tam_x": 0.5, "dung": [0.4, 5.2],    // tùy chọn, chỉnh sau khi xem clip thật
 "prompt_flow": "..."}
```
Nhịp: mỗi clip dùng ~3–6 s, chia 2–3 góc → mỗi góc 1,5–3 s (gần nhịp 2,3 s của video mẫu) mà không tốn thêm credit.
