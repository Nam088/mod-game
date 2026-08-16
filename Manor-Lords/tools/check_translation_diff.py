import os
import sys
import json
import glob
import struct
import difflib

sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
EXTRACTED_DIR = os.path.join(PROJECT_ROOT, "extracted", "ManorLords", "Content", "Translation", "HoodedHorse")
TRANS_DIR = os.path.join(PROJECT_ROOT, "translations")

def extract_strings_from_uexp(uexp_path):
    """Trích xuất danh sách tất cả FString hiện có từ file binary .uexp gốc mới nhất của game"""
    if not os.path.exists(uexp_path):
        return []
    with open(uexp_path, "rb") as f:
        data = f.read()
    
    pos = 0
    extracted = []
    while pos < len(data) - 4:
        length, = struct.unpack_from("<i", data, pos)
        if 1 < length < 3000 and pos + 4 + length <= len(data):
            s_bytes = data[pos+4:pos+4+length]
            if s_bytes[-1] == 0:
                try:
                    s = s_bytes[:-1].decode("utf-8")
                    if len(s) >= 1 and not any(ord(c) < 32 and c not in '\r\n\t' for c in s):
                        extracted.append({
                            "offset": pos,
                            "length": length,
                            "text": s
                        })
                        pos += 4 + length - 1
                except:
                    pass
        pos += 1
    return extracted

def detect_dev_updates():
    print("=======================================================")
    print("🔍 MANOR LORDS - CÔNG CỤ PHÁT HIỆN DEV CẬP NHẬT / SỬA TEXT TIẾNG ANH (EN)")
    print("=======================================================\n")

    if not os.path.exists(EXTRACTED_DIR):
        print(f"[!] Không tìm thấy thư mục template game gốc: {EXTRACTED_DIR}")
        print("    Vui lòng trích xuất dữ liệu game mới vào thư mục 'extracted/' trước.")
        return

    json_files = sorted(glob.glob(os.path.join(TRANS_DIR, "DT_Translation_*.json")))
    
    total_modified_en = []
    total_new_keys = []
    total_removed_keys = []

    print("[*] Đang so sánh dữ liệu bản dịch hiện tại với dữ liệu nhị phân game gốc mới nhất...\n")

    for json_path in json_files:
        table_name = os.path.basename(json_path)
        base_name = os.path.splitext(table_name)[0]
        uexp_path = os.path.join(EXTRACTED_DIR, f"{base_name}.uexp")

        if not os.path.exists(uexp_path):
            continue

        with open(json_path, "r", encoding="utf-8") as f:
            current_entries = json.load(f)

        # Trích xuất chuỗi từ file uexp mới của game
        fresh_extracted = extract_strings_from_uexp(uexp_path)
        fresh_dict_by_offset = {e["offset"]: e["text"] for e in fresh_extracted}

        modified_in_table = []
        new_in_table = []

        for entry in current_entries:
            offset = entry.get("offset")
            curr_en = entry.get("en", "")
            key = entry.get("key", "")
            curr_vi = entry.get("vi", "")

            if offset in fresh_dict_by_offset:
                fresh_en = fresh_dict_by_offset[offset]
                # Kiểm tra nếu text tiếng Anh gốc của game đã bị Dev sửa đổi
                if fresh_en != curr_en:
                    modified_in_table.append({
                        "table": table_name,
                        "key": key,
                        "old_en": curr_en,
                        "new_en": fresh_en,
                        "current_vi": curr_vi
                    })
            else:
                # Key có thể bị đổi offset hoặc dev xóa bớt
                pass

        if modified_in_table:
            total_modified_en.extend(modified_in_table)
            print(f"  🚨 [{table_name}] Phát hiện {len(modified_in_table)} chuỗi tiếng Anh BỊ DEV SỬA ĐỔI NỘI DUNG!")
        else:
            print(f"  ✅ [{table_name:<38}] Text tiếng Anh đồng bộ 100% với game gốc.")

    print("\n-------------------------------------------------------")
    print(f"📊 BÁO CÁO PHÁT HIỆN SỬA ĐỔI TIẾNG ANH TỪ DEV GAME:")
    print(f"   • Tổng số chuỗi EN bị sửa đổi: {len(total_modified_en)}")
    print("-------------------------------------------------------\n")

    if total_modified_en:
        print("🚨 CHI TIẾT CÁC CHUỖI TIẾNG ANH ĐÃ BỊ THAY ĐỔI CẦN DỊCH LẠI:")
        for idx, item in enumerate(total_modified_en, 1):
            print(f"\n[{idx}] Bảng: {item['table']} | Key: {item['key']}")
            print(f"   - [EN CŨ] : {item['old_en']}")
            print(f"   - [EN MỚI]: {item['new_en']}")
            print(f"   - [VI HIỆN TẠI]: {item['current_vi']}")
            print("   👉 Đề xuất: Cần cập nhật lại bản dịch tiếng Việt theo nội dung [EN MỚI].")
    else:
        print("🎉 Tuyệt vời! Toàn bộ chuỗi tiếng Anh hiện tại khớp hoàn toàn 100% với file gốc của game.")

if __name__ == "__main__":
    detect_dev_updates()
