# Trạng thái — NSTT-20261001-B

**ĐÃ DUYỆT — CHỜ ĐĂNG** (chủ kênh "DUYỆT NSTT-20261001-B" 01/10/2026) — `ban_dung/NSTT-20261001-B.mp4`, 124,6 s, −14,4 LUFS, Whisper 20/20 đạt.
Bản duyệt: không chữ lớn, phụ đề chân y=1245, logo (36, 290). Chủ kênh tự đăng theo `seo.md`.
S11 đã tạo lại (chủ kênh tạo tay, khớp 100%). S16 KHÔNG cần tạo lại: Veo nói đủ câu, Whisper VAD cắt mất nửa đầu
→ `moc_tu_whisper.py` nay tự nghe lại không VAD khi điểm thấp (S16 khớp 78%, sai do model small nghe nhầm chữ).

- [x] Kịch bản v3.3 (giá chốt 65k, câu chào/kết mới, 20 cảnh — S18+S19 là câu kết tách đôi) — `kiem_tra_kich_ban.py`: OK
- [x] Chủ kênh duyệt từng cảnh S01–S05; từ S05 cho làm hết không cần hỏi
- [x] 20/20 clip Flow (Veo 3.1 Lite, 8 s; S01 10 s) trong `clip_veo/` — xem `flow_tien_do.md`
- [x] Whisper (small, CPU) — 18/20 đúng lời; **S11 sai lời** (Veo nói "Dạ. Con biết. Cứ uống trà đi đó"), **S16 thiếu nửa đầu câu**
- [x] Soát khung hình 20 clip: đúng mặt/áo, không chữ lạ, không người lạ
- [x] Dựng `ban_dung/NSTT-20261001-B.mp4` — 117,8 s, 1080×1920, −14,4 LUFS, phụ đề karaoke theo mốc Whisper
- [x] Tạo lại S11 (Flow chặn tự động → chủ kênh tạo tay; clip 81842a70), S16 giữ nguyên
- [x] Chạy lại Whisper + dựng lại (124,6 s)
- [x] Chủ kênh DUYỆT video (01/10/2026)
- [ ] Đăng (chỉ sau chữ DUYỆT)
