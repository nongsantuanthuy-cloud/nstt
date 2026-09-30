#!/usr/bin/env python3
"""Xuất trang HTML để chủ kênh đọc + duyệt kịch bản trên điện thoại (thay cho kich_ban.md khó xem).

    python3 tools/xuat_trang_duyet.py kich_ban/NSTT-A/canh.json kich_ban/NSTT-B/canh.json ... -o duyet.html

Trang đọc được cả kiểu v3 (thoai) và v2 (loi). Phiên Claude xuất bản trang bằng công cụ Artifact.
"""
import argparse, html, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from kiem_tra_kich_ban import TEN, giay, kieu, mmss  # noqa: E402

PHAN = {"HOOK": "Mở màn", "CAU_MO": "Câu chào", "BOI_CANH": "Bối cảnh", "VONG_LAP": "Nút thắt",
        "LEO_THANG": "Căng thẳng", "DINH_DIEM": "Đỉnh điểm", "HOA_GIAI": "Hóa giải", "GOC_NHIN": "Góc nhìn",
        "MEO": "Mẹo", "CAU_HOI_2_PHE": "Câu hỏi", "KET_1": "Kết", "KET_2": "Kết"}
GOC = {"toan": "toàn", "can": "cận", "dac_ta": "đặc tả"}
BOI = {"vuon": "vườn", "kho": "kho", "bai_can": "bãi cân"}
e = html.escape

CSS = """
<style>
/* Bố cục: 1 cột đọc như kịch bản quay phim; mỗi cảnh là 1 hàng có mốc giây bên trái */
:root{
  --bg:#f5f7f2; --paper:#ffffff; --ink:#17241b; --muted:#5c6b60; --line:#dde4da;
  --brand:#024815; --gold:#F2CD41; --gold-ink:#6b5200; --chip:#e8efe6;
  --f-display:"Barlow Condensed","Arial Narrow",sans-serif; --f-body:"Be Vietnam Pro",system-ui,sans-serif;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0f1511; --paper:#162019; --ink:#e7eee8; --muted:#9aab9e; --line:#27342b;
  --brand:#7fc493; --gold:#F2CD41; --gold-ink:#F2CD41; --chip:#1f2c23; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0f1511; --paper:#162019; --ink:#e7eee8; --muted:#9aab9e; --line:#27342b;
  --brand:#7fc493; --gold:#F2CD41; --gold-ink:#F2CD41; --chip:#1f2c23; color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:var(--f-body);font-size:16px;line-height:1.6}
.wrap{max-width:760px;margin:0 auto;padding-inline:16px;padding-block:20px 60px}
h1,h2{font-family:var(--f-display);text-wrap:balance;margin:0;line-height:1.1}
h1{font-size:2.2rem;color:var(--brand);text-transform:uppercase;letter-spacing:.02em}
.sub{color:var(--muted);margin:.4rem 0 1rem}
nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);display:flex;gap:8px;
  flex-wrap:wrap;padding-block:10px;border-bottom:1px solid var(--line)}
nav a{font-family:var(--f-display);font-size:1.05rem;text-decoration:none;color:var(--brand);
  border:1.5px solid var(--brand);border-radius:999px;padding:2px 12px}
.howto{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:16px 0}
.howto code{background:var(--chip);padding:1px 6px;border-radius:4px;font-size:.92em}
section.video{margin-top:34px;scroll-margin-top:70px}
.ma{font-family:var(--f-display);letter-spacing:.08em;color:var(--muted);font-size:.95rem}
h2{font-size:1.9rem;margin:.2rem 0 .4rem}
.meta{color:var(--muted);font-size:.95rem}
.so{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 4px}
.so span{background:var(--chip);border-radius:6px;padding:2px 8px;font-size:.85rem;font-variant-numeric:tabular-nums}
ol.canh{list-style:none;padding:0;margin:14px 0 0;display:flex;flex-direction:column;gap:10px}
ol.canh li{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:12px 14px;
  display:grid;grid-template-columns:62px 1fr;gap:4px 12px}
.t{font-family:var(--f-display);font-size:1.15rem;color:var(--brand);font-variant-numeric:tabular-nums;line-height:1.2}
.t small{display:block;color:var(--muted);font-size:.8rem}
.body{min-width:0}
.tag{display:inline-block;font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-right:6px}
.who{font-size:.85rem;color:var(--muted)}
p.line{margin:.25rem 0}
p.line b{color:var(--brand)}
.silent{color:var(--muted);font-style:italic}
.chu{display:inline-block;background:#024815;color:#F2CD41;font-family:var(--f-display);font-size:1.05rem;
  padding:1px 10px;border-radius:4px;margin-top:4px;letter-spacing:.02em}
.cat{font-size:.82rem;color:var(--muted);margin-top:4px}
details{margin-top:6px}
summary{cursor:pointer;color:var(--muted);font-size:.85rem}
pre{white-space:pre-wrap;word-break:break-word;background:var(--chip);border-radius:6px;padding:8px 10px;
  font-size:.8rem;line-height:1.45;margin:6px 0}
button.copy{font:inherit;font-size:.8rem;border:1px solid var(--line);background:var(--paper);color:var(--ink);
  border-radius:6px;padding:2px 10px;cursor:pointer}
button.copy:focus-visible,nav a:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.hoi{border-left:4px solid var(--gold);padding-left:10px}
@media (max-width:420px){ol.canh li{grid-template-columns:1fr}.t small{display:inline;margin-left:6px}}
</style>
"""

