"""
Manor Lords - Game Update Translation Diff Checker
===================================================
Công cụ tự động phát hiện các thay đổi nội dung tiếng Anh (EN) và các Key mới
được thêm vào sau mỗi bản cập nhật của Manor Lords.

Tính năng:
1. Tự động tìm kiếm file PAK chứa DataTable dịch thuật trong thư mục game.
2. Trích xuất file nhị phân UE5 (.uasset / .uexp) bằng repak.exe.
3. Parse cấu trúc nhị phân DataTable UE5.5 chuẩn xác (NameMap FName + FString 19 ngôn ngữ).
4. So sánh với bản dịch hiện tại:
   - Phát hiện các chuỗi Tiếng Anh bị Dev sửa đổi (Modified EN).
   - Phát hiện các Key mới xuất hiện (New Keys).
   - Hiển thị bản dịch Tiếng Việt hiện tại để dịch giả tiện đối chiếu.
5. Xuất báo cáo chi tiết Markdown và JSON, đồng thời tạo template để dịch ngay.
"""

import os
import sys
import glob
import json
import struct
import argparse
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
TOOLS_DIR = os.path.join(PROJECT_ROOT, "tools")
TRANS_DIR = os.path.join(PROJECT_ROOT, "translations")
OLD_EXTRACTED_DIR = os.path.join(PROJECT_ROOT, "extracted", "ManorLords", "Content", "Translation", "HoodedHorse")
REPAK_EXE = os.path.join(TOOLS_DIR, "repak.exe")
AES_KEY = "0xD7D2FFA2744D18A7B84DFF09591C212C2068413A23BA3967F9890A6654989321"

DEFAULT_GAME_PATHS = [
    r"C:\Users\nam\Downloads\Compressed\Manor-Lords-AnkerGames",
    r"C:\Users\nam\Downloads\Compressed\Manor-Lords-AnkerGames_2",
    r"C:\Program Files (x86)\Steam\steamapps\common\Manor Lords",
    r"D:\SteamLibrary\steamapps\common\Manor Lords"
]

def parse_uasset_names(uasset_path):
    """Đọc NameMap từ header của file .uasset UE5"""
    with open(uasset_path, "rb") as f:
        data = f.read()
    
    pos = 24
    custom_ver_count, = struct.unpack_from("<i", data, pos)
    pos += 4 + custom_ver_count * 20
    
    total_hdr_size, = struct.unpack_from("<i", data, pos)
    pos += 4
    
    fn_len, = struct.unpack_from("<i", data, pos)
    pos += 4
    if fn_len > 0:
        pos += fn_len
    elif fn_len < 0:
        pos += (-fn_len) * 2
        
    pkg_flags, = struct.unpack_from("<I", data, pos)
    pos += 4
    
    name_count, name_offset = struct.unpack_from("<ii", data, pos)
    
    names = []
    n_pos = name_offset
    for i in range(name_count):
        s_len, = struct.unpack_from("<i", data, n_pos)
        n_pos += 4
        if s_len > 0:
            s = data[n_pos:n_pos+s_len-1].decode("utf-8", errors="replace")
            n_pos += s_len
        elif s_len < 0:
            s_len = -s_len
            s = data[n_pos:n_pos+s_len*2-2].decode("utf-16le", errors="replace")
            n_pos += s_len * 2
        else:
            s = ""
        n_pos += 4  # Non-case hash (2) + Case hash (2)
        names.append(s)
        
    return names

def read_fstring(data, pos):
    """Đọc một FString từ mảng byte tại vị trí pos (hỗ trợ cả UTF-8 và UTF-16 LE)"""
    slen, = struct.unpack_from("<i", data, pos)
    if slen > 0:
        total = 4 + slen
        text = data[pos+4:pos+4+slen-1].decode("utf-8", errors="replace")
    elif slen < 0:
        total = 4 + (-slen)*2
        text = data[pos+4:pos+4+(-slen)*2-2].decode("utf-16le", errors="replace")
    else:
        total = 4
        text = ""
    return slen, total, text

def parse_datatable(uasset_path, uexp_path):
    """Parse toàn bộ các hàng (Row Name, English Text, Offset, Length) từ cặp file .uasset và .uexp"""
    names = parse_uasset_names(uasset_path)
    with open(uexp_path, "rb") as f:
        data = f.read()
    
    num_rows, = struct.unpack_from("<i", data, 10)
    pos = 14
    rows = []
    
    for r in range(num_rows):
        if pos >= len(data):
            break
        name_idx, name_num = struct.unpack_from("<ii", data, pos)
        r_name = names[name_idx] if name_idx < len(names) else f"name_{name_idx}"
        if name_num > 0:
            r_name = f"{r_name}_{name_num}"
            
        en_offset = pos + 10
        slen, total, en_text = read_fstring(data, en_offset)
        rows.append({
            "key": r_name,
            "en": en_text,
            "offset": en_offset,
            "length": abs(slen)
        })
        
        # Nhảy qua 19 cột ngôn ngữ của hàng này
        cur = en_offset
        for _ in range(19):
            if cur >= len(data):
                break
            _, c_tot, _ = read_fstring(data, cur)
            cur += c_tot
        pos = cur

    return num_rows, rows

