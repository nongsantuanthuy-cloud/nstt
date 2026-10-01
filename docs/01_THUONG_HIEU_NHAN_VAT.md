# 01 — Thương hiệu & Dàn nhân vật

Nguồn: Drive `NSTT/docs/thông tin kênh nông sản tuấn thủy`, `thuong_hieu/nhan vat/nhan_vat.md`, skill `nstt-san-xuat-video`. Cập nhật 30/09/2026 (v2: chốt tên **Nông Sản Tuấn Thủy**; thêm 4 nhân vật mới).

## 1. Định vị
- **Tên kênh:** Nông Sản Tuấn Thủy (NSTT) — chủ kênh chốt 30/09/2026, KHÔNG viết "Tuấn Thúy" · Đắk Lắk (Tây Nguyên) · Hotline/Zalo **0392.547.547**.
- **Slogan:** "Review Chuyện Sầu Riêng".
- **Ngách:** góc khuất thị trường sầu riêng — drama nhà vườn / thương lái / chủ kho / cò. KHÔNG làm kỹ thuật canh tác thuần.
- **Khán giả:** nhà vườn, thương lái, tài xế chở hàng, chủ vựa/kho, người quan tâm giá sầu.
- **Phương châm:** không đứng về phe nào; mở đầu gay gắt → kết thúc êm đẹp, hai bên cùng vui, người xem thỏa mãn.
  Tuấn Thủy mở đầu giới thiệu chuyện, cuối video khuyên chọn đơn vị uy tín / nhà vườn trung thực,
  mời kết nối NSTT **nhẹ nhàng, không áp đặt, không phô trương**.
- **Giọng văn:** mộc mạc, dân dã, thật ("bầm trầy", "toang", "sập giá", "dạt", "ép giá").
- **Hình ảnh:** AI photorealistic, tông ấm vàng–nâu đất, sương gió; khung dọc 9:16; có nhãn "nội dung AI".

## 2. Nhận diện
- Logo: `thuong_hieu/logo/logo_chinh_goc.webp` (gốc) + `thuong_hieu/logo/logo_nstt_400.png` (tròn, nền trong — dùng khi dựng video). Slogan trên logo: "Tinh hoa nông sản Việt".
- Màu: **xanh #024815** + **vàng cơm sầu #F2CD41**. Không dùng tông nâu cho đồ họa.
- Câu mở cố định: *"Chào bà con. Chuyện nghề sầu riêng hôm nay, Tuấn Thủy kể bà con nghe."*
- Câu kết cố định:
  1. *"Có hàng cần bán, bà con cứ gọi Tuấn Thủy. Mình cùng trao đổi rõ ràng, thuận mua vừa bán, ai cũng vui."*
  2. *"Cảm ơn bà con đã tin tưởng và hẹn gặp lại trong những vườn sầu riêng."*

## 3. Dàn nhân vật — TỪ 30/09/2026 NHÂN VẬT TỰ THOẠI (chủ kênh chốt)
- Không còn người kể giọng đọc (UV07). Câu chuyện diễn ra bằng **lời thoại của nhân vật**, Veo tạo tiếng + khẩu hình.
- **Tuấn Thủy** (`Nguoi Ke`) vẫn xuất hiện đầu/cuối nhưng là **nhân vật nói thẳng vào máy** (kiểu vlog chủ kênh):
  câu mở, góc nhìn, mẹo, câu hỏi, 2 câu kết — không lồng tiếng đè lên cảnh khác.
- Mỗi nhân vật có **giọng cố định** (mô tả chèn vào prompt, xem bảng giọng dưới) để Veo giữ đồng nhất.

| Tên Flow | Giọng (chèn sau "says") |
|---|---|
| `Nguoi Ke` | in a warm, clear young female voice with a Southern Vietnamese accent |
| `Em Tuan` | in a friendly young male voice with a Southern Vietnamese accent |
| `Chu Nam` | in a warm, slightly husky middle-aged male voice with a Southern Vietnamese accent |
| `Bay Loi` | in a deep, gruff male voice with a Southern Vietnamese accent |
| `Thang Lanh` | in a fast, smooth-talking male voice with a Southern Vietnamese accent |
| `Chu Tu` | in a slow, calm elderly male voice with a Southern Vietnamese accent |
| `Ut Nho` | in a bright young female voice with a Southern Vietnamese accent |
| `Sau Tai` | in a hearty male voice with a Southern Vietnamese accent |
| `Ba Tam` | in a firm elderly female voice with a Southern Vietnamese accent |

