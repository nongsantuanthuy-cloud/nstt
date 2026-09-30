#!/usr/bin/env python3
"""Kiểm tra canh.json của kênh NSTT và (tùy chọn) xuất kich_ban.md.

    python3 tools/kiem_tra_kich_ban.py kich_ban/<ma>/canh.json [--md]

Kiểm tra: trường bắt buộc, phần (phan) hợp lệ, nhân vật hợp lệ + mô tả có trong prompt,
chữ số trong lời, câu mở/kết cố định, số âm tiết mỗi câu, tổng thời lượng ước tính.
Tốc độ ước tính hiệu chỉnh theo bản mẫu NSTT-20260929-MAU v10 (22 cảnh ≈ 2:10):
thời lượng cảnh ≈ âm_tiết / 4,0 + 0,8 giây.
"""
import json, re, sys
from pathlib import Path

TOC_DO = 4.0      # âm tiết / giây (UV07)
NGHI = 0.8        # giây nghỉ giữa cảnh
TONG_MIN, TONG_MAX, TONG_CUNG = 110, 135, 178

CAU_MO = "Chào bà con. Chuyện nghề sầu riêng hôm nay, Tuấn Thủy kể bà con nghe."
KET_1 = "Có hàng cần bán, bà con cứ gọi Tuấn Thủy. Mình cùng trao đổi rõ ràng, thuận mua vừa bán, ai cũng vui."
KET_2 = "Cảm ơn bà con đã tin tưởng và hẹn gặp lại trong những vườn sầu riêng."

NHAN_VAT = {
    "Nguoi Ke": "white collared shirt, beige wide-leg trousers",
    "Em Tuan": "short spiky black hair, black polo shirt",
    "Co Hai": "dark brown ba ba shirt",
    "Bay Loi": "plain camouflage bucket hat with no badge",
    "Thang Lanh": "slicked hair, thin mustache",
}
CAM = ["Chu Ba", "Ong Sau Cu"]
PHAN = ["HOOK", "CAU_MO", "BOI_CANH", "VONG_LAP", "LEO_THANG", "DINH_DIEM", "HOA_GIAI",
        "GOC_NHIN", "MEO", "CAU_HOI_2_PHE", "KET_1", "KET_2"]
BOI_CANH = ["vuon", "kho", "bai_can"]


def am_tiet(loi: str) -> int:
    return len(re.findall(r"[^\W\d_]+", loi))


def giay(loi: str) -> float:
    return am_tiet(loi) / TOC_DO + NGHI


def mmss(s: float) -> str:
    return f"{int(s // 60)}:{int(round(s % 60)):02d}"


def kiem_tra(data: dict):
    loi_nang, canh_bao = [], []
    for k in ("ma_video", "chu_de", "tieu_de_tam", "canh"):
        if k not in data:
            loi_nang.append(f"thiếu trường '{k}'")
    canh = data.get("canh", [])
    if not 16 <= len(canh) <= 24:
        canh_bao.append(f"số cảnh {len(canh)} (nên 18–22)")
    tong = 0.0
    for i, c in enumerate(canh, 1):
        so = c.get("so", f"#{i}")
        if so != f"S{i:02d}":
            loi_nang.append(f"{so}: số cảnh phải là S{i:02d}")
        if c.get("phan") not in PHAN:
            loi_nang.append(f"{so}: phan '{c.get('phan')}' không hợp lệ")
        if c.get("boi_canh") not in BOI_CANH:
            loi_nang.append(f"{so}: boi_canh '{c.get('boi_canh')}' không hợp lệ")
        loi = c.get("loi", "")
        if re.search(r"\d", loi):
            loi_nang.append(f"{so}: lời có chữ số — phải viết bằng chữ: {loi}")
        n = am_tiet(loi)
        if not 14 <= n <= 28:
            canh_bao.append(f"{so}: {n} âm tiết (nên 18–27)")
        tong += giay(loi)
        prompt = c.get("prompt_flow", "")
        for nv in c.get("nhan_vat", []):
            if nv in CAM:
                loi_nang.append(f"{so}: nhân vật cấm '{nv}'")
            elif nv not in NHAN_VAT:
                loi_nang.append(f"{so}: nhân vật lạ '{nv}' (chưa được chủ kênh duyệt)")
            elif nv not in prompt or NHAN_VAT[nv] not in prompt:
                loi_nang.append(f"{so}: prompt thiếu tên/mô tả của {nv}")
        for nv in CAM:
            if nv in prompt:
                loi_nang.append(f"{so}: prompt chứa nhân vật cấm '{nv}'")
        if "Setting:" not in prompt:
            loi_nang.append(f"{so}: prompt thiếu 'Setting:'")
        if not prompt.rstrip().endswith("No dialogue, no music, no on-screen text."):
            loi_nang.append(f"{so}: prompt phải kết thúc bằng 'No dialogue, no music, no on-screen text.'")
    theo_phan = {c.get("phan"): c.get("loi") for c in canh}
    for phan, mau in (("CAU_MO", CAU_MO), ("KET_1", KET_1), ("KET_2", KET_2)):
        if theo_phan.get(phan) != mau:
            loi_nang.append(f"{phan}: phải đúng câu cố định")
    if not TONG_MIN <= tong <= TONG_MAX:
        canh_bao.append(f"tổng ước tính {mmss(tong)} (mục tiêu 1:50–2:15)")
    if tong > TONG_CUNG:
        loi_nang.append(f"tổng ước tính {mmss(tong)} vượt 2:58")
    return loi_nang, canh_bao, tong


def xuat_md(data: dict, path: Path):
    dong = [f"# {data['ma_video']} — {data['tieu_de_tam']}", "",
            f"**Chủ đề:** {data['chu_de']}", "", f"**Ghi chú:** {data.get('ghi_chu', '')}", "",
            "## Bảng tính", ""]
    dong += [f"- `{k}`: {v}" for k, v in data.get("bang_tinh", {}).items()]
    dong += ["", "## Kịch bản theo từng khung (thời gian ước tính)", "",
             "| Cảnh | Giây | Phần | Bối cảnh | Nhân vật | Lời đọc (UV07) | Chữ trên màn hình |",
             "|---|---|---|---|---|---|---|"]
    t = 0.0
    for c in data["canh"]:
        d = giay(c["loi"])
        dong.append(f"| {c['so']} | {mmss(t)}–{mmss(t + d)} | {c['phan']} | {c['boi_canh']} | "
                    f"{', '.join(c['nhan_vat']) or '—'} | {c['loi']} | {c.get('chu_man_hinh', '')} |")
        t += d
    dong += ["", f"**Tổng ước tính:** {mmss(t)}", "", "## Prompt Google Flow (Veo 3.1 Lite, 16:9, x1)", ""]
    for c in data["canh"]:
        dong += [f"### {c['so']} — {c['phan']}", "", "```", c["prompt_flow"], "```", ""]
    path.write_text("\n".join(dong), encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    p = Path(sys.argv[1])
    data = json.loads(p.read_text(encoding="utf-8"))
    loi_nang, canh_bao, tong = kiem_tra(data)
    print(f"{data.get('ma_video')}: {len(data.get('canh', []))} cảnh, ước tính {mmss(tong)}")
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
