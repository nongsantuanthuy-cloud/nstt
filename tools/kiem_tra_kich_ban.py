#!/usr/bin/env python3
"""Kiểm tra canh.json của kênh NSTT và (tùy chọn) xuất kich_ban.md.

    python3 tools/kiem_tra_kich_ban.py kich_ban/<ma>/canh.json [--md]

Hỗ trợ 2 kiểu:
  - v3 "thoai" (từ 30/09/2026, mặc định): nhân vật tự thoại, mỗi cảnh có `thoai` [{nv, cau}], `cat`.
  - v2 "nguoi_ke" (cũ): 1 giọng kể UV07, mỗi cảnh có `loi`.
Kiểm tra: trường bắt buộc, phần/bối cảnh hợp lệ, nhân vật hợp lệ + mô tả có trong prompt,
chữ số trong lời, câu mở/kết cố định, số âm tiết, lời thoại nằm nguyên văn trong prompt, tổng thời lượng.
"""
import json, re, sys
from pathlib import Path

TOC_DO = 4.0      # âm tiết / giây
NGHI = 0.8        # v2: giây nghỉ giữa cảnh
NHIP = 1.2        # v3: giây phản ứng/hành động thêm mỗi clip có thoại
IM_LANG = 2.5     # v3: clip không thoại dùng ~2,5 s
MAX_AM_TIET_CLIP = 26   # clip Veo 8 s
TONG_MIN, TONG_MAX, TONG_CUNG = 100, 135, 178

CAU_MO = "Chào cả nhà, chuyện nghề sầu riêng hôm nay, Tuấn Thủy lại kể mọi người nghe."
KET_1 = "Có hàng cần bán, bà con cứ tham khảo Nông Sản Tuấn Thủy xem sao nha. Mình cùng trao đổi rõ ràng, thuận mua vừa bán, ai cũng vui."
KET_2 = "Cảm ơn bà con đã tin tưởng và hẹn gặp lại trong những vườn sầu riêng."

NHAN_VAT = {
    "Nguoi Ke": "white collared shirt, beige wide-leg trousers",
    "Em Tuan": "short spiky black hair, black polo shirt",
    "Chu Nam": "faded light grey striped long-sleeve work shirt",  # thay Cô Hai từ 30/09
    "Bay Loi": "plain camouflage bucket hat with no badge",
    "Thang Lanh": "slicked hair, thin mustache",
    # Nhân vật mới — chủ kênh duyệt 30/09/2026
    "Chu Tu": "faded plaid shirt, checkered krama scarf",
    "Ut Nho": "black square glasses, long black hair in a high ponytail",
    "Sau Tai": "orange high-visibility work shirt",
    "Ba Tam": "grey hair in a bun, light blue blouse",
}
CAM = ["Chu Ba", "Ong Sau Cu"]
PHAN = ["HOOK", "CAU_MO", "BOI_CANH", "VONG_LAP", "LEO_THANG", "DINH_DIEM", "HOA_GIAI",
        "GOC_NHIN", "MEO", "CAU_HOI_2_PHE", "KET_1", "KET_2"]
BOI_CANH = ["vuon", "kho", "bai_can"]
KHUNG = ["toan", "can", "dac_ta"]


def am_tiet(loi: str) -> int:
    return len(re.findall(r"[^\W\d_]+", loi))


def kieu(data: dict) -> str:
    return data.get("kieu") or ("thoai" if data.get("canh") and "thoai" in data["canh"][0] else "nguoi_ke")


def loi_canh(c: dict) -> str:
    """Toàn bộ lời của 1 cảnh (v3: nối các câu thoại)."""
    if "thoai" in c:
        return " ".join(t["cau"] for t in c["thoai"])
    return c.get("loi", "")


def giay(c: dict, k: str) -> float:
    n = am_tiet(loi_canh(c))
    if k == "thoai":
        return n / TOC_DO + NHIP if n else IM_LANG
    return n / TOC_DO + NGHI


def mmss(s: float) -> str:
    s = int(round(s))
    return f"{s // 60}:{s % 60:02d}"


