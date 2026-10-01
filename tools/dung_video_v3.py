#!/usr/bin/env python3
"""Dựng video NSTT kiểu v3 (nhân vật tự thoại) bằng FFmpeg — không cần Remotion, không cần TTS.

    python3 tools/dung_video_v3.py kich_ban/<ma>/canh.json [--logo thuong_hieu/logo/logo_nstt_400.png]
                                   [--font "Arial"] [--nhap]

Đầu vào (trong kich_ban/<ma>/):
  clip_veo/Sxx.mp4        clip Google Flow 16:9 (720p/1080p) CÓ TIẾNG THOẠI của Veo
  tu_thoai/Sxx.json       (tùy chọn) mốc từng chữ [{"w": "bao", "start": 0.41, "end": 0.62}, ...] tính theo giây
                          trong clip — sinh bằng faster-whisper trên máy (tools/moc_tu_whisper.py). Không có thì
                          công cụ tự ước tính: dò khoảng có tiếng trong clip rồi chia đều theo âm tiết.
Mỗi cảnh trong canh.json có thể thêm:
  "dung": [a, b]          chỉ lấy đoạn a→b giây của clip (mặc định: tự dò đoạn có tiếng nói ± đệm)
  "tam_x": 0.5            tâm ngang khi cắt dọc (0 = mép trái, 1 = mép phải) — chỉnh khi mặt nhân vật lệch
  "cat": ["toan","can@0.33","dac_ta"]  chia đoạn dùng thành các góc (thêm @x để đặt tâm ngang riêng từng góc): toàn (khung 16:9 + nền mờ),
                          cận (cắt dọc 9:16), đặc tả (cắt dọc phóng 1,6 lần)
Đầu ra: ban_dung/<ma>.mp4 — 1080×1920, 30 fps, H.264 yuv420p, AAC, −14 LUFS; phụ đề karaoke 2–3 chữ IN HOA,
chữ đang nói tô vàng #F2CD41; logo góc trên (nếu có). Chữ lớn `chu_man_hinh` nền xanh #024815 chỉ hiện khi
thêm --hien-chu-lon (chủ kênh 01/10/2026: mọi video bỏ chữ lớn).
Bản cũ chuyển vào _tam/<ma>_vN.mp4.  --nhap: nhanh, chất lượng thấp để xem thử.
"""
import argparse, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path

W, H, FPS = 1080, 1920, 30
VANG, XANH = "F2CD41", "024815"   # màu thương hiệu (RGB)
ZOOM_DAC_TA = 1.6
DEM_TRUOC, DEM_SAU = 0.25, 0.6    # giây đệm quanh tiếng nói
IM_LANG_MAC_DINH = 2.5
# Vùng an toàn chung TikTok / Reels / Shorts (soát bằng tools/vung_an_toan.py): tránh 14% trên (270 px),
# 35% dưới của Reels (từ y≈1250) và cột nút bên phải.
LOGO_X, LOGO_Y, LOGO_RONG = 36, 290, 150
PHU_DE_MARGIN_V = 675        # chân phụ đề ở y = 1245 — thấp nhất còn an toàn cho Reels (35% dưới); TikTok/Shorts cho phép thấp hơn
CHU_MARGIN_V, CHU_MARGIN_L = 300, 210   # chữ lớn bắt đầu y=300, chừa chỗ logo bên trái


def ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        sys.exit("Không tìm thấy ffmpeg. Cài: pip install imageio-ffmpeg")


FF = ffmpeg()


