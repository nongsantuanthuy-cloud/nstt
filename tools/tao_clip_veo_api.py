#!/usr/bin/env python3
"""Tự tạo clip Veo 3.1 qua Gemini API (không cần mở Google Flow) cho mọi cảnh trong canh.json.

    python3 tools/tao_clip_veo_api.py kich_ban/<ma>/canh.json [--canh S01,S03] [--model veo-3.1-fast-generate-preview]
                                     [--do-phan-giai 720p] [--liet-ke] [--thu-nghiem]

Cần biến môi trường GEMINI_API_KEY (tạo ở aistudio.google.com, bật thanh toán). KHÔNG dán key vào chat/repo.
Ảnh nhân vật: thuong_hieu/nhan_vat/<ten>.png với <ten> = tên Flow viết thường, nối "_" (vd chu_nam.png, ut_nho.png).
Mỗi cảnh gửi tối đa 3 ảnh tham chiếu (loại "asset") theo `nhan_vat` của cảnh.
Clip đã có (clip_veo/Sxx.mp4) sẽ bỏ qua — muốn tạo lại thì xóa/đổi tên file cũ.
--liet-ke: in các model Veo mà key dùng được.  --thu-nghiem: chỉ in yêu cầu, không gọi API (không tốn tiền).
Giá tham khảo (Gemini API, 2026): Veo 3.1 0,40 USD/giây · Fast 0,10 · Lite 0,05 (720p) — 1 clip 8 giây Fast ≈ 0,8 USD.
"""
import argparse, base64, json, os, sys, time
from pathlib import Path
import urllib.request, urllib.error

API = "https://generativelanguage.googleapis.com/v1beta"
GIA = {"veo-3.1-generate-preview": 0.40, "veo-3.1-fast-generate-preview": 0.10, "veo-3.1-lite-generate-preview": 0.05}
GOC = Path(__file__).resolve().parent.parent


def goi(url, key, body=None, raw=False):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"x-goog-api-key": key, "Content-Type": "application/json"},
                                 method="POST" if body is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = r.read()
            return data if raw else json.loads(data)
    except urllib.error.HTTPError as e:
        loi = e.read().decode("utf-8", "replace")[:800]
        raise RuntimeError(f"HTTP {e.code}: {loi}") from None


def anh_nhan_vat(ten):
    for duoi in (".png", ".jpg", ".jpeg", ".webp"):
        p = GOC / "thuong_hieu" / "nhan_vat" / (ten.lower().replace(" ", "_") + duoi)
        if p.exists():
            return p
    return None


def mime(p):
    return {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}[p.suffix]


def yeu_cau(c, do_phan_giai, kieu_anh):
    anh = []
    for nv in c.get("nhan_vat", [])[:3]:
        p = anh_nhan_vat(nv)
        if p is None:
            raise FileNotFoundError(f"{c['so']}: thiếu ảnh nhân vật {nv} (thuong_hieu/nhan_vat/"
                                    f"{nv.lower().replace(' ', '_')}.png)")
        b64 = base64.b64encode(p.read_bytes()).decode()
        img = ({"inlineData": {"mimeType": mime(p), "data": b64}} if kieu_anh == "inline"
               else {"bytesBase64Encoded": b64, "mimeType": mime(p)})
        anh.append({"image": img, "referenceType": "asset"})
    inst = {"prompt": c["prompt_flow"]}
    if anh:
        inst["referenceImages"] = anh
    return {"instances": [inst],
            "parameters": {"aspectRatio": "16:9", "resolution": do_phan_giai, "durationSeconds": 8,
                           "personGeneration": "allow_adult"}}


def tao_mot(c, key, model, do_phan_giai, ra):
    for kieu_anh in ("inline", "bytes"):   # API có 2 cách gửi ảnh; thử lần lượt
        try:
            op = goi(f"{API}/models/{model}:predictLongRunning", key, yeu_cau(c, do_phan_giai, kieu_anh))
            break
        except RuntimeError as e:
            if kieu_anh == "bytes" or "HTTP 400" not in str(e):
                raise
    ten_op = op["name"]
    bd = time.time()
    while not op.get("done"):
        if time.time() - bd > 900:
            raise TimeoutError(f"{c['so']}: quá 15 phút chưa xong ({ten_op})")
        time.sleep(15)
        op = goi(f"{API}/{ten_op}", key)
    if "error" in op:
        raise RuntimeError(f"{c['so']}: Veo báo lỗi: {json.dumps(op['error'], ensure_ascii=False)[:500]}")
    res = op.get("response", {})
    mau = (res.get("generateVideoResponse", {}).get("generatedSamples")
           or res.get("generatedVideos") or [])
    if not mau:
        raise RuntimeError(f"{c['so']}: không có video (có thể bị bộ lọc an toàn chặn): "
                           f"{json.dumps(res, ensure_ascii=False)[:500]}")
    uri = mau[0]["video"]["uri"]
    ra.write_bytes(goi(uri, key, raw=True))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canh_json", nargs="?")
    ap.add_argument("--canh", help="chỉ làm các cảnh này, vd S01,S03")
    ap.add_argument("--model", default="veo-3.1-fast-generate-preview")
    ap.add_argument("--do-phan-giai", default="720p", choices=["720p", "1080p"])
    ap.add_argument("--liet-ke", action="store_true")
    ap.add_argument("--thu-nghiem", action="store_true")
    a = ap.parse_args()
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key and not a.thu_nghiem:
        sys.exit("Chưa có GEMINI_API_KEY trong môi trường. Thêm vào cài đặt môi trường (biến môi trường), mở phiên mới.")
    if a.liet_ke:
        for m in goi(f"{API}/models?pageSize=200", key).get("models", []):
            if "veo" in m["name"]:
                print(m["name"], "-", m.get("displayName", ""))
        return
    pj = Path(a.canh_json)
    data = json.loads(pj.read_text(encoding="utf-8"))
    ds = [c for c in data["canh"] if not a.canh or c["so"] in a.canh.split(",")]
    thu_muc = pj.parent / "clip_veo"
    thu_muc.mkdir(exist_ok=True)
    viec = [c for c in ds if not (thu_muc / f"{c['so']}.mp4").exists()]
    gia = GIA.get(a.model, 0.40) * 8 * len(viec)
    print(f"{len(viec)} clip cần tạo · model {a.model} · ước tính ~{gia:.2f} USD")
    loi = []
    for c in viec:
        ra = thu_muc / f"{c['so']}.mp4"
        if a.thu_nghiem:
            try:
                yeu_cau(c, a.do_phan_giai, "inline")
                print(c["so"], "OK ảnh:", c["nhan_vat"][:3], "| prompt", len(c["prompt_flow"]), "ký tự")
            except FileNotFoundError as e:
                print("THIẾU", e)
            continue
        try:
            print(f"{c['so']}: đang tạo…", flush=True)
            tao_mot(c, key, a.model, a.do_phan_giai, ra)
            print(f"{c['so']}: xong → {ra}")
        except Exception as e:   # ghi lỗi, làm tiếp cảnh sau
            print(f"{c['so']}: LỖI {e}")
            loi.append(c["so"])
    if loi:
        print("Cảnh lỗi (chạy lại với --canh):", ",".join(loi))
        sys.exit(1)


if __name__ == "__main__":
    main()