def find_game_paks_dir(base_game_path):
    """Tìm thư mục Content/Paks từ đường dẫn game gốc"""
    candidates = [
        os.path.join(base_game_path, "Content", "Paks"),
        os.path.join(base_game_path, "ManorLords", "Content", "Paks"),
        os.path.join(base_game_path, "Manor Lords", "ManorLords", "Content", "Paks")
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None

def extract_translation_from_game(paks_dir, output_dir):
    """Trích xuất file translation từ các file PAK của game"""
    if not os.path.exists(REPAK_EXE):
        raise FileNotFoundError(f"Không tìm thấy repak.exe tại: {REPAK_EXE}")

    os.makedirs(output_dir, exist_ok=True)
    pak_files = sorted(glob.glob(os.path.join(paks_dir, "*.pak")))
    if not pak_files:
        raise FileNotFoundError(f"Không tìm thấy file .pak nào trong {paks_dir}")

    print(f"[*] Đang tìm kiếm DataTable dịch thuật trong {len(pak_files)} file PAK...")
    target_pak = None

    # Kiểm tra các pak có khả năng chứa Translation trước (s15, s16, s14, ...)
    priority_paks = sorted(pak_files, key=lambda p: 0 if "s15" in p or "s16" in p else 1)

    for pak in priority_paks:
        try:
            cmd = [REPAK_EXE, "--aes-key", AES_KEY, "list", pak]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if "DT_Translation" in res.stdout:
                target_pak = pak
                print(f"  -> Tìm thấy DataTable dịch thuật tại: {os.path.basename(pak)}")
                break
        except Exception:
            continue

    if not target_pak:
        raise RuntimeError("Không tìm thấy DataTable dịch thuật trong bất kỳ file PAK nào.")

    print(f"[*] Đang giải nén file Translation từ {os.path.basename(target_pak)}...")
    unpack_cmd = [
        REPAK_EXE, "--aes-key", AES_KEY, "unpack",
        "-o", output_dir,
        "-i", "ManorLords/Content/Translation/HoodedHorse/*",
        "-f", target_pak
    ]
    subprocess.run(unpack_cmd, check=True, stdout=subprocess.PIPE)
    print("  -> Giải nén thành công!")

def check_game_update(game_dir=None, export_template=True):
    print("================================================================================")
    print("🏰 MANOR LORDS - CÔNG CỤ TỰ ĐỘNG PHÁT HIỆN SỬA ĐỔI / THÊM KEY TIẾNG ANH (EN)")
    print("================================================================================\n")

    # Xác định thư mục game
    selected_game_dir = None
    if game_dir and os.path.exists(game_dir):
        selected_game_dir = game_dir
    else:
        for p in DEFAULT_GAME_PATHS:
            if os.path.exists(p):
                selected_game_dir = p
                break

    if not selected_game_dir:
        print("[!] LỖI: Không tìm thấy thư mục game Manor Lords!")
        print("    Vui lòng truyền đường dẫn thư mục game vào tham số:")
        print("    python check_game_update.py \"C:\\Path\\To\\Manor-Lords\"")
        return

    print(f"[+] Thư mục game phát hiện: {selected_game_dir}")
    paks_dir = find_game_paks_dir(selected_game_dir)
    if not paks_dir:
        print(f"[!] Không tìm thấy thư mục Content/Paks bên trong: {selected_game_dir}")
        return
    print(f"[+] Thư mục Paks: {paks_dir}")

    # Thư mục giải nén tạm
    extracted_fresh_dir = os.path.join(PROJECT_ROOT, "extracted_fresh")
    hooded_fresh_dir = os.path.join(extracted_fresh_dir, "ManorLords", "Content", "Translation", "HoodedHorse")

    # Giải nén
    extract_translation_from_game(paks_dir, extracted_fresh_dir)

    if not os.path.exists(hooded_fresh_dir):
        print(f"[!] Không tìm thấy thư mục giải nén HoodedHorse: {hooded_fresh_dir}")
        return

    # Quét tất cả file DataTable
    fresh_uassets = sorted(glob.glob(os.path.join(hooded_fresh_dir, "*.uasset")))
    print(f"\n[*] Đang phân tích {len(fresh_uassets)} bảng dịch thuật từ game cập nhật mới...\n")

    total_modified_en = []
    total_new_keys = []
    total_removed_keys = []
    table_stats = []

    for uasset_path in fresh_uassets:
        table_name = os.path.basename(uasset_path).replace(".uasset", "")
        uexp_path = uasset_path.replace(".uasset", ".uexp")
        if not os.path.exists(uexp_path):
            continue

        num_fresh_rows, fresh_rows = parse_datatable(uasset_path, uexp_path)
        fresh_dict = {r["key"]: r for r in fresh_rows}

        # Đọc dữ liệu cũ từ extracted/ và translations/
        old_uasset = os.path.join(OLD_EXTRACTED_DIR, f"{table_name}.uasset")
        old_uexp = os.path.join(OLD_EXTRACTED_DIR, f"{table_name}.uexp")
        old_dict = {}
        if os.path.exists(old_uasset) and os.path.exists(old_uexp):
            _, old_rows = parse_datatable(old_uasset, old_uexp)
            old_dict = {r["key"]: r for r in old_rows}

        # Đọc bản dịch hiện tại từ translations/
        json_path = os.path.join(TRANS_DIR, f"{table_name}.json")
        trans_vi_by_key = {}
        trans_vi_by_en = {}
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as jf:
                    for item in json.load(jf):
                        k = item.get("key", "")
                        en = item.get("en", "")
                        vi = item.get("vi", "")
                        if k: trans_vi_by_key[k] = vi
                        if en: trans_vi_by_en[en] = vi
            except Exception:
                pass

        table_mod = []
        table_new = []
        table_rem = []

        # Kiểm tra key mới và key bị sửa EN
        for k, nr in fresh_dict.items():
            if k not in old_dict:
                table_new.append({
                    "table": table_name,
                    "key": k,
                    "en": nr["en"],
                    "offset": nr["offset"],
                    "length": nr["length"]
                })
            else:
                old_en = old_dict[k]["en"]
                new_en = nr["en"]
                if old_en.strip() != new_en.strip():
                    curr_vi = trans_vi_by_key.get(k) or trans_vi_by_en.get(old_en, "")
                    table_mod.append({
                        "table": table_name,
                        "key": k,
                        "old_en": old_en,
                        "new_en": new_en,
                        "current_vi": curr_vi,
                        "new_offset": nr["offset"],
                        "new_length": nr["length"]
                    })

        # Kiểm tra key bị xóa
        for k in old_dict:
            if k not in fresh_dict:
                table_rem.append({
                    "table": table_name,
                    "key": k
                })

        total_modified_en.extend(table_mod)
        total_new_keys.extend(table_new)
        total_removed_keys.extend(table_rem)

        table_stats.append({
            "table": table_name,
            "total_rows": len(fresh_rows),
            "new": len(table_new),
            "modified": len(table_mod),
            "removed": len(table_rem)
        })

        if table_new or table_mod or table_rem:
            print(f"  📌 [{table_name:<36}] +{len(table_new):2d} Mới | ~{len(table_mod):2d} Sửa EN | -{len(table_rem):2d} Bị xóa | Tổng: {len(fresh_rows):3d}")
        else:
            print(f"  ✅ [{table_name:<36}] Đồng bộ 100% (Tổng {len(fresh_rows):3d} chuỗi)")

    # Báo cáo tổng kết
    print("\n" + "="*80)
    print("📊 BÁO CÁO TỔNG KẾT THAY ĐỔI DỮ LIỆU:")
    print(f"   • Tổng số bảng kiểm tra:             {len(fresh_uassets)}")
    print(f"   • Tổng số Key MỚI ĐƯỢC THÊM VÀO:    {len(total_new_keys)}")
    print(f"   • Tổng số chuỗi EN BỊ DEV SỬA ĐỔI:  {len(total_modified_en)}")
    print(f"   • Tổng số Key BỊ DEV XÓA:           {len(total_removed_keys)}")
    print("="*80 + "\n")

    # In chi tiết các chuỗi sửa đổi
    if total_modified_en:
        print("🚨 CHI TIẾT CÁC CHUỖI TIẾNG ANH ĐÃ BỊ THAY ĐỔI (CẦN CẬP NHẬT DỊCH LẠI):")
        for i, item in enumerate(total_modified_en, 1):
            print(f"\n[{i:2d}] Bảng: {item['table']} | Key: {item['key']}")
            print(f"     [EN CŨ] : {item['old_en']}")
            print(f"     [EN MỚI]: {item['new_en']}")
            if item['current_vi']:
                print(f"     [VI CŨ] : {item['current_vi']}")

    if total_new_keys:
        print("\n" + "-"*80)
        print(f"✨ DANH SÁCH KEY MỚI CẦN DỊCH ({len(total_new_keys)} keys):")
        for i, item in enumerate(total_new_keys, 1):
            print(f"[{i:2d}] {item['table']:<32} | Key: {item['key']:<26} | EN: '{item['en'][:60]}'")

    # Xuất file JSON
    report_json_path = os.path.join(PROJECT_ROOT, "update_diff_report.json")
    with open(report_json_path, "w", encoding="utf-8") as jf:
        json.dump({
            "game_path": selected_game_dir,
            "summary": {
                "total_tables": len(fresh_uassets),
                "total_new_keys": len(total_new_keys),
                "total_modified_en": len(total_modified_en),
                "total_removed_keys": len(total_removed_keys)
            },
            "table_stats": table_stats,
            "modified_en": total_modified_en,
            "new_keys": total_new_keys,
            "removed_keys": total_removed_keys
        }, jf, ensure_ascii=False, indent=2)
    print(f"\n[✔] Đã lưu báo cáo JSON tại: {report_json_path}")

    # Xuất file Markdown
    report_md_path = os.path.join(PROJECT_ROOT, "update_diff_report.md")
    with open(report_md_path, "w", encoding="utf-8") as mf:
        mf.write("# 🏰 Manor Lords - Báo Cáo Thay Đổi Bản Cập Nhật (Update Diff Report)\n\n")
        mf.write(f"- **Thư mục game:** `{selected_game_dir}`\n")
        mf.write(f"- **Tổng số Key Mới:** **{len(total_new_keys)}**\n")
        mf.write(f"- **Tổng số Chuỗi EN Bị Sửa:** **{len(total_modified_en)}**\n")
        mf.write(f"- **Tổng số Key Bị Xóa:** **{len(total_removed_keys)}**\n\n")
        
        mf.write("## 1. Chi Tiết Chuỗi Tiếng Anh Bị Thay Đổi (Cần cập nhật dịch lại)\n\n")
        if total_modified_en:
            for i, item in enumerate(total_modified_en, 1):
                mf.write(f"### {i}. `{item['table']}` → `{item['key']}`\n")
                mf.write(f"- **EN Cũ:** {item['old_en']}\n")
                mf.write(f"- **EN Mới:** {item['new_en']}\n")
                if item['current_vi']:
                    mf.write(f"- **VI Hiện Tại:** {item['current_vi']}\n")
                mf.write("\n")
        else:
            mf.write("Không có chuỗi tiếng Anh nào bị thay đổi.\n\n")

        mf.write("## 2. Chi Tiết Các Key Mới Cần Dịch Thuật\n\n")
        if total_new_keys:
            mf.write("| # | Bảng | Key | Nội dung Tiếng Anh (EN) |\n")
            mf.write("|---|---|---|---|\n")
            for i, item in enumerate(total_new_keys, 1):
                en_safe = item['en'].replace("\n", " ").replace("|", "\\|")
                mf.write(f"| {i} | `{item['table']}` | `{item['key']}` | {en_safe} |\n")
            mf.write("\n")
        else:
            mf.write("Không có key mới nào.\n\n")

    print(f"[✔] Đã lưu báo cáo Markdown tại: {report_md_path}")

    # Xuất template cần dịch (translations_pending_update.json) nếu được bật
    if export_template and (total_modified_en or total_new_keys):
        pending_path = os.path.join(PROJECT_ROOT, "translations_pending_update.json")
        pending_list = []
        for m in total_modified_en:
            pending_list.append({
                "type": "MODIFIED_EN",
                "table": m["table"],
                "key": m["key"],
                "old_en": m["old_en"],
                "en": m["new_en"],
                "current_vi": m["current_vi"],
                "vi": ""  # Chỗ để dịch mới
            })
        for n in total_new_keys:
            pending_list.append({
                "type": "NEW_KEY",
                "table": n["table"],
                "key": n["key"],
                "en": n["en"],
                "vi": ""  # Chỗ để dịch mới
            })
        with open(pending_path, "w", encoding="utf-8") as pf:
            json.dump(pending_list, pf, ensure_ascii=False, indent=2)
        print(f"[✔] Đã tạo file template dịch thuật ({len(pending_list)} mục) tại: {pending_path}")

    print("\n🎉 Hoàn thành kiểm tra thay đổi!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manor Lords Translation Diff Checker")
    parser.add_argument("game_dir", nargs="?", default=None, help="Đường dẫn thư mục game cập nhật")
    parser.add_argument("--no-template", action="store_true", help="Không tạo file template pending")
    args = parser.parse_args()

    check_game_update(game_dir=args.game_dir, export_template=not args.no_template)
