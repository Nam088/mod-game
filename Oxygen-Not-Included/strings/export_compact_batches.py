#!/usr/bin/env python3
"""
Chia nhỏ các Patch thành các batch siêu gọn nhẹ (khoảng 300 - 500 chuỗi / file) dạng Key-Value dictionary đơn giản:
{
  "STRINGS.ID": "English text"
}
Giúp AI dễ đọc, không bị quá tải context window.
"""

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import polib

POT_PATH = os.path.join(BASE_DIR, 'strings_template.pot')
BATCH_DIR = os.path.join(BASE_DIR, 'ai_batches_compact')
os.makedirs(BATCH_DIR, exist_ok=True)

CHUNK_SIZE = 300  # 300 câu 1 file vừa in 1 prompt của ChatGPT/Claude

def export_compact_chunks():
    pot = polib.pofile(POT_PATH)
    total_entries = len(pot)
    print(f"[*] Đang chia nhỏ {total_entries:,} chuỗi thành các file nhỏ gọn ({CHUNK_SIZE} câu/file)...")

    chunk_idx = 1
    current_chunk = {}

    for i, e in enumerate(pot):
        if not e.msgctxt:
            continue
        current_chunk[e.msgctxt] = e.msgid

        if len(current_chunk) >= CHUNK_SIZE or i == total_entries - 1:
            filename = f"batch_{chunk_idx:03d}.json"
            filepath = os.path.join(BATCH_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(current_chunk, f, ensure_ascii=False, indent=2)
            current_chunk = {}
            chunk_idx += 1

    print(f"[✓] Đã tạo xong {chunk_idx - 1} file batch nhỏ gọn tại thư mục: {BATCH_DIR}")

if __name__ == '__main__':
    export_compact_chunks()
