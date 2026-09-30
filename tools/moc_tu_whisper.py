#!/usr/bin/env python3
"""Nghe lại lời thoại clip Veo bằng Whisper: (1) kiểm tra Veo nói ĐÚNG lời + đúng tiếng Việt,
(2) lấy mốc thời gian từng chữ cho phụ đề karaoke. Chạy trên máy chủ kênh (cần tải mô hình Whisper).

    python tools/moc_tu_whisper.py kich_ban/<ma>/canh.json [--model large-v3] [--nguong 0.75]

Cài: pip install faster-whisper   (máy yếu dùng --model medium; có GPU thêm --device cuda)
Đầu ra:
  kich_ban/<ma>/tu_thoai/Sxx.json      [{"w": chữ theo KỊCH BẢN (đúng chính tả), "start", "end"}]
  kich_ban/<ma>/clip_veo/kiem_tra_thoai.json   điểm khớp từng cảnh; cảnh < ngưỡng → TẠO LẠI clip
Phụ đề luôn dùng chữ của kịch bản; Whisper chỉ cung cấp thời gian (tránh lỗi kiểu "giường"/"vườn").
"""
import argparse, difflib, json, re, sys, unicodedata
from pathlib import Path


def chuan(w: str) -> str:
    return unicodedata.normalize("NFC", re.sub(r"[^\w]", "", w.lower()))


def tach(cau: str):
    return re.findall(r"[^\W\d_]+[^\s]*", cau)


def gan_moc(tu_kb, tu_wh):
    """Ghép chữ kịch bản với chữ Whisper (có thời gian); chữ không khớp thì nội suy."""
    a = [chuan(w) for w in tu_kb]
    b = [chuan(w["w"]) for w in tu_wh]
    moc = [None] * len(tu_kb)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            w = tu_wh[blk.b + k]
            moc[blk.a + k] = (w["start"], w["end"])
    # nội suy chỗ trống
    t0 = tu_wh[0]["start"] if tu_wh else 0.0
    t1 = tu_wh[-1]["end"] if tu_wh else 1.0
    i = 0
    while i < len(moc):
        if moc[i] is None:
            j = i
            while j < len(moc) and moc[j] is None:
                j += 1
            s = moc[i - 1][1] if i else t0
            e = moc[j][0] if j < len(moc) else t1
            buoc = max(e - s, 0.1) / (j - i)
            for k in range(i, j):
                moc[k] = (s + (k - i) * buoc, s + (k - i + 1) * buoc * 0.9)
            i = j
        else:
            i += 1
    return [{"w": w, "start": round(m[0], 3), "end": round(m[1], 3)} for w, m in zip(tu_kb, moc)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canh_json")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--device", default="auto")
    ap.add_argument("--nguong", type=float, default=0.75)
    a = ap.parse_args()
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("Cần: pip install faster-whisper")

    pj = Path(a.canh_json)
    data = json.loads(pj.read_text(encoding="utf-8"))
    goc = pj.parent
    (goc / "tu_thoai").mkdir(exist_ok=True)
    model = WhisperModel(a.model, device=a.device, compute_type="int8")
    ket_qua, can_lam_lai = {}, []
    for c in data["canh"]:
        thoai = c.get("thoai", [])
        clip = goc / "clip_veo" / f"{c['so']}.mp4"
        if not thoai or not clip.exists():
            continue
        cau_kb = " ".join(t["cau"] for t in thoai)
        segs, info = model.transcribe(str(clip), language="vi", word_timestamps=True, vad_filter=True,
                                      initial_prompt=cau_kb)
        tu_wh = [{"w": w.word.strip(), "start": w.start, "end": w.end} for s in segs for w in (s.words or [])]
        nghe = " ".join(w["w"] for w in tu_wh)
        # kiểm tra ngôn ngữ riêng (không ép vi) để bắt tiếng nước ngoài
        _, info2 = model.transcribe(str(clip), without_timestamps=True)
        diem = difflib.SequenceMatcher(None, [chuan(w) for w in tach(cau_kb)],
                                       [chuan(w["w"]) for w in tu_wh], autojunk=False).ratio()
        dat = diem >= a.nguong and info2.language == "vi"
        ket_qua[c["so"]] = {"kich_ban": cau_kb, "nghe_duoc": nghe, "diem_khop": round(diem, 3),
                            "ngon_ngu": info2.language, "dat": dat}
        if not dat:
            can_lam_lai.append(c["so"])
        (goc / "tu_thoai" / f"{c['so']}.json").write_text(
            json.dumps(gan_moc(tach(cau_kb), tu_wh), ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{c['so']}: khớp {diem:.0%} [{info2.language}] {'OK' if dat else 'TẠO LẠI'}  — {nghe}")
    (goc / "clip_veo" / "kiem_tra_thoai.json").write_text(
        json.dumps({"can_tao_lai": can_lam_lai, "chi_tiet": ket_qua}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Cần tạo lại:", ", ".join(can_lam_lai) or "không")
    sys.exit(1 if can_lam_lai else 0)


if __name__ == "__main__":
    main()
