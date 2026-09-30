# 09 — Một nguồn kiến thức chung (chủ kênh chốt 30/09/2026)

## Nguyên tắc
- **Repo GitHub `nongsantuanthuy-cloud/nstt` là nguồn DUY NHẤT** cho: tài liệu (`docs/`), kịch bản (`kich_ban/*/canh.json, kich_ban.md, seo.md, trang_thai.md`),
  nhật ký (`nhat_ky/`), câu hỏi (`CAU_HOI_CHO_CHU_KENH.md`), công cụ (`tools/`, `hau_ky/src/`), skill (`.claude/skills/`).
- Máy chủ kênh (`D:\CLAUDE DU AN NSTT\kenh nstt`), phiên cloud, phiên mới — ai cũng **`git pull` đầu phiên, `git push` cuối phiên**.
- File nặng KHÔNG đưa lên git (xem `.gitignore`): clip Veo, wav, mp4, OmniVoice, `tools/node/`, `node_modules/`, token `bi_mat/`.
  → File nặng giữ trên máy + sao lưu Drive `NSTT/kich_ban/<ma>/`.
- Drive `NSTT/docs` chỉ giữ tài liệu gốc của chủ kênh + video mẫu. Kiến thức mới ghi vào repo, không ghi 2 nơi.
- Skill dự án: `.claude/skills/nstt-san-xuat-video/SKILL.md` (Claude Code tự nạp khi mở repo). Skill cũ đồng bộ trong tài khoản
  vẫn dùng được nhưng **repo đúng hơn** nếu mâu thuẫn.

## Việc 1 lần trên máy chủ kênh (gộp thư mục cũ vào repo)
Mở Claude Code trong `D:\CLAUDE DU AN NSTT\kenh nstt` và dán yêu cầu:
> "Gộp thư mục này vào repo GitHub nongsantuanthuy-cloud/nstt theo docs/09 trong repo: giữ bản repo cho CLAUDE.md, kich_ban mới, nhat_ky;
> đưa docs 03/05/07/08/09 cũ, tools/*.py, hau_ky/src, kich_ban/NSTT-20260929-MAU/canh.json lên; không đưa file nặng; commit và push."

Lệnh tương đương (PowerShell, trong thư mục đó; cần Git for Windows):
```powershell
git init
git remote add origin https://github.com/nongsantuanthuy-cloud/nstt.git
git fetch origin
git checkout -b may-chu-kenh
git add .gitignore     # lấy .gitignore từ repo trước: git checkout origin/claude/kind-turing-suxd5o -- .gitignore
git add docs tools hau_ky/src kich_ban nhat_ky CLAUDE.md
git commit -m "Đưa kiến thức + công cụ trên máy lên repo"
git push -u origin may-chu-kenh
```
Sau đó phiên cloud sẽ gộp `may-chu-kenh` với nhánh làm việc, xử lý trùng tên file (docs cũ trên máy dùng số 03/05/07/08/09 — sẽ đối chiếu nội dung, giữ bản đầy đủ hơn).

## Đầu mỗi phiên (mọi nơi)
1. `git pull`
2. Đọc `CLAUDE.md` → nhật ký mới nhất → `CAU_HOI_CHO_CHU_KENH.md`.
## Cuối mỗi phiên
1. Ghi `nhat_ky/YYYY-MM-DD.md` (nếu đã có file cùng ngày thì thêm mục "Phiên N").
2. Cập nhật `docs/` với kiến thức mới, `trang_thai.md` từng video.
3. `git add -A && git commit && git push`.
