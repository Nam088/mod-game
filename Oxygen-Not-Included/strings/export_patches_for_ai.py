#!/usr/bin/env python3
"""
Tách toàn bộ 21.330 chuỗi thành 6 file PO/JSON tương ứng 6 Patch kèm prompt hướng dẫn chuẩn cho AI
"""

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import polib

POT_PATH = os.path.join(BASE_DIR, 'strings_template.pot')
PATCH_DIR = os.path.join(BASE_DIR, 'patches_for_ai')
os.makedirs(PATCH_DIR, exist_ok=True)

PATCH_CONFIG = {
    1: {
        'name': 'patch_1_ui_and_inputs',
        'title': 'Patch 1: UI & Giao diện cốt lõi (Menu, Settings, Overlays, Input)',
        'prefixes': ['STRINGS.UI', 'STRINGS.INPUT', 'STRINGS.INPUT_BINDINGS', 'STRINGS.SEARCH_TERMS']
    },
    2: {
        'name': 'patch_2_buildings_and_machines',
        'title': 'Patch 2: Công trình & Máy móc (Buildings, Power, Plumbing, Ventilation)',
        'prefixes': ['STRINGS.BUILDINGS', 'STRINGS.BUILDING']
    },
    3: {
        'name': 'patch_3_duplicants_and_skills',
        'title': 'Patch 3: Dàn Đệ, Thuộc tính, Kỹ năng & Bệnh tật (Duplicants, Equipment, Roles)',
        'prefixes': ['STRINGS.DUPLICANTS', 'STRINGS.EQUIPMENT', 'STRINGS.NAMEGEN']
    },
    4: {
        'name': 'patch_4_items_research_rooms',
        'title': 'Patch 4: Vật phẩm, Món ăn, Nghiên cứu & Phòng ốc (Items, Elements, Research, Rooms)',
        'prefixes': ['STRINGS.ITEMS', 'STRINGS.ELEMENTS', 'STRINGS.RESEARCH', 'STRINGS.ROOMS', 'STRINGS.BLUEPRINTS', 'STRINGS.STICKERNAMES']
    },
    5: {
        'name': 'patch_5_creatures_and_worlds',
        'title': 'Patch 5: Sinh vật, Thế giới, Bản đồ & Thành tựu (Creatures, Worlds, Achievements)',
        'prefixes': ['STRINGS.CREATURES', 'STRINGS.ROBOTS', 'STRINGS.WORLDS', 'STRINGS.SUBWORLDS', 'STRINGS.CLUSTER_NAMES', 'STRINGS.WORLD_TRAITS', 'STRINGS.COLONY_ACHIEVEMENTS', 'STRINGS.GAMEPLAY_EVENTS']
    },
    6: {
        'name': 'patch_6_codex_and_lore',
        'title': 'Patch 6: Bách khoa toàn thư Codex & Cốt truyện Gravitas (Codex, Lore, Videos)',
        'prefixes': ['STRINGS.CODEX', 'STRINGS.LORE', 'STRINGS.VIDEOS', 'STRINGS.MISC']
    }
}

def export_patches():
    pot = polib.pofile(POT_PATH)
    print(f"[*] Đang xuất 6 Patch từ {POT_PATH}...")

    summary = {}
    for p_id, cfg in PATCH_CONFIG.items():
        po_patch = polib.POFile()
        po_patch.metadata = {
            'Project-Id-Version': f'Oxygen Not Included Vietnamese - {cfg["title"]}',
            'Language': 'vi',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=UTF-8',
            'Content-Transfer-Encoding': '8bit',
            'Plural-Forms': 'nplurals=1; plural=0;',
            'Application': 'Oxygen Not Included',
            'POT Version': '2.0'
        }

        json_data = []
        for e in pot:
            if e.msgctxt and any(e.msgctxt.startswith(p) for p in cfg['prefixes']):
                new_entry = polib.POEntry(
                    msgid=e.msgid,
                    msgstr='',
                    msgctxt=e.msgctxt,
                    comment=e.comment
                )
                po_patch.append(new_entry)
                json_data.append({
                    'msgctxt': e.msgctxt,
                    'msgid': e.msgid,
                    'msgstr': ''
                })

        po_file_path = os.path.join(PATCH_DIR, f"{cfg['name']}.po")
        json_file_path = os.path.join(PATCH_DIR, f"{cfg['name']}.json")
        
        po_patch.save(po_file_path)
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)

        summary[cfg['name']] = len(po_patch)
        print(f"[✓] {cfg['title']} -> {len(po_patch):,} chuỗi -> Đã xuất .po và .json")

    print("\n[+] Hoàn tất xuất toàn bộ 6 Patch!")
    return summary

if __name__ == '__main__':
    export_patches()
