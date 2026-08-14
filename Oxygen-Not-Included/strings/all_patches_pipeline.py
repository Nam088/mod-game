#!/usr/bin/env python3
"""
Oxygen Not Included (ONI) - Master Translation Pipeline (All Patches Framework)
Framework phân chia 6 Patch bài bản, tích hợp từ điển, kiểm soát cú pháp và verify tự động.
"""

import os
import sys
import re
import argparse

# Setup path cho polib
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import polib

POT_PATH = os.path.join(BASE_DIR, 'strings_template.pot')
PO_PATH = os.path.join(BASE_DIR, 'strings.po')

# Cấu hình phân loại 6 Patch
PATCH_CONFIG = {
    1: {
        'name': 'Patch 1: UI & Giao diện cốt lõi (Menu, Settings, Overlays, Input)',
        'prefixes': ['STRINGS.UI', 'STRINGS.INPUT', 'STRINGS.INPUT_BINDINGS', 'STRINGS.SEARCH_TERMS']
    },
    2: {
        'name': 'Patch 2: Công trình & Máy móc (Buildings, Power, Plumbing, Ventilation)',
        'prefixes': ['STRINGS.BUILDINGS', 'STRINGS.BUILDING']
    },
    3: {
        'name': 'Patch 3: Dàn Đệ, Thuộc tính, Kỹ năng & Bệnh tật (Duplicants, Equipment, Roles)',
        'prefixes': ['STRINGS.DUPLICANTS', 'STRINGS.EQUIPMENT', 'STRINGS.NAMEGEN']
    },
    4: {
        'name': 'Patch 4: Vật phẩm, Món ăn, Nghiên cứu & Phòng ốc (Items, Elements, Research, Rooms)',
        'prefixes': ['STRINGS.ITEMS', 'STRINGS.ELEMENTS', 'STRINGS.RESEARCH', 'STRINGS.ROOMS', 'STRINGS.BLUEPRINTS', 'STRINGS.STICKERNAMES']
    },
    5: {
        'name': 'Patch 5: Sinh vật, Thế giới, Bản đồ & Thành tựu (Creatures, Worlds, Achievements)',
        'prefixes': ['STRINGS.CREATURES', 'STRINGS.ROBOTS', 'STRINGS.WORLDS', 'STRINGS.SUBWORLDS', 'STRINGS.CLUSTER_NAMES', 'STRINGS.WORLD_TRAITS', 'STRINGS.COLONY_ACHIEVEMENTS', 'STRINGS.GAMEPLAY_EVENTS']
    },
    6: {
        'name': 'Patch 6: Bách khoa toàn thư Codex & Cốt truyện Gravitas (Codex, Lore, Videos)',
        'prefixes': ['STRINGS.CODEX', 'STRINGS.LORE', 'STRINGS.VIDEOS', 'STRINGS.MISC']
    }
}


class TranslationPipeline:
    def __init__(self, po_file=PO_PATH, pot_file=POT_PATH):
        self.po_file = po_file
        self.pot_file = pot_file
        self.po = polib.pofile(po_file) if os.path.exists(po_file) else polib.pofile(pot_file)

    def get_patch_entries(self, patch_num):
        """Lọc danh sách các chuỗi thuộc Patch chỉ định"""
        prefixes = PATCH_CONFIG[patch_num]['prefixes']
        return [
            e for e in self.po 
            if e.msgctxt and any(e.msgctxt.startswith(p) for p in prefixes)
        ]

    def print_patch_statistics(self):
        """In thống kê tổng quan tiến độ của cả 6 Patch"""
        print("\n" + "=" * 70)
        print("        TIẾN ĐỘ & PHÂN PHỐI CHUỖI TOÀN BỘ 6 PATCH (ONI)")
        print("=" * 70)
        total_all = len(self.po)
        translated_all = sum(1 for e in self.po if e.msgstr and e.msgstr.strip() != "")

        for patch_id, cfg in PATCH_CONFIG.items():
            entries = self.get_patch_entries(patch_id)
            trans_count = sum(1 for e in entries if e.msgstr and e.msgstr.strip() != "")
            total_patch = len(entries)
            pct = (trans_count / total_patch * 100) if total_patch > 0 else 0
            print(f"[{patch_id}] {cfg['name']}")
            print(f"    -> Đã dịch: {trans_count:,} / {total_patch:,} chuỗi ({pct:.1f}%)\n")

        print("-" * 70)
        total_pct = (translated_all / total_all * 100) if total_all > 0 else 0
        print(f"TỔNG CỘNG TOÀN BỘ GAME: {translated_all:,} / {total_all:,} chuỗi ({total_pct:.1f}%)")
        print("=" * 70 + "\n")

    def run_patch_pipeline(self, patch_num):
        """Khung chạy xử lý dịch thuật cho từng Patch"""
        print(f"[*] Bắt đầu xử lý {PATCH_CONFIG[patch_num]['name']}...")
        entries = self.get_patch_entries(patch_num)
        print(f"[*] Tổng số chuỗi trong Patch {patch_num}: {len(entries):,}")
        
        # Placeholder để gắn logic dịch thuật chi tiết cho từng Patch
        # ...
        
        self.po.save(self.po_file)
        print(f"[✓] Đã lưu kết quả Patch {patch_num} vào {self.po_file}")


def main():
    parser = argparse.ArgumentParser(description="Oxygen Not Included - Master All-Patches Translation Script")
    parser.add_argument("--stats", action="store_true", help="Hiển thị thống kê số lượng chuỗi và tiến độ của cả 6 Patch")
    parser.add_argument("--patch", type=int, choices=[1, 2, 3, 4, 5, 6], help="Chạy pipeline cho một Patch cụ thể (1-6)")
    parser.add_argument("--all", action="store_true", help="Chạy toàn bộ 6 Patch")
    args = parser.parse_args()

    pipeline = TranslationPipeline()

    if args.patch:
        pipeline.run_patch_pipeline(args.patch)
    elif args.all:
        for p in range(1, 7):
            pipeline.run_patch_pipeline(p)
    else:
        pipeline.print_patch_statistics()


if __name__ == '__main__':
    main()
