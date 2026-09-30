#!/usr/bin/env python3
"""Trích khung hình video mẫu để phân tích theo từng cảnh.

    python3 tools/trich_khung_hinh.py "video mẫu.mp4" [thu_muc_ra] [--nguong 0.3] [--moi 1]

Đầu ra (mặc định `phan_tich/<tên video>/`):
  - canh_XX_<giây>.jpg   : 1 ảnh đầu mỗi lần chuyển cảnh (scene detect, ngưỡng --nguong)
  - moi_giay/tXXX.jpg    : 1 ảnh mỗi --moi giây
  - luoi.jpg             : lưới ảnh 1 khung/giây để xem nhanh cả video
  - bang_canh.csv        : cảnh, bắt đầu, kết thúc, độ dài — điền thêm cột mô tả bằng tay/AI
  - am_thanh.wav         : âm thanh mono 16 kHz (để chạy Whisper lấy lời thoại)
Cần ffmpeg (hoặc `pip install imageio-ffmpeg`).
"""
import csv, re, shutil, subprocess, sys
from pathlib import Path


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("Không tìm thấy ffmpeg. Cài: pip install imageio-ffmpeg")


def chay(args):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def do_dai(ff, video):
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", chay([ff, "-i", str(video)]).stderr)
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else 0.0


def main():
    args = [a for a in sys.argv[1:]]
    if not args:
        print(__doc__); sys.exit(2)
    nguong = float(args[args.index("--nguong") + 1]) if "--nguong" in args else 0.3
    moi = float(args[args.index("--moi") + 1]) if "--moi" in args else 1.0
    vitri = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or not args[i - 1].startswith("--"))]
    video = Path(vitri[0])
    ra = Path(vitri[1]) if len(vitri) > 1 else Path("phan_tich") / video.stem
    (ra / "moi_giay").mkdir(parents=True, exist_ok=True)
    ff = ffmpeg_exe()
    tong = do_dai(ff, video)

    # 1. Phát hiện chuyển cảnh
    r = chay([ff, "-hide_banner", "-i", str(video), "-vf", f"select='gt(scene,{nguong})',showinfo",
              "-vsync", "vfr", "-f", "null", "-"])
    moc = [0.0] + [float(x) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)]
    moc = sorted(set(round(x, 2) for x in moc))
    with open(ra / "bang_canh.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["canh", "bat_dau_s", "ket_thuc_s", "do_dai_s", "anh", "mo_ta_hinh", "loi_thoai", "am_thanh"])
        for i, t in enumerate(moc, 1):
            het = moc[i] if i < len(moc) else tong
            anh = f"canh_{i:02d}_{t:06.2f}.jpg"
            chay([ff, "-y", "-ss", f"{t + 0.05:.2f}", "-i", str(video), "-frames:v", "1", "-q:v", "3", str(ra / anh)])
            w.writerow([i, f"{t:.2f}", f"{het:.2f}", f"{het - t:.2f}", anh, "", "", ""])

    # 2. Mỗi giây 1 ảnh + lưới
    chay([ff, "-y", "-i", str(video), "-vf", f"fps=1/{moi},scale=270:-1", "-q:v", "4",
          str(ra / "moi_giay" / "t%03d.jpg")])
    so = max(1, int(tong / moi))
    cot = 10
    chay([ff, "-y", "-i", str(video), "-vf",
          f"fps=1/{moi},scale=216:-1,tile={cot}x{(so + cot - 1) // cot}", "-frames:v", "1", "-q:v", "4",
          str(ra / "luoi.jpg")])

    # 3. Âm thanh
    chay([ff, "-y", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(ra / "am_thanh.wav")])
    print(f"Video {tong:.1f}s — {len(moc)} cảnh → {ra}")


if __name__ == "__main__":
    main()