JS = """
<script>
document.addEventListener('click', function (ev) {
  var b = ev.target.closest('button.copy'); if (!b) return;
  var pre = b.parentElement.querySelector('pre');
  var done = function () { b.textContent = 'Đã chép'; setTimeout(function () { b.textContent = 'Chép prompt'; }, 1500); };
  var fallback = function () { var r = document.createRange(); r.selectNodeContents(pre);
    var s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = 'Đã chọn — bấm giữ để chép'; };
  try { navigator.clipboard.writeText(pre.textContent).then(done, fallback); } catch (e) { fallback(); }
});
</script>
"""


def video_html(data):
    k = kieu(data)
    tong = sum(giay(c, k) for c in data["canh"])
    out = [f'<section class="video" id="{e(data["ma_video"].replace("NSTT-", "v"))}">',
           f'<div class="ma">{e(data["ma_video"])} · bản {e(str(data.get("phien_ban", 1)))} · '
           f'{"nhân vật tự thoại" if k == "thoai" else "người kể"}</div>',
           f'<h2>{e(data["tieu_de_tam"])}</h2>',
           f'<div class="meta">{len(data["canh"])} cảnh · dài khoảng {mmss(tong)}</div>']
    if data.get("bang_tinh"):
        out.append('<div class="so">' + "".join(f"<span>{e(str(v))}</span>" for v in data["bang_tinh"].values()) + "</div>")
    out.append('<ol class="canh">')
    t = 0.0
    for c in data["canh"]:
        g = giay(c, k)
        nv = ", ".join(TEN.get(x, x) for x in c["nhan_vat"]) or "không nhân vật"
        if k == "thoai":
            loi = "".join(f'<p class="line"><b>{e(TEN.get(x["nv"], x["nv"]))}:</b> {e(x["cau"])}</p>' for x in c["thoai"]) \
                or '<p class="line silent">(không có lời — cảnh hình)</p>'
        else:
            loi = f'<p class="line">{e(c["loi"])}</p>'
        cls = ' class="hoi"' if c["phan"] == "CAU_HOI_2_PHE" else ""
        chu = f'<div class="chu">{e(c["chu_man_hinh"])}</div>' if c.get("chu_man_hinh") else ""
        cat = f'<div class="cat">Góc máy: {" → ".join(GOC.get(x, x) for x in c.get("cat", []))}</div>' if c.get("cat") else ""
        out.append(
            f'<li><div class="t">{e(c["so"])}<small>{mmss(t)}–{mmss(t + g)}</small></div>'
            f'<div class="body"><span class="tag">{e(PHAN.get(c["phan"], c["phan"]))}</span>'
            f'<span class="who">{e(BOI.get(c["boi_canh"], c["boi_canh"]))} · {e(nv)}</span>'
            f'<div{cls}>{loi}</div>{chu}{cat}'
            f'<details><summary>Prompt Flow</summary><button class="copy" type="button">Chép prompt</button>'
            f'<pre>{e(c["prompt_flow"])}</pre></details></div></li>')
        t += g
    out.append("</ol></section>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canh_json", nargs="+")
    ap.add_argument("-o", "--out", default="duyet_kich_ban.html")
    a = ap.parse_args()
    ds = [json.loads(Path(p).read_text(encoding="utf-8")) for p in a.canh_json]
    nav = "".join(f'<a href="#{e(d["ma_video"].replace("NSTT-", "v"))}">{e(d["ma_video"][5:])}</a>' for d in ds)
    page = f"""<title>Duyệt kịch bản NSTT</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Be+Vietnam+Pro:wght@400;600&display=swap">
{CSS}
<div class="wrap">
<h1>Nông Sản Tuấn Thủy</h1>
<p class="sub">Kịch bản chờ duyệt lời. Mỗi cảnh là một clip Veo khoảng 8 giây; thời gian ghi bên trái là ước tính.</p>
<nav>{nav}</nav>
<div class="howto">Duyệt: nhắn <code>DUYỆT LỜI NSTT-20261001-A</code>. Muốn sửa: nhắn <code>SỬA NSTT-20261001-A S05: …</code> (ghi số cảnh và lời mới).</div>
{"".join(video_html(d) for d in ds)}
</div>
{JS}"""
    Path(a.out).write_text(page, encoding="utf-8")
    print("đã ghi", a.out)


if __name__ == "__main__":
    main()
