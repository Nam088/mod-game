import struct
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
UASSET_PATH = os.path.join(PROJECT_ROOT, "extracted", "Whiskerwood", "Content", "Data", "TextDB", "Loc_En.uasset")
UEXP_PATH = os.path.join(PROJECT_ROOT, "extracted", "Whiskerwood", "Content", "Data", "TextDB", "Loc_En.uexp")
TRANS_DIR = os.path.join(PROJECT_ROOT, "translations")

os.makedirs(TRANS_DIR, exist_ok=True)

def parse_loc_en():
    with open(UASSET_PATH, "rb") as f:
        uasset = f.read()
    with open(UEXP_PATH, "rb") as f:
        uexp = f.read()

    name_count, name_offset = struct.unpack_from("<ii", uasset, 85)
    names = []
    pos = name_offset
    for i in range(name_count):
        s_len, = struct.unpack_from("<i", uasset, pos)
        pos += 4
        if s_len > 0:
            s = uasset[pos:pos+s_len-1].decode("utf-8", errors="replace")
            pos += s_len
        elif s_len < 0:
            s_len = -s_len
            s = uasset[pos:pos+s_len*2-2].decode("utf-16le", errors="replace")
            pos += s_len * 2
        else:
            s = ""
        non_case_hash, case_hash = struct.unpack_from("<HH", uasset, pos)
        pos += 4
        names.append(s)

    row_count, = struct.unpack_from("<i", uexp, 10)
    entries = []
    pos = 14
    for r in range(row_count):
        name_idx, name_inst = struct.unpack_from("<ii", uexp, pos)
        pos += 8
        key_name = names[name_idx] if 0 <= name_idx < len(names) else f"Unknown_{name_idx}"
        flags = uexp[pos:pos+2]
        pos += 2
        text_len_offset = pos
        s_len, = struct.unpack_from("<i", uexp, pos)
        pos += 4
        if s_len > 0:
            text = uexp[pos:pos+s_len-1].decode("utf-8", errors="replace")
            pos += s_len
        elif s_len < 0:
            s_len = -s_len
            text = uexp[pos:pos+s_len*2-2].decode("utf-16le", errors="replace")
            pos += s_len * 2
        else:
            text = ""
        
        prefix = key_name.split('.')[0] if '.' in key_name else "other"
        
        # Categorization
        if prefix in ['menu', 'settings', 'toolbar', 'tooltip', 'action', 'error', 'notif', 'hoverNotif', 'pause', 'stats', 'credit', 'save', 'keybinding', 'cheat', 'aa']:
            category = "01_Core_UI_Menus"
        elif prefix in ['building', 'logistics', 'aim', 'slot', 'problem', 'indicator']:
            category = "02_Buildings_Logistics"
        elif prefix in ['resource', 'unlock', 'policy', 'tech', 'industry', 'crop', 'meal', 'drink']:
            category = "03_Resources_Items_Tech"
        elif prefix in ['whiskerActivity', 'thought', 'trait', 'education', 'guild', 'morale', 'happiness', 'job']:
            category = "04_Mice_Traits_Thoughts"
        elif prefix in ['nautical', 'embark', 'worldeffect', 'dockedship', 'ferrydock', 'weather', 'season', 'ship', 'colonyname']:
            category = "05_Nautical_Exploration_World"
        else:
            category = "06_Quests_Events_Story"
            
        entries.append({
            "id": r,
            "key": key_name,
            "category": category,
            "source_en": text,
            "target_vi": "",
            "context": f"{prefix} | Row {r}",
            "offset": text_len_offset,
            "length": s_len
        })
        
    return entries

def main():
    entries = parse_loc_en()
    print(f"Extracted total {len(entries)} translation strings from Whiskerwood!")
    
    # Save master file
    master_file = os.path.join(TRANS_DIR, "Whiskerwood_Loc_En_Master.json")
    with open(master_file, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"Saved master file: {master_file}")
    
    # Group by category and save module files
    categories = {}
    for e in entries:
        cat = e["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(e)
        
    for cat, cat_entries in sorted(categories.items()):
        cat_file = os.path.join(TRANS_DIR, f"{cat}.json")
        with open(cat_file, "w", encoding="utf-8") as f:
            json.dump(cat_entries, f, ensure_ascii=False, indent=2)
        print(f"  - {cat}.json: {len(cat_entries):4d} strings")

if __name__ == "__main__":
    main()
