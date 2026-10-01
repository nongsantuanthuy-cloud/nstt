#!/usr/bin/env python3
"""Đặt "dung" [a, b] cho từng cảnh theo mốc chữ Whisper (kich_ban/<mã>/tu_thoai/Sxx.json):
0,25 s trước chữ đầu → 0,5 s sau chữ cuối. Cảnh đã có "dung" đặt tay thì giữ nguyên nếu thêm --giu.

    py .claude/skills/chuyen-sau-rieng/scripts/dat_dung.py NSTT-20261001-B [--giu S01,S20]

Lý do: clip Veo 8 s gần như không có khoảng lặng, công cụ dựng dò im lặng sẽ lấy cả 8 s → video dài thêm ~35 s.
"""
import json, sys
from pathlib import Path

DAI_CLIP = 8.0   # Veo 3.1 Lite trên Flow cho clip 8 s (S01 cũ 10 s thì đặt tay + --giu)
ma = sys.argv[1]
giu = set(sys.argv[sys.argv.index("--giu") + 1].split(",")) if "--giu" in sys.argv else set()
goc = Path("kich_ban") / ma
p = goc / "canh.json"
d = json.loads(p.read_text(encoding="utf-8"))
tong = 0.0
for c in d["canh"]:
    f = goc / "tu_thoai" / f"{c['so']}.json"
    if c["so"] in giu or not f.exists():
        a, b = c.get("dung", [0, 8])
    else:
        w = json.loads(f.read_text(encoding="utf-8"))
        a = max(0.0, round(w[0]["start"] - 0.25, 2))
        b = min(DAI_CLIP, round(w[-1]["end"] + 0.5, 2))   # không vượt quá độ dài clip Veo
        c["dung"] = [a, b]
    tong += b - a
    print(c["so"], c.get("dung"), round(b - a, 2))
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("tổng ước tính", round(tong, 1), "giây (mục tiêu 110–135)")
