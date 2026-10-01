#!/usr/bin/env python3
"""Ảnh lưới 3 khung (giây 1, 4, 7) cho mỗi clip để soát nhanh mặt, áo, chữ lạ, người lạ.

    py .claude/skills/chuyen-sau-rieng/scripts/luoi_khung.py NSTT-20261001-B <thư mục ra> [S06,S07]
Đầu ra: <thư mục ra>/luoi_Sxx.jpg — xem bằng công cụ Read.
"""
import subprocess, sys
from pathlib import Path
import imageio_ffmpeg
from PIL import Image, ImageDraw

ff = imageio_ffmpeg.get_ffmpeg_exe()
goc = Path("kich_ban") / sys.argv[1] / "clip_veo"
ra = Path(sys.argv[2]); ra.mkdir(parents=True, exist_ok=True)
chon = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
for clip in sorted(goc.glob("S*.mp4")):
    if chon and clip.stem not in chon:
        continue
    khung = []
    for t in (1, 4, 7):
        p = ra / f"{clip.stem}_{t}.jpg"
        subprocess.run([ff, "-y", "-loglevel", "error", "-ss", str(t), "-i", str(clip), "-frames:v", "1",
                        "-vf", "scale=426:-1", str(p)], check=True)
        khung.append(Image.open(p))
    w, h = khung[0].size
    luoi = Image.new("RGB", (w * 3, h + 24), "black")
    for i, k in enumerate(khung):
        luoi.paste(k, (i * w, 24))
    ImageDraw.Draw(luoi).text((6, 4), clip.stem, fill="yellow")
    luoi.save(ra / f"luoi_{clip.stem}.jpg", quality=85)
    for k in khung:
        k.close()
    print(clip.stem, "ok")
