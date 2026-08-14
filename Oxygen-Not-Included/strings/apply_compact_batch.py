#!/usr/bin/env python3
"""
Gộp file batch JSON đã dịch (ví dụ: batch_001.json, batch_001_vi.json) trực tiếp vào strings.po và chạy verify.
"""

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import polib

PO_PATH = os.path.join(BASE_DIR, 'strings.po')
POT_PATH = os.path.join(BASE_DIR, 'strings_template.pot')

def apply_batch_file(json_file_path):
    if not os.path.exists(json_file_path):
        print(f"[!] Không tìm thấy file: {json_file_path}")
        return 0

    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    po = polib.pofile(PO_PATH) if os.path.exists(PO_PATH) else polib.pofile(POT_PATH)
    lookup = {e.msgctxt: e for e in po if e.msgctxt}

    updated_count = 0
    for key, text in data.items():
        if key in lookup and text and text.strip():
            lookup[key].msgstr = text
            updated_count += 1

    po.save(PO_PATH)
    print(f"[✓] Đã cập nhật {updated_count:,} chuỗi từ '{os.path.basename(json_file_path)}' vào {PO_PATH}")
    return updated_count

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Sử dụng: python3 apply_compact_batch.py <đường_dẫn_batch_json>")
        sys.exit(1)

    for path in sys.argv[1:]:
        apply_batch_file(path)
