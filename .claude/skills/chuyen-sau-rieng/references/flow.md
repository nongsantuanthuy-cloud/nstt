# Thao tác Google Flow bằng Claude in Chrome

Rút từ lần làm NSTT-20261001-B (01/10/2026). Giao diện Flow thay đổi thường xuyên — luôn chụp màn hình / `find`
để xác nhận trước khi bấm.

## Chuẩn bị
- Nạp công cụ Chrome một lần: `tabs_context_mcp, navigate, computer, find, javascript_tool, browser_batch,
  get_page_text, file_upload`. Tab có thể bị đổi id giữa chừng ("not in Claude's tab group") → gọi lại
  `tabs_context_mcp {createIfEmpty:true}`.
- Chrome phải **tắt "Hỏi nơi lưu trước khi tải xuống"** (Cài đặt → Tải xuống). Nếu bật, mỗi lần tải mở hộp thoại
  "Lưu thành" nằm ngoài trang → Claude không thấy, file không về. Dấu hiệu: bấm 720p mà Downloads không có file mới.
- Mất mạng (DNS lỗi, máy có VPN WireGuard) → dừng, nhờ chủ kênh bật lại mạng; ghi tiến độ vào `flow_tien_do.md`.

## Tạo nhân vật Flow (khi thiếu)
1. Mục **Nhân vật → Nhân vật mới → Thêm từ dự án → Tải nội dung lên**. Ô `input[type=file]` chỉ xuất hiện tạm;
   nếu `find` không thấy, cài bẫy JS để giữ nó lại rồi dùng `file_upload`:
   ```js
   const orig=HTMLInputElement.prototype.click;
   HTMLInputElement.prototype.click=function(){ if(this.type==='file'){ if(!this.isConnected){this.style.display='none';document.body.appendChild(this);} return;} return orig.call(this); };
   ```
2. Dùng ảnh 1 người, không chữ (`thuong_hieu/nhan_vat/*.png`), không dùng ảnh ghép có chú thích.
3. Đặt tên đúng tên Flow (không dấu: `Chu Nam`, `Ut Nho`…), điền "Thông tin nhân vật" = mô tả ngoại hình + giọng
   (lấy từ `docs/01`), bấm **Xong**.

## Cài đặt trước mỗi lượt tạo
- Ô nhập ở đáy trang; nút chip "Video · 720p · 8 giây · x1" mở menu: chọn **Video**, **Thành phần**, **16:9**,
  **Veo 3.1 - Lite**, **x1** → dòng "Quá trình tạo sẽ tốn **10** tín dụng". Thấy 12 = đang Omni 1.1 Flash → đổi lại.
- Nếu ô nhập hiện chip **"Tác nhân"** đang bật (chế độ agent) thì bấm để tắt — chế độ agent tốn 15 tín dụng.
- Bảng chat "Phiên không có tiêu đề" bên phải che bố cục → đóng bằng nút "Đóng".

## Gửi 1 cảnh
Cách chắc ăn nhất (đã chạy ổn):
1. Nạp `scripts/flow_helpers.js` (dán vào `javascript_tool`, thay `window.__P` bằng prompt các cảnh cần làm —
   tạo từ canh.json: `{ "S06": {"p": prompt_flow, "nv": [nhan_vat...]}, ... }`).
2. `await __prep('S06')` → gắn nhân vật + dán prompt, trả "prompt ok".
3. Kiểm tra bằng zoom ảnh ô nhập (đủ chip nhân vật), rồi bấm nút **"Bắt đầu tạo"** (tìm bằng `find`) hoặc `__submit()`.
4. Ô nhập trống lại = đã gửi. Còn chữ = chưa gửi, xem lỗi.

Lưu ý:
- Mỗi lệnh `javascript_tool` tối đa 45 giây; tab chạy nền làm `setTimeout` chậm → **mỗi lệnh chỉ 1 cảnh**
  (hoặc 1 bước), không gộp vòng lặp nhiều cảnh.
- Lần đầu sau khi tải trang, nút "+" hay không mở bảng chọn → bấm lại; ô tìm kiếm thành phần đôi khi báo
  "không tìm thấy" → tải lại trang rồi gõ bằng bàn phím thật (`computer type`).
- Bấm vào tên nhân vật trong danh sách là **gắn luôn** và đóng bảng; đừng bấm thêm "Thêm vào câu lệnh"
  (cú bấm thứ hai rơi vào clip phía sau và mở trình chỉnh sửa).
- Gửi dồn dập nhiều cảnh trong vài phút có thể bị Flow chặn "hoạt động bất thường" — khi đó dừng hẳn, chủ kênh
  tạo tay theo file `tao_lai_*.txt`.

## Ghép clip với cảnh
Ô thu nhỏ (`img[alt="Hình thu nhỏ của video đã tạo"]`) xếp mới nhất trước. Bấm từng ô → đọc
`document.body.innerText.match(/says[^"]*"([^"]*)"/)[1]` + `location.pathname` (id clip) → ghi vào `flow_tien_do.md`.
Ô lỗi ("Không thành công") không có ảnh thu nhỏ video.

## Tải 720p
- Mở `https://flow.google.com/project/<dự án>/edit/<id>`, chờ ~6–8 giây.
- Nút tải **"Tải nội dung nghe nhìn xuống"** nằm cạnh nút **"Chuyển vào thùng rác"** (cách ~42 px). Đừng bấm theo
  tọa độ đoán; cách an toàn:
  ```js
  const b=[...document.querySelectorAll('button')].find(e=>(e.getAttribute('aria-label')||'')==='Tải nội dung nghe nhìn xuống'); b.focus();
  ```
  rồi nhấn phím `Return` (hoặc `space`), kiểm tra `document.querySelectorAll('[role=menuitem]').length === 4`.
  Nếu dùng tọa độ thì phóng to (zoom) thanh công cụ trước và bấm đúng biểu tượng mũi tên tải.
- `find "720p menu item (Kích thước gốc)"` → bấm ref → chạy `scripts/nhan_clip.ps1 -So Sxx`.
- Tên file Flow đặt theo nội dung ("Man_pours_tea_for_man_...mp4") — đừng dựa vào tên để đoán cảnh.
