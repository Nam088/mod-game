import os
import json
import csv
import struct

def export_all():
    i2_bin_path = r'C:\Users\nam\.gemini\antigravity-ide\brain\2388ad27-36d6-43c6-856f-5ebe9484bfd1\scratch\i2languages.bin'
    dest_dir = os.path.dirname(os.path.abspath(__file__))
    trans_dir = os.path.join(dest_dir, 'translations')
    os.makedirs(trans_dir, exist_ok=True)

    with open(i2_bin_path, 'rb') as f:
        data = f.read()

    offset = 0x38
    total_terms = struct.unpack_from('<i', data, offset)[0]
    offset += 4
    print(f"Total master terms in I2Languages: {total_terms}")

    def read_str(offset):
        s_len = struct.unpack_from('<i', data, offset)[0]
        offset += 4
        if s_len == 0: return offset, ""
        s = data[offset:offset+s_len].decode('utf-8', errors='replace')
        offset += s_len
        if offset % 4 != 0: offset += (4 - (offset % 4))
        return offset, s

    master_list = []
    for i in range(total_terms):
        offset, term = read_str(offset)
        term_type = struct.unpack_from('<i', data, offset)[0]
        offset += 4
        
        lang_cnt = struct.unpack_from('<i', data, offset)[0]
        offset += 4
        langs = []
        for _ in range(lang_cnt):
            offset, s = read_str(offset)
            langs.append(s)
            
        offset, desc = read_str(offset)
        
        flags_cnt = struct.unpack_from('<i', data, offset)[0]
        offset += 4
        flags = data[offset:offset+flags_cnt]
        offset += flags_cnt
        if offset % 4 != 0: offset += (4 - (offset % 4))
        
        en_text = langs[0] if langs else ""
        master_list.append({
            "key": term,
            "type": term_type,
            "en": en_text
        })

    # Save master English
    with open(os.path.join(dest_dir, 'master_english.json'), 'w', encoding='utf-8') as f:
        json.dump(master_list, f, ensure_ascii=False, indent=2)

    with open(os.path.join(dest_dir, 'master_english.csv'), 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Key', 'Type', 'Desc', 'English'])
        for item in master_list:
            writer.writerow([item["key"], item["type"], "", item["en"]])

    print(f"Exported master_english.json and master_english.csv ({len(master_list)} terms).")

    # Categorize into 7 modules
    modules = {
        "01_ui_menu.json": [],
        "02_buildings_construction.json": [],
        "03_items_equipment.json": [],
        "04_settlers_jobs_combat.json": [],
        "05_events_trading_factions.json": [],
        "06_almanac_lore.json": [],
        "07_tutorials_scenarios.json": []
    }

    def categorize(key, en):
        k = key.lower()
        if k.startswith(('tutorial_', 'scenario_', 'scenarios_', 'tip_', 'gameplay_tip_')) or 'tutorial' in k or 'scenario' in k:
            return "07_tutorials_scenarios.json"
        if k.startswith(('almanac_', 'almanacentry_', 'lore_', 'history_', 'chronicle_')) or 'almanac' in k:
            return "06_almanac_lore.json"
        if k.startswith(('event_', 'gameevent_', 'eventoption_', 'eventeffect_', 'eventreaction_', 'trading_', 'merchant_', 'faction_', 'caravan_', 'barter_', 'diplomacy_')) or 'faction' in k or 'merchant' in k:
            return "05_events_trading_factions.json"
        if k.startswith(('building_', 'structure_', 'construct_', 'room_', 'roomtype_', 'roof_', 'wall_', 'floor_', 'door_', 'window_', 'stair_', 'furniture_', 'decoration_', 'stability_')) or 'building' in k or 'construct' in k or 'room' in k:
            return "02_buildings_construction.json"
        if k.startswith(('item_', 'equipment_', 'weapon_', 'armor_', 'garment_', 'shield_', 'resource_', 'food_', 'meal_', 'crop_', 'plant_', 'animal_', 'seed_', 'material_', 'quality_')) or 'weapon' in k or 'armor' in k or 'resource' in k:
            return "03_items_equipment.json"
        if k.startswith(('settler_', 'worker_', 'job_', 'role_', 'skill_', 'perk_', 'trait_', 'attribute_', 'stat_', 'mood_', 'need_', 'thought_', 'religion_', 'alignment_', 'combat_', 'wound_', 'injury_', 'effect_', 'action_')) or 'skill' in k or 'perk' in k or 'job' in k or 'combat' in k or 'mood' in k:
            return "04_settlers_jobs_combat.json"
        return "01_ui_menu.json"

    # Preserve existing translations if any JSON file already has non-empty/different 'vi'
    existing_trans = {}
    for mod_file in os.listdir(trans_dir):
        if mod_file.endswith('.json'):
            p = os.path.join(trans_dir, mod_file)
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    entries = json.load(f)
                    for e in entries:
                        if isinstance(e, dict) and e.get("vi") and e.get("vi") != e.get("en"):
                            existing_trans[e["key"]] = e["vi"]
            except Exception:
                pass

    for item in master_list:
        k = item["key"]
        en = item["en"]
        mod_name = categorize(k, en)
        vi_val = existing_trans.get(k, en)
        modules[mod_name].append({
            "key": k,
            "type": item["type"],
            "en": en,
            "vi": vi_val
        })

    for m, entries in modules.items():
        p = os.path.join(trans_dir, m)
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
        print(f"  Module {m}: {len(entries)} keys")

if __name__ == '__main__':
    export_all()