def kiem_tra(data: dict):
    loi_nang, canh_bao = [], []
    k = kieu(data)
    for f in ("ma_video", "chu_de", "tieu_de_tam", "canh"):
        if f not in data:
            loi_nang.append(f"thiếu trường '{f}'")
    canh = data.get("canh", [])
    if not 16 <= len(canh) <= 30:
        canh_bao.append(f"số cảnh {len(canh)} (nên 18–26)")
    tong = 0.0
    for i, c in enumerate(canh, 1):
        so = c.get("so", f"#{i}")
        if so != f"S{i:02d}":
            loi_nang.append(f"{so}: số cảnh phải là S{i:02d}")
        if c.get("phan") not in PHAN:
            loi_nang.append(f"{so}: phan '{c.get('phan')}' không hợp lệ")
        if c.get("boi_canh") not in BOI_CANH:
            loi_nang.append(f"{so}: boi_canh '{c.get('boi_canh')}' không hợp lệ")
        loi = loi_canh(c)
        if re.search(r"\d", loi):
            loi_nang.append(f"{so}: lời có chữ số — phải viết bằng chữ: {loi}")
        n = am_tiet(loi)
        prompt = c.get("prompt_flow", "")
        if k == "thoai":
            if n > MAX_AM_TIET_CLIP:
                loi_nang.append(f"{so}: {n} âm tiết > {MAX_AM_TIET_CLIP} — không vừa clip 8 giây, tách cảnh")
            for t in c.get("thoai", []):
                if t.get("nv") not in c.get("nhan_vat", []):
                    loi_nang.append(f"{so}: người nói '{t.get('nv')}' không có trong nhan_vat")
                if f'"{t.get("cau")}"' not in prompt:
                    loi_nang.append(f"{so}: prompt thiếu nguyên văn câu thoại của {t.get('nv')}")
            if len(c.get("thoai", [])) > 2:
                canh_bao.append(f"{so}: hơn 2 lượt thoại trong 1 clip — Veo dễ lẫn giọng")
            for x in c.get("cat", []):
                if x.partition("@")[0] not in KHUNG:
                    loi_nang.append(f"{so}: khung cắt '{x}' không hợp lệ ({', '.join(KHUNG)})")
            if "Vietnamese" not in prompt:
                loi_nang.append(f"{so}: prompt phải ghi rõ nói tiếng Việt (Vietnamese)")
            if not prompt.rstrip().endswith("No music, no subtitles, no on-screen text."):
                loi_nang.append(f"{so}: prompt phải kết thúc bằng 'No music, no subtitles, no on-screen text.'")
        else:
            if not 14 <= n <= 28:
                canh_bao.append(f"{so}: {n} âm tiết (nên 18–27)")
            if not prompt.rstrip().endswith("No dialogue, no music, no on-screen text."):
                loi_nang.append(f"{so}: prompt phải kết thúc bằng 'No dialogue, no music, no on-screen text.'")
        tong += giay(c, k)
        for nv in c.get("nhan_vat", []):
            if nv in CAM:
                loi_nang.append(f"{so}: nhân vật cấm '{nv}'")
            elif nv not in NHAN_VAT:
                loi_nang.append(f"{so}: nhân vật lạ '{nv}' (chưa được chủ kênh duyệt)")
            elif NHAN_VAT[nv] not in prompt:
                loi_nang.append(f"{so}: prompt thiếu mô tả của {nv}")
        for nv in CAM:
            if nv in prompt:
                loi_nang.append(f"{so}: prompt chứa nhân vật cấm '{nv}'")
        if "Setting:" not in prompt:
            loi_nang.append(f"{so}: prompt thiếu 'Setting:'")
    theo_phan = {}  # câu cố định dài có thể tách nhiều cảnh liên tiếp cùng phần → nối lại
    for c in canh:
        theo_phan[c.get("phan")] = " ".join(x for x in (theo_phan.get(c.get("phan")), loi_canh(c)) if x)
    for phan, mau in (("CAU_MO", CAU_MO), ("KET_1", KET_1), ("KET_2", KET_2)):
        if theo_phan.get(phan) != mau:
            loi_nang.append(f"{phan}: phải đúng câu cố định")
    if not TONG_MIN <= tong <= TONG_MAX:
        canh_bao.append(f"tổng ước tính {mmss(tong)} (mục tiêu 1:40–2:15)")
    if tong > TONG_CUNG:
        loi_nang.append(f"tổng ước tính {mmss(tong)} vượt 2:58")
    return loi_nang, canh_bao, tong