Bảng ngoại hình (giữ nguyên):
Tên Flow viết không dấu. Mỗi prompt phải gọi tên + chèn nguyên văn mô tả.

| Nhân vật | Tên Flow | Vai trò | Mô tả chèn vào prompt |
|---|---|---|---|
| Tuấn Thủy (chủ kênh, ảnh thật) | `Nguoi Ke` | Người kể, xuất hiện câu mở, góc nhìn, mẹo, câu hỏi, kết | the young woman in the reference: white collared shirt, beige wide-leg trousers, black belt, hair in a low bun |
| Em Tuấn (ảnh thật) | `Em Tuan` | Thương lái trẻ phe NSTT, làm ăn đàng hoàng; cảnh kiểm hàng, cảnh kết | the young man in the reference: short spiky black hair, black polo shirt, dark cargo pants |
| **Chú Năm** (thay Cô Hai từ 30/09, **ảnh thật chủ kênh** `thuong_hieu/nhan_vat/chu_nam_goc.webp`) | `Chu Nam` | Chủ vườn chất phác, hiền, dễ tin người; ba của Út Nhỏ | Chu Nam, the man in the reference: around 55, short messy grey-black hair, tanned weathered face, faded light grey striped long-sleeve work shirt, conical hat on his back |
| Bảy Lợi | `Bay Loi` | Chủ kho cứng rắn, hay ép giá, bắt dạt | Bay Loi, a man around 55, plain camouflage bucket hat with no badge, dark denim shirt, thick silver chain, tattoos, arms crossed |
| Thắng Lanh | `Thang Lanh` | Cò trung gian, nói ngọt, hứa giá cao rồi biến mất | Thang Lanh, a man around 35, slicked hair, thin mustache, tight black T-shirt, gold chain and gold watch, two phones, motorbike |
| Chú Tư (mới) | `Chu Tu` | Nhà vườn nam lão làng, hàng xóm Cô Hai, hiền, "chốt lẽ phải" | Chu Tu, a man around 60, faded plaid shirt, checkered krama scarf around his neck, soft bucket hat, weathered kind face |
| Út Nhỏ (mới, **ảnh thật chủ kênh cung cấp** `thuong_hieu/nhan_vat/ut_nho_goc.webp`) | `Ut Nho` | Con gái út Chú Năm, phụ vườn, bán hàng qua Zalo/Facebook | Ut Nho, the young woman in the reference: black square glasses, long black hair in a high ponytail with bangs, pink plaid long-sleeve shirt, black cargo pants, rubber boots, work gloves, conical hat on her back |
| Anh Sáu Tài (mới) | `Sau Tai` | Tài xế xe tải chở sầu — nhân chứng trung lập | Sau Tai, a man around 40, truck driver, orange high-visibility work shirt, towel around his neck, cap |
| Bà Tám Cân (mới) | `Ba Tam` | Giữ trạm cân đầu xã / cân đối chứng — "trọng tài" | Ba Tam, a woman around 65, grey hair in a bun, light blue blouse, reading glasses hanging on a cord |

Út Nhỏ đã có ảnh (30/09). 3 nhân vật mới còn lại **chưa có ảnh tham chiếu trong Flow** → tạo theo `thuong_hieu/nhan_vat_moi.md` trước khi dựng clip có họ.

**Không dùng:** `Co Hai` (đã đổi thành Chú Năm 30/09), `Chu Ba`, `Ong Sau Cu`, ảnh `bay_loi_goc_co_huy_hieu.png` (nón có huy hiệu — clip nào lòi huy hiệu phải tạo lại).

## 4. Lưu ý khi tạo clip
- Luôn ghi `Setting: ...` (Veo hay chép nền ảnh tham chiếu).
- Tư thế đời thường: ghế nhựa đỏ thấp, ngồi xổm, đứng cạnh xe còn chở sầu. KHÔNG ngồi trên thùng xe / tailgate.
- Kho phải đang hoạt động (có người làm, có hàng).
- Xem lại từng clip: tư thế lỗi, chữ sai chính tả, người lạ, huy hiệu → tạo lại.
- Nhân vật "xấu" (Thắng Lanh, Bảy Lợi) không bị bôi nhọ tuyệt đối — mỗi video nên cho họ một lý do/khó khăn thật, và kết có hậu (xem docs/03).
