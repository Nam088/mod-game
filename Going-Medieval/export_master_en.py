import os
import json
import csv
import struct
import math

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

    # Preserve existing translations if any JSON file already has non-empty/different 'vi'
    existing_trans = {}
    if os.path.exists(trans_dir):
        for f in os.listdir(trans_dir):
            if f.endswith('.json'):
                p = os.path.join(trans_dir, f)
                try:
                    with open(p, 'r', encoding='utf-8') as fp:
                        entries = json.load(fp)
                        for e in entries:
                            if isinstance(e, dict) and e.get("vi") and e.get("vi") != e.get("en"):
                                existing_trans[e["key"]] = e["vi"]
                except Exception:
                    pass

    categories = {
        "tutorials_scenarios": [],
        "almanac_lore": [],
        "events_factions_trade": [],
        "settlers_skills_perks": [],
        "settlers_combat_mood_health": [],
        "buildings_construction": [],
        "furniture_rooms_decor": [],
        "items_weapons_armor": [],
        "items_resources_food": [],
        "ui_main_menu_settings": [],
        "ui_hud_controls": [],
        "ui_alerts_notifications": [],
        "ui_general": []
    }

    for item in master_list:
        k = item["key"]
        en = item["en"]
        kl = k.lower()
        
        vi_val = existing_trans.get(k, en)
        entry = {
            "key": k,
            "type": item.get("type", 0),
            "en": en,
            "vi": vi_val
        }
        
        if kl.startswith(('tutorial_', 'scenario_', 'scenarios_', 'tip_', 'gameplay_tip_')) or 'tutorial' in kl or 'scenario' in kl:
            categories["tutorials_scenarios"].append(entry)
        elif kl.startswith(('almanac_', 'almanacentry_', 'lore_', 'history_', 'chronicle_')) or 'almanac' in kl:
            categories["almanac_lore"].append(entry)
        elif kl.startswith(('event_', 'gameevent_', 'eventoption_', 'eventeffect_', 'eventreaction_', 'trading_', 'merchant_', 'faction_', 'caravan_', 'barter_', 'diplomacy_')) or 'faction' in kl or 'merchant' in kl or 'raid' in kl:
            categories["events_factions_trade"].append(entry)
        elif kl.startswith(('skill_', 'perk_', 'trait_', 'job_', 'role_', 'attribute_', 'profession_')) or 'skill' in kl or 'perk' in kl:
            categories["settlers_skills_perks"].append(entry)
        elif kl.startswith(('mood_', 'need_', 'thought_', 'religion_', 'alignment_', 'combat_', 'wound_', 'injury_', 'effect_', 'action_', 'health_')) or 'combat' in kl or 'mood' in kl or 'injury' in kl:
            categories["settlers_combat_mood_health"].append(entry)
        elif kl.startswith(('building_', 'structure_', 'construct_', 'roof_', 'wall_', 'floor_', 'door_', 'window_', 'stair_', 'stability_')) or 'building' in kl or 'construct' in kl:
            categories["buildings_construction"].append(entry)
        elif kl.startswith(('room_', 'roomtype_', 'furniture_', 'decoration_', 'table_', 'bed_', 'light_', 'torch_', 'zone_')) or 'room' in kl or 'furniture' in kl:
            categories["furniture_rooms_decor"].append(entry)
        elif kl.startswith(('weapon_', 'armor_', 'garment_', 'shield_', 'helmet_', 'equipment_')) or 'weapon' in kl or 'armor' in kl:
            categories["items_weapons_armor"].append(entry)
        elif kl.startswith(('resource_', 'food_', 'meal_', 'crop_', 'plant_', 'animal_', 'seed_', 'material_', 'quality_', 'item_')) or 'resource' in kl or 'plant' in kl or 'animal' in kl:
            categories["items_resources_food"].append(entry)
        elif kl.startswith(('menu_', 'mainmenu_', 'settings_', 'setting_', 'option_', 'options_', 'audio_', 'graphics_', 'key_', 'keycode_', 'ctrl_')) or 'menu' in kl or 'settings' in kl:
            categories["ui_main_menu_settings"].append(entry)
        elif kl.startswith(('hud_', 'btn_', 'button_', 'panel_', 'tab_', 'toggle_', 'slider_', 'speed_', 'view_', 'camera_')) or 'hud' in kl or 'button' in kl:
            categories["ui_hud_controls"].append(entry)
        elif kl.startswith(('alert_', 'warning_', 'notify_', 'notification_', 'msg_', 'message_', 'info_', 'popup_', 'dialog_')) or 'warning' in kl or 'alert' in kl:
            categories["ui_alerts_notifications"].append(entry)
        else:
            categories["ui_general"].append(entry)

    patch_list = []
    CHUNK_SIZE = 150

    for cat, items in categories.items():
        if len(items) <= CHUNK_SIZE:
            patch_list.append((cat, items))
        else:
            num_chunks = math.ceil(len(items) / CHUNK_SIZE)
            for i in range(num_chunks):
                sub_items = items[i*CHUNK_SIZE : (i+1)*CHUNK_SIZE]
                patch_list.append((f"{cat}_part{i+1}", sub_items))

    for f in os.listdir(trans_dir):
        if f.endswith('.json'):
            os.remove(os.path.join(trans_dir, f))

    for idx, (pname, pitems) in enumerate(patch_list, 1):
        fname = f"patch_{idx:02d}_{pname}.json"
        fpath = os.path.join(trans_dir, fname)
        with open(fpath, 'w', encoding='utf-8') as fp:
            json.dump(pitems, fp, ensure_ascii=False, indent=2)
        print(f"  Saved {fname}: {len(pitems)} keys")

if __name__ == '__main__':
    export_all()
