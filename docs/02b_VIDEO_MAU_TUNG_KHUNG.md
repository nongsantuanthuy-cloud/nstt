# 02b — Video mẫu "Cái cân biết nói": phân tích THẬT từng khung (50 cảnh)

Phân tích ngày 30/09/2026 từ file chủ kênh tải lên (`video mẫu.mp4`, Drive id `1AoZMQ-d2VdcNr0OIr_siuGvhKrfeiTNe`).
Công cụ: `tools/trich_khung_hinh.py` (ngưỡng 0.25) + đọc phụ đề cháy trên hình 3 khung/giây.
Ảnh từng cảnh: `docs/hinh_video_mau/canh_XX-YY.jpg` (số góc trái = cảnh_giây). Lời thoại dựng lại từ phụ đề
(phụ đề của video mẫu có lỗi chính tả, đã sửa trong ngoặc).

## 1. Thông số kỹ thuật
| Mục | Giá trị | So với NSTT |
|---|---|---|
| Độ dài | 1:56 (116 s) | NSTT mục tiêu 1:50–2:10 ✓ |
| Khung | 576×1024, 9:16, 30 fps | NSTT 1080×1920 (nét hơn) |
| Số cảnh (lần cắt) | **50** → trung bình **2,3 s/cảnh**, ngắn nhất 0,7 s, dài nhất 5,5 s | NSTT hiện 19–20 cảnh × ~6 s → **chậm gấp 2,5 lần** |
| Âm thanh | Thoại nhân vật (khẩu hình), có khoảng lặng thật (< −40 dB) giữa các câu → **không có nhạc nền liên tục** | NSTT: 1 giọng kể, không nhạc ✓ |
| Độ lớn | −22,4 LUFS (nhỏ) | NSTT −14 LUFS (to, rõ hơn) ✓ |
| Phụ đề | Karaoke **2–3 chữ/lần, IN HOA**, font đậm hẹp, chữ trắng viền đen, **từ đang đọc đổi màu xanh ngọc**, nằm ~75% chiều cao | Nên áp dụng (màu vàng #F2CD41 thay xanh ngọc) |
| Watermark | Dấu ✦ góc dưới phải (Veo/Gemini) suốt video | NSTT phải xử lý đúng luật, không che watermark dịch vụ khác |
| Logo lạ | **Logo VTV góc trên trái cảnh 44–46 (96–106 s)** — gắn logo đài truyền hình giả | ⛔ NSTT tuyệt đối không dùng logo đài/báo |
| Mở/kết thương hiệu | Không có, không hotline, không kêu gọi | NSTT có câu mở/kết + hotline ✓ |
| Màu | Trời âm u, ánh sáng mềm, xanh lá chủ đạo, tự nhiên | NSTT ấm vàng–nâu → nhận diện riêng ✓ |

## 2. Nhân vật (tất cả có thoại, khẩu hình)
| Nhân vật | Ngoại hình | Vai |
|---|---|---|
| Ông Sáu | ~60, nón tai bèo xanh rêu, áo caro xanh nhạt, khăn rằn đen trắng, ủng cao su | Nhà vườn bị hụt ký |
| Hùng (thương lái) | ~40, sơ mi xanh đen (cảnh 25–26, 37, 43 lại mặc **áo thun** — lỗi nhất quán trang phục), quần jean, đồng hồ bạc | Người mua — **hóa ra ngay thẳng** |
| Con gái ông Sáu | ~28, áo khoác kaki xanh rêu, áo thun be, jean đen, cầm điện thoại | Người có bằng chứng (video quay cả buổi) |
| Tấn (nhân viên cân) | ~40, polo xám, nón lưỡi trai đen, túi đeo hông | **Thủ phạm**: đạp chân dưới bàn cân |
| Dân làng, công nhân | nón lá, áo bảo hộ | Đám đông chứng kiến |

## 3. Bảng từng cảnh
Ký hiệu cỡ cảnh: TC toàn cảnh · TR trung cảnh · CA cận · ĐC đặc tả · QV qua vai · POV góc nhìn điện thoại.

| # | Giây | Dài | Cỡ | Hình | Lời thoại (người nói) |
|---|---|---|---|---|---|
| 1 | 0,0 | 2,0 | TC | Đường bê tông giữa vườn sầu, xe tải nhỏ chở đầy sầu, công nhân, cân bàn | "Khoan!" (Ông Sáu, ngoài khung) |
| 2 | 2,0 | 4,0 | TR | Ông Sáu dang tay chặn đầu xe, tay cầm phiếu | "Khoan. Xe chưa được đi. Gần 2T sầu riêng của tui đâu mất rồi?" |
| 3 | 6,0 | 1,3 | QV | Hùng từ đuôi xe bước tới, cầm phiếu | "Ông coi kỹ…" (Hùng) |
| 4 | 7,3 | 1,1 | TR | Hùng đứng, phiếu trong tay | "…lại đi, phiếu cân in rõ…" |
| 5 | 8,3 | 1,7 | CA | Mặt Hùng gắt | "…ràng, đừng chặn xe rồi làm lớn chuyện." |
| 6 | 10,0 | 0,7 | ĐC | Tay lật sổ ghi chép + phiếu cân trên bàn gỗ, cuống sầu | "Tui ghi từng…" (Ông Sáu) |
| 7 | 10,7 | 3,6 | CA | Ông Sáu cầm sổ, nói | "…sọt, tổng số không sai một trái, sao phiếu lại hụt gần 2T." |
| 8 | 14,3 | 3,5 | TR | Con gái bước tới, ông Sáu cầm sổ | "Ba đưa sổ đây để con đối chiếu từng lượt cân với giờ quay." (Con gái) |
| 9 | 17,8 | 1,3 | POV | Tay mở thư viện video trên điện thoại + sổ | (lặng) |
| 10 | 19,2 | 3,5 | TR | Hùng chỉ vào đầu cân điện tử cạnh xe | "Cân này mới kiểm định tuần rồi, không thể…" (Hùng) |
| 11 | 22,6 | 1,0 | ĐC | Đầu cân điện tử, số đỏ | "…sai. Có khi…" |
| 12 | 23,7 | 1,5 | QV | Ông Sáu cầm sổ, Hùng quay lưng | "…ông ghi nhầm số sọt." |
| 13 | 25,1 | 3,0 | CA | Mặt ông Sáu ngỡ ngàng | "Tui làm vườn mấy [chục năm], không thể nhầm tới 2T hàng." (Ông Sáu) |
| 14 | 28,1 | 1,0 | TC | Công nhân, sọt, cân bàn, xe | — |
| 15 | 29,2 | 3,0 | TR | Tấn ghi phiếu cạnh đầu cân | "Trái lép, cuống dài, mất nước thì phải trừ hao chớ." (Tấn) |
| 16 | 32,1 | 1,5 | ĐC | Tay cầm phiếu in nhiệt từ cân | (lặng) |
| 17 | 33,7 | 5,5 | TR | Ông Sáu cầm phiếu cạnh cân, sọt đỏ | "Trừ kiểu gì mà mỗi sọt hụt cả 10 ký. Mức này vô lý, tui không chấp nhận." |
| 18 | 39,2 | 1,3 | TC | Đuôi xe tải giữa vườn, công nhân hai bên | — |
| 19 | 40,5 | 0,8 | TR | Ông Sáu bước ra chặn | — |
| 20 | 41,3 | 2,3 | CA | Mặt Hùng | "Không chấp nhận phiếu thì tui cho xe đi, tiền để tính sau." (Hùng) |
| 21 | 43,6 | 0,7 | TR | Hai người đối mặt (nghiêng) | — |
| 22 | 44,3 | 4,8 | CA | Mặt ông Sáu | "Hàng của tui chưa thanh toán đủ. Hôm nay không ai được chở khỏi [vườn]." (phụ đề sai "giường") |
| 23 | 49,2 | 2,9 | TR | Con gái đi giữa xe và cân | "Mọi người khoan cãi. Từ sáng con có quay…" |
| 24 | 52,1 | 1,2 | POV | Tay giơ điện thoại quay cảnh cân | "…toàn bộ quá trình cân hàng." |
| 25 | 53,3 | 3,7 | TR | Hùng nhìn điện thoại con gái chìa ra | "Vậy mở ra coi ngay. Tôi cũng muốn biết…" (Hùng) |
| 26 | 57,0 | 2,2 | TC | Con gái, Hùng khoanh tay, cân | "…rốt cuộc bên nào đang nói sai." |
| 27 | 59,2 | 3,5 | TR | Con gái bấm điện thoại | "Đây. Mỗi lần công nhân quay lưng, chú Tấn đều đạp chân dưới bàn cân." |
| 28 | 62,7 | 1,1 | POV | **Video trong khung điện thoại**: Tấn đứng cạnh cân | (lặng) |
| 29 | 63,8 | 1,8 | POV | Video trong điện thoại: chân mang dép đạp mép bàn cân | (lặng) |
| 30 | 65,6 | 3,5 | CA | Mặt ông Sáu sững sờ | "Đúng lúc đó số ký trên màn hình [tụt] xuống rõ ràng." |
| 31 | 69,2 | 2,0 | TR | Tấn đi tới, tay cầm phiếu | "Tôi chỉ vô tình chạm chân thôi." (Tấn) |
| 32 | 71,1 | 3,0 | TR | Con gái chìa điện thoại vào mặt Tấn | "Đừng vu oan cho tôi." (Tấn) / "Vô tình mà lặp lại hơn 20 lần." (Con gái) |
| 33 | 74,2 | 1,4 | POV | Điện thoại hiện 3 khung hình lặp lại | "Sao mỗi lần đạp là cân lại hụt ký?" |
| 34 | 75,5 | 1,6 | ĐC | Cực cận mắt Tấn | (lặng) |
| 35 | 77,1 | 3,8 | TR | Ông Sáu xếp hàng sầu dưới đất cạnh cân đồng hồ | "Lấy ngẫu nhiên 10 sọt cân lại bằng cân của hợp tác xã." |
| 36 | 80,9 | 1,5 | TR | Cân đồng hồ, xe, Hùng | "Được, cân ngay…" (Hùng) |
| 37 | 82,4 | 2,0 | CA | Mặt Hùng | "…trước mặt mọi người. Nếu cân cũ sai, tôi chịu trách nhiệm." |
| 38 | 84,4 | 1,6 | TC | Mọi người cân từng trái | — |
| 39 | 86,0 | 1,3 | TC | Dưới mái tôn: cân bàn, sọt, xe | — |
| 40 | 87,3 | 1,2 | ĐC | Đầu cân số đỏ + 2 phiếu có dấu đỏ | — |
| 41 | 88,5 | 1,0 | TR | Con gái ghi sổ cạnh Hùng | "Cân mới đủ…" (Con gái) |
| 42 | 89,5 | 2,4 | CA | Con gái cầm phiếu | "…ký, còn phiếu cũ mỗi sọt hụt 15 tới 20 ký." |
| 43 | 91,9 | 4,1 | CA | Hùng cầm phiếu, sửng sốt | "Cộng hết số sọt lại đúng gần 2T, không thể chối nữa." |
| 44 | 96,0 | 1,0 | TC | Đám đông dân làng, Tấn cúi đầu — **logo VTV** | — |
| 45 | 97,0 | 3,5 | CA | Hùng cầm phiếu ghi "HÙNG" hỏi Tấn — **logo VTV** | "Hãy nói cho tôi biết sự thật: ai bảo anh điều chỉnh cái cân để lấy tiền chênh lệch?" (Hùng) |
| 46 | 100,5 | 4,0 | CA | Tấn cúi đầu — **logo VTV** | "Không có ai đâu. Tôi tự làm và bán riêng phần thiếu hụt đó." (Tấn) |
| 47 | 104,5 | 1,5 | TR | Tấn đặt phiếu lên bàn inox trước đám đông | "Tôi xin lỗi tất cả mọi người." |
| 48 | 106,0 | 3,0 | TR | Hùng đưa phong bì cho ông Sáu ở bàn gỗ | "Tôi xin lỗi ông Sáu. Tôi thanh toán đủ số tiền còn thiếu ngay." (Hùng) |
| 49 | 109,0 | 3,8 | CA | Ông Sáu nhận tiền | "Tiền đủ là được. Làm ăn lâu dài mà mất chữ tín…" (Ông Sáu) |
| 50 | 112,8 | 3,2 | TC | Hai người ở bàn, xe tải, ông Sáu bước đi | "…thì chẳng còn gì." |

## 4. Cấu trúc thật (khác với bản mô tả trước)
| Hồi | Giây | Cảnh | Nội dung |
|---|---|---|---|
| Hook | 0–6 | 1–2 | Chặn xe + câu hỏi mất hàng — **xung đột trong 2 giây** |
| Đối đầu | 6–49 | 3–22 | Qua lại 6 lượt: nhà vườn (sổ tay) ↔ thương lái (phiếu, cân kiểm định) ↔ nhân viên cân (trừ hao). Leo thang tới "không ai được chở khỏi vườn" |
| Bằng chứng | 49–76 | 23–34 | Con gái có **video quay cả buổi** → chú Tấn đạp chân dưới bàn cân, lặp hơn 20 lần |
| Kiểm chứng | 77–96 | 35–43 | Lấy ngẫu nhiên 10 sọt, cân hợp tác xã trước mặt mọi người → mỗi sọt hụt 15–20 ký |
| Lật ngược | 96–106 | 44–47 | Thủ phạm là **nhân viên cân tự làm**, không phải thương lái → xin lỗi |
| Kết | 106–116 | 48–50 | Thương lái xin lỗi, trả đủ; câu chốt "mất chữ tín thì chẳng còn gì" |

## 5. Bài học cho NSTT (đã đưa vào docs/03 v3)
1. **Nhịp cắt nhanh 2–3 s/cảnh** là lý do chính giữ người xem. NSTT: mỗi câu lời (~6 s) nên có 2–3 góc (toàn → cận mặt → đặc tả tay/vật).
2. **Xung đột nói bằng hành động ngay giây 0** (chặn xe), không phải cảnh tĩnh.
3. **Lật ngược "người tưởng xấu hóa ra tốt"** (thương lái ngay thẳng, thủ phạm là người thứ ba) → khớp phương châm NSTT "không đứng về phe nào".
4. **Bằng chứng cụ thể, nhìn được**: video trong điện thoại, phiếu cân, cân đối chứng, lấy ngẫu nhiên 10 sọt.
5. **Đặc tả vật chứng** (chân đạp cân, phiếu in, màn hình cân) chèn 1 s — rẻ, không cần nhân vật.
6. **Phụ đề karaoke 2–3 chữ** giúp xem không cần bật tiếng.
7. Câu chốt đạo lý ngắn ở cuối ("mất chữ tín thì chẳng còn gì").

## 6. Những điều video mẫu làm SAI — NSTT tránh
- Gắn logo VTV giả → rủi ro vi phạm bản quyền/nhãn hiệu, mạo danh báo chí, dễ bị gỡ/khóa kênh.
- Trang phục nhân vật đổi giữa các cảnh (Hùng: sơ mi ↔ áo thun) → NSTT dùng ảnh tham chiếu cố định + kiểm từng clip.
- Phụ đề tự động sai ("giường", "tục", "chữ tính") → NSTT lấy phụ đề từ `loi` trong canh.json (đúng 100%).
- Viết tắt số "2T" gây mơ hồ (2 tạ hay 2 tấn?) → NSTT viết số đầy đủ.
- Âm lượng −22 LUFS nhỏ → NSTT giữ −14 LUFS.
- Không thương hiệu, không kêu gọi.

## 7. Khác biệt để NSTT không trùng video mẫu
Kịch bản NSTT-20261001-A (cân) cùng đề tài "cân sai" (đề tài chung của ngành, không ai giữ bản quyền) nhưng:
lật tẩy bằng **bao phân 50 ký**, không có video đạp chân; không có nhân viên cân gian; nhân vật, lời, bố cục khác hoàn toàn;
có người kể + bảng tính + mẹo. KHÔNG dùng: "đạp chân dưới bàn cân", "con gái quay video", "lấy ngẫu nhiên 10 sọt", câu "mất chữ tín thì chẳng còn gì".
