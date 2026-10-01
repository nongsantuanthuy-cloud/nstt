#!/usr/bin/env python3
"""Vẽ vùng bị giao diện che (TikTok / Facebook Reels / YouTube Shorts) lên 1 khung hình video dọc 1080×1920
để soát phụ đề, chữ lớn, logo có nằm trong vùng an toàn không.

    python tools/vung_an_toan.py kich_ban/<ma>/ban_dung/<ma>.mp4 --giay 20 -o soat_vung_an_toan.jpg

Số đo vùng che là ước lượng thận trọng theo hướng dẫn công bố của các nền tảng (dễ thay đổi theo phiên bản app):
  - Trên: thanh tab / nút LIVE / tìm kiếm ≈ 14% chiều cao (270 px).
  - Dưới: tên kênh, chú thích, nhạc ≈ 35% (Reels, khắt khe nhất) — TikTok/Shorts ≈ 20–25%.
  - Phải: cột nút thích / bình luận / chia sẻ ≈ 140 px (từ ~40% đến ~85% chiều cao).
"""
import argparse, subprocess
from pathlib import Path
from PIL import Image, ImageDraw

W, H = 1080, 1920
VUNG = [  # (tên, hộp, màu)
    ("TREN (14%)", (0, 0, W, 270), (255, 0, 0, 70)),
    ("DUOI REELS (35%)", (0, H - 672, W, H), (255, 140, 0, 55)),
    ("DUOI TIKTOK/SHORTS (~22%)", (0, H - 420, W, H), (255, 0, 0, 70)),
    ("COT NUT PHAI", (W - 140, 760, W, 1640), (255, 0, 0, 70)),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--giay", type=float, default=20)
    ap.add_argument("-o", default="soat_vung_an_toan.jpg")
    a = ap.parse_args()
    try:
        import imageio_ffmpeg
        ff = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        ff = "ffmpeg"
    tam = Path(a.o).with_suffix(".tmp.png")
    subprocess.run([ff, "-y", "-loglevel", "error", "-ss", str(a.giay), "-i", a.video, "-frames:v", "1", str(tam)], check=True)
    nen = Image.open(tam).convert("RGBA")
    lop = Image.new("RGBA", nen.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lop)
    for ten, hop, mau in VUNG:
        d.rectangle(hop, fill=mau, outline=mau[:3] + (255,), width=3)
        d.text((hop[0] + 10, hop[1] + 8), ten, fill=(255, 255, 255, 255))
    Image.alpha_composite(nen, lop).convert("RGB").save(a.o, quality=88)
    tam.unlink()
    print("đã ghi", a.o)


if __name__ == "__main__":
    main()