TEN = {"Nguoi Ke": "Tuấn Thủy", "Em Tuan": "Em Tuấn", "Chu Nam": "Chú Năm", "Co Hai": "Cô Hai", "Bay Loi": "Bảy Lợi",
       "Thang Lanh": "Thắng Lanh", "Chu Tu": "Chú Tư", "Ut Nho": "Út Nhỏ", "Sau Tai": "Anh Sáu Tài", "Ba Tam": "Bà Tám"}


def xuat_md(data: dict, path: Path):
    k = kieu(data)
    dong = [f"# {data['ma_video']} — {data['tieu_de_tam']}", "",
            f"**Kiểu:** {'nhân vật tự thoại (v3)' if k == 'thoai' else 'người kể UV07 (v2)'} · "
            f"**Phiên bản:** {data.get('phien_ban', 1)}", "",
            f"**Chủ đề:** {data['chu_de']}", "", f"**Ghi chú:** {data.get('ghi_chu', '')}", "", "## Bảng tính", ""]
    dong += [f"- `{a}`: {b}" for a, b in data.get("bang_tinh", {}).items()]
    dong += ["", "## Kịch bản theo từng khung (thời gian ước tính)", ""]
    if k == "thoai":
        dong += ["| Cảnh | Giây | Phần | Bối cảnh | Nhân vật | Lời thoại | Cắt khung | Chữ trên màn hình |",
                 "|---|---|---|---|---|---|---|---|"]
    else:
        dong += ["| Cảnh | Giây | Phần | Bối cảnh | Nhân vật | Lời đọc (UV07) | Chữ trên màn hình |",
                 "|---|---|---|---|---|---|---|"]
    t = 0.0
    for c in data["canh"]:
        g = giay(c, k)
        nv = ", ".join(TEN.get(x, x) for x in c["nhan_vat"]) or "—"
        if k == "thoai":
            thoai = "<br>".join(f"**{TEN.get(x['nv'], x['nv'])}:** {x['cau']}" for x in c["thoai"]) or "(không thoại)"
            dong.append(f"| {c['so']} | {mmss(t)}–{mmss(t + g)} | {c['phan']} | {c['boi_canh']} | {nv} | {thoai} | "
                        f"{' → '.join(c.get('cat', []))} | {c.get('chu_man_hinh', '')} |")
        else:
            dong.append(f"| {c['so']} | {mmss(t)}–{mmss(t + g)} | {c['phan']} | {c['boi_canh']} | {nv} | {c['loi']} | "
                        f"{c.get('chu_man_hinh', '')} |")
        t += g
    dong += ["", f"**Tổng ước tính:** {mmss(t)}", "", "## Prompt Google Flow (Veo 3.1, 16:9, x1)", ""]
    for c in data["canh"]:
        dong += [f"### {c['so']} — {c['phan']}", "", "```", c["prompt_flow"], "```", ""]
    path.write_text("\n".join(dong), encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    p = Path(sys.argv[1])
    data = json.loads(p.read_text(encoding="utf-8"))
    loi_nang, canh_bao, tong = kiem_tra(data)
    print(f"{data.get('ma_video')} [{kieu(data)}]: {len(data.get('canh', []))} cảnh, ước tính {mmss(tong)}")
    for x in canh_bao:
        print("  CẢNH BÁO:", x)
    for x in loi_nang:
        print("  LỖI:", x)
    if "--md" in sys.argv:
        xuat_md(data, p.with_name("kich_ban.md"))
        print("  đã ghi", p.with_name("kich_ban.md"))
    print("OK" if not loi_nang else "CHƯA ĐẠT")
    sys.exit(1 if loi_nang else 0)


if __name__ == "__main__":
    main()
