#!/usr/bin/env python3
"""
Gộp toàn bộ các file patch đã được AI dịch (trong thư mục patches_for_ai/) trở lại strings.po tổng
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import polib

POT_PATH = os.path.join(BASE_DIR, 'strings_template.pot')
PO_PATH = os.path.join(BASE_DIR, 'strings.po')
PATCH_DIR = os.path.join(BASE_DIR, 'patches_for_ai')

def merge_all_patches():
    master_po = polib.pofile(PO_PATH) if os.path.exists(PO_PATH) else polib.pofile(POT_PATH)
    lookup = {e.msgctxt: e for e in master_po if e.msgctxt}

    total_merged = 0
    for filename in sorted(os.listdir(PATCH_DIR)):
        if filename.endswith('.po'):
            patch_file = os.path.join(PATCH_DIR, filename)
            p_po = polib.pofile(patch_file)
            print(f"[*] Đang gộp file: {filename} ({len(p_po):,} entries)...")
            
            for e in p_po:
                if e.msgctxt and e.msgctxt in lookup and e.msgstr and e.msgstr.strip() != "":
                    lookup[e.msgctxt].msgstr = e.msgstr
                    total_merged += 1

    master_po.save(PO_PATH)
    print(f"\n[✓] Hoàn tất! Đã gộp tổng cộng {total_merged:,} chuỗi đã dịch vào {PO_PATH}")

if __name__ == '__main__':
    merge_all_patches()