def chay(args, check=True):
    r = subprocess.run([FF, "-hide_banner", "-y", *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if check and r.returncode:
        sys.exit("FFmpeg lỗi:\n" + r.stderr[-2000:])
    return r.stderr


def do_dai(p: Path) -> float:
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", chay(["-i", str(p)], check=False))
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else 0.0


def doan_co_tieng(p: Path, dai: float):
    """Các đoạn có tiếng [(đầu, cuối)], dò bằng silencedetect; bỏ tiếng động ngắn ở đầu (bước chân, lá…)."""
    err = chay(["-i", str(p), "-af", "silencedetect=n=-32dB:d=0.25", "-f", "null", "-"], check=False)
    lang, bd = [], None
    for dong in err.splitlines():
        if "silence_start" in dong:
            bd = float(dong.split("silence_start:")[1])
        elif "silence_end" in dong and bd is not None:
            lang.append((bd, float(dong.split("silence_end:")[1].split("|")[0])))
            bd = None
    if bd is not None:
        lang.append((bd, dai))
    doan, t = [], 0.0
    for a, b in lang:
        if a - t > 0.05:
            doan.append((t, a))
        t = b
    if dai - t > 0.05:
        doan.append((t, dai))
    while doan and doan[0][1] - doan[0][0] < 0.35:   # tiếng lẻ ngắn trước câu nói
        doan.pop(0)
    return doan


def khoang_co_tieng(p: Path, dai: float):
    d = doan_co_tieng(p, dai)
    return (d[0][0], d[-1][1]) if d else None


def am_tiet(cau: str):
    return re.findall(r"[^\W\d_]+[^\s]*", cau)


def uoc_tinh_moc(thoai, dau, cuoi):
    """Chia đều thời gian nói cho từng âm tiết (có trọng số theo độ dài chữ + nghỉ ở dấu câu)."""
    tu = []
    for t in thoai:
        tu += am_tiet(t["cau"])
    if not tu:
        return []
    trong_so = [len(re.sub(r"\W", "", w)) + 2 + (3 if re.search(r"[.,!?:;]$", w) else 0) for w in tu]
    tong = sum(trong_so)
    moc, t = [], dau
    for w, s in zip(tu, trong_so):
        d = (cuoi - dau) * s / tong
        moc.append({"w": w, "start": t, "end": t + d * 0.85})
        t += d
    return moc


def ass_mau(rgb: str, alpha="00"):
    return f"&H{alpha}{rgb[4:6]}{rgb[2:4]}{rgb[0:2]}"


def ass_gio(t: float):
    t = max(0.0, t)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def ass_dau(font):
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: PhuDe,{font},84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,1,0,0,0,90,100,0,0,1,6,3,2,150,150,{PHU_DE_MARGIN_V},1
Style: Chu,{font},64,{ass_mau(VANG)},{ass_mau(VANG)},{ass_mau(XANH)},{ass_mau(XANH)},1,0,0,0,95,100,0,0,3,16,0,8,{CHU_MARGIN_L},60,{CHU_MARGIN_V},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def cum_tu(moc, toi_da=3):
    """Gom 2–3 âm tiết/cụm, ngắt sau dấu câu."""
    cum, hien = [], []
    for m in moc:
        hien.append(m)
        if len(hien) >= toi_da or re.search(r"[.,!?:;]$", m["w"]):
            cum.append(hien)
            hien = []
    if hien:
        cum.append(hien)
    return cum


def su_kien_phu_de(moc):
    """Mỗi chữ 1 sự kiện: cả cụm hiện, chữ đang nói tô vàng (giống karaoke của video mẫu)."""
    out = []
    for cum in cum_tu(moc):
        for i, m in enumerate(cum):
            bd = m["start"]
            kt = cum[i + 1]["start"] if i + 1 < len(cum) else max(m["end"], bd + 0.25)
            chu = " ".join(("{\\c" + ass_mau(VANG) + "}" + x["w"].upper() + "{\\c&H00FFFFFF}") if j == i
                           else x["w"].upper() for j, x in enumerate(cum))
            out.append(f"Dialogue: 0,{ass_gio(bd)},{ass_gio(kt)},PhuDe,,0,0,0,,{chu}")
    return out


def loc_khung(kieu: str, tam_x: float, iw: int, ih: int):
    """Chuỗi filter biến clip 16:9 thành 1080×1920 theo kiểu khung."""
    if kieu == "toan":
        return (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=30,"
                f"eq=brightness=-0.08[nen];[b]scale={W}:-2[tr];[nen][tr]overlay=0:(H-h)/2")
    z = ZOOM_DAC_TA if kieu == "dac_ta" else 1.0
    ch = int(ih / z) // 2 * 2
    cw = int(ch * 9 / 16) // 2 * 2
    x = int(min(max(tam_x * iw - cw / 2, 0), iw - cw))
    y = int((ih - ch) * (0.4 if kieu == "dac_ta" else 0.5))
    return f"crop={cw}:{ch}:{x}:{y},scale={W}:{H}"


def kich_thuoc(p: Path):
    m = re.search(r"Video:.*?(\d{3,5})x(\d{3,5})", chay(["-i", str(p)], check=False))
    return (int(m[1]), int(m[2])) if m else (1280, 720)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canh_json")
    ap.add_argument("--logo")
    ap.add_argument("--font", default="Arial")
    ap.add_argument("--nhap", action="store_true")
    # Chủ kênh 01/10/2026: mọi video bỏ chữ lớn nền xanh (chu_man_hinh) — mặc định tắt, muốn hiện thì --hien-chu-lon
    ap.add_argument("--hien-chu-lon", action="store_true", help="hiện chữ lớn chu_man_hinh (mặc định tắt)")
    ap.add_argument("--bo-chu-lon", action="store_true", help="(giữ tương thích, nay là mặc định)")
    a = ap.parse_args()

    pj = Path(a.canh_json)
    data = json.loads(pj.read_text(encoding="utf-8"))
    goc = pj.parent
    ma = data["ma_video"]
    thieu = [c["so"] for c in data["canh"] if not (goc / "clip_veo" / f"{c['so']}.mp4").exists()]
    if thieu:
        sys.exit(f"Thiếu clip: {', '.join(thieu)} (cần kich_ban/{ma}/clip_veo/Sxx.mp4)")
    chat = ["-c:v", "libx264", "-preset", "ultrafast" if a.nhap else "medium", "-crf", "30" if a.nhap else "19",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]

    tam = Path(tempfile.mkdtemp(prefix="nstt_"))
    doan, su_kien, t_ra = [], [], 0.0
    bao_cao = []
    for c in data["canh"]:
        clip = goc / "clip_veo" / f"{c['so']}.mp4"
        dai = do_dai(clip)
        iw, ih = kich_thuoc(clip)
        thoai = c.get("thoai", [])
        tieng = khoang_co_tieng(clip, dai) if thoai else None
        if c.get("dung"):
            u0, u1 = c["dung"]
        elif thoai and tieng:
            u0, u1 = max(0.0, tieng[0] - DEM_TRUOC), min(dai, tieng[1] + DEM_SAU)
        else:
            u0 = min(0.5, dai / 4)
            u1 = min(dai, u0 + IM_LANG_MAC_DINH)
        # mốc chữ
        f_moc = goc / "tu_thoai" / f"{c['so']}.json"
        if f_moc.exists():
            moc = json.loads(f_moc.read_text(encoding="utf-8"))
            nguon = "whisper"
        elif thoai:
            doan_t = [d for d in doan_co_tieng(clip, dai) if d[1] > u0 and d[0] < u1]
            if len(thoai) == 2 and len(doan_t) >= 2:
                k = max(range(1, len(doan_t)), key=lambda i: doan_t[i][0] - doan_t[i - 1][1])
                moc = (uoc_tinh_moc(thoai[:1], doan_t[0][0], doan_t[k - 1][1])
                       + uoc_tinh_moc(thoai[1:], doan_t[k][0], doan_t[-1][1]))
            else:
                s0, s1 = (doan_t[0][0], doan_t[-1][1]) if doan_t else (u0 + 0.2, u1 - 0.3)
                moc = uoc_tinh_moc(thoai, s0, s1)
            nguon = "uoc_tinh" if tieng else "uoc_tinh_khong_do_duoc_tieng"
        else:
            moc, nguon = [], "-"
        dich = t_ra - u0
        su_kien += su_kien_phu_de([{**m, "start": m["start"] + dich, "end": m["end"] + dich}
                                   for m in moc if u0 - 0.1 <= m["start"] <= u1])
        if c.get("chu_man_hinh") and a.hien_chu_lon:
            chu = c["chu_man_hinh"].replace(" | ", r"\N")   # " | " = xuống dòng có chủ đích
            su_kien.append(f"Dialogue: 1,{ass_gio(t_ra + 0.2)},{ass_gio(t_ra + (u1 - u0))},Chu,,0,0,0,,{chu}")
        # cắt góc
        cat = c.get("cat") or ["toan"]
        buoc = (u1 - u0) / len(cat)
        that = 0.0   # độ dài thật sau khi cắt (khung hình làm tròn) — dùng để phụ đề cảnh sau không bị trôi
        for i, kieu in enumerate(cat):
            out = tam / f"{c['so']}_{i}.mp4"
            kieu, _, tx = kieu.partition("@")   # "can@0.33" = cận, tâm ngang 33% khung
            tx = float(tx) if tx else c.get("tam_x", 0.5)
            chay(["-ss", f"{u0 + i * buoc:.3f}", "-t", f"{buoc:.3f}", "-i", str(clip),
                  "-filter_complex", f"[0:v]{loc_khung(kieu, tx, iw, ih)},setsar=1,fps={FPS}[v]",
                  "-map", "[v]", "-map", "0:a?", *chat, "-shortest", str(out)])
            doan.append(out)
            that += do_dai(out)
        bao_cao.append(f"{c['so']}: dùng {u0:.2f}–{u1:.2f}s / {dai:.2f}s, góc {'→'.join(cat)}, mốc chữ: {nguon}")
        t_ra += that

    # nối
    ds = tam / "ds.txt"
    ds.write_text("".join(f"file '{p.as_posix()}'\n" for p in doan), encoding="utf-8")
    noi = tam / "noi.mp4"
    chay(["-f", "concat", "-safe", "0", "-i", str(ds), *chat, str(noi)])
    # phụ đề + logo + âm lượng
    ass = tam / "phu_de.ass"
    ass.write_text(ass_dau(a.font) + "\n".join(su_kien) + "\n", encoding="utf-8")
    ass_duong = ass.as_posix().replace(":", "\\:")
    vf = f"ass='{ass_duong}'"
    vao = ["-i", str(noi)]
    if a.logo and Path(a.logo).exists():
        vao += ["-i", a.logo]
        loc = f"[1:v]scale={LOGO_RONG}:-1,format=rgba[lg];[0:v]{vf}[s];[s][lg]overlay={LOGO_X}:{LOGO_Y}[v]"
    else:
        loc = f"[0:v]{vf}[v]"
    ra_dir = goc / "ban_dung"
    ra_dir.mkdir(exist_ok=True)
    ra = ra_dir / f"{ma}.mp4"
    if ra.exists():
        (goc / "_tam").mkdir(exist_ok=True)
        n = len(list((goc / "_tam").glob(f"{ma}_v*.mp4"))) + 1
        shutil.move(str(ra), str(goc / "_tam" / f"{ma}_v{n}.mp4"))
    chay([*vao, "-filter_complex", loc, "-map", "[v]", "-map", "0:a?",
          "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", *chat, "-movflags", "+faststart", str(ra)])
    (goc / "ban_dung" / "bao_cao_dung.txt").write_text("\n".join(bao_cao) + f"\nTổng: {t_ra:.1f}s\n", encoding="utf-8")
    shutil.rmtree(tam, ignore_errors=True)
    print("\n".join(bao_cao))
    print(f"Xong: {ra} ({t_ra:.1f}s)")


if __name__ == "__main__":
    main()
