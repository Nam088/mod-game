import os
import json
import re
import sys
from collections import Counter

# Ensure UTF-8 stdout on Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def verify():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    trans_dir = os.path.join(base_dir, 'translations')
    
    total_keys = 0
    total_translated = 0
    total_errors = 0
    total_warnings = 0
    total_quality_warnings = 0

    print("=" * 65)
    print("🔍 GOING MEDIEVAL TRANSLATION VERIFICATION & PROGRESS REPORT")
    print("=" * 65)

    module_stats = []
    preserved_keys = {
        'DefaultFont', 'TitleFont', 'damage_per_second_ab',
        'general_symbol_Celsius', 'general_symbol_Fahrenheit', 'general_symbol_Kelvin',
        'general_minute_short', 'general_hour_short', 'general_day_short', 'general_year_short',
        'general_minute_short_duration', 'general_hour_short_duration',
        'general_day_short_duration', 'general_year_short_duration',
        'unit_suffix_percent', 'unit_suffix_per_hour', 'unit_suffix_times',
        'unit_suffix_per_second', 'unit_suffix_hour', 'unit_suffix_second',
        'unit_suffix_meter', 'unit_suffix_meters_per_second', 'general_required_fields_symbol', 'general_kg', 'general_cm',
        'combat_hit_unarmed_pattern', 'combat_hit_beast_pattern',
        'combat_block_pattern', 'health_wounding_pattern', 'health_healing_pattern',
        'health_carrying_pattern',
        'options_vsync', 'options_aa_FXAA', 'options_twitch', 'workshop_open',
        'update_entry_92', 'map_size_dev_100', 'map_size_dev_512',
        'effector_name_2x', 'effector_name_3x', 'effector_name_4x', 'game_name', 'DefaultFont', 'TitleFont',
        'damage_per_second_ab', 'general_ok', 'general_symbol_Celsius', 'general_symbol_Fahrenheit', 'general_symbol_Kelvin',
        'lastwords_default_2', 'building_info_foxy_statue', 'building names',
    }

    # English words that are intentionally retained in the Vietnamese build.
    allowed_english = {
        'steam', 'discord', 'directx', 'opengl', 'vulkan', 'xbox', 'epic',
        'klei', 'url', 'fps', 'cpu', 'gpu', 'rgb', 'ui', 'id', 'xp',
        'oak', 'brethren', 'restitutionist', 'almanac', 'settler', 'settlement',
        'draft', 'fruit', 'pie', 'pudding', 'cheese', 'fish', 'meat',
    }
    english_signal = {
        'the', 'and', 'or', 'of', 'on', 'for', 'with', 'from',
        'is', 'are', 'was', 'has', 'have', 'cannot', 'another', 'assigned',
        'preparing', 'ingredients', 'practicing', 'mixing', 'minting',
        'coins', 'broken', 'arm', 'bitten', 'face', 'deep', 'chest',
        'laceration', 'human', 'leather', 'production', 'select', 'dig',
    }
    wrapper_prefixes = (
        'Tên:',
        'Xuất thân và câu chuyện quá khứ của dân làng trước khi gia nhập khu định cư:',
    )
    generic_resource_text = 'Tài nguyên quan trọng dùng cho việc sinh tồn, nấu nướng hoặc chế tác tại khu định cư.'

    for file_name in sorted(os.listdir(trans_dir)):
        if not file_name.endswith('.json'):
            continue
        
        file_path = os.path.join(trans_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            entries = json.load(f)

        mod_keys = len(entries)
        mod_translated = 0
        mod_errors = 0
        mod_warnings = 0
        mod_quality = 0

        for idx, item in enumerate(entries):
            k = item.get("key", "")
            en = item.get("en", "")
            vi = item.get("vi", "")

            # Some technical, branded and composition strings must remain unchanged.
            is_preserved = (
                k.startswith(('dev_', 'keycode_', 'menu_language_'))
                or k in preserved_keys
            )
            is_translated = is_preserved or bool(vi and vi.strip() != en.strip())
            if is_translated:
                mod_translated += 1

            # Check 1: numbered/named placeholders and gender tokens.
            token_pattern = r'(?:\{[^{}]+\}|(?:#\d+)?\[[A-Za-z]+/[A-Za-z]+\])'
            en_placeholders = sorted(re.findall(token_pattern, en))
            vi_placeholders = sorted(re.findall(token_pattern, vi))
            if en_placeholders != vi_placeholders:
                print(f"❌ [PLACEHOLDER ERROR] {file_name} -> Key: '{k}'")
                print(f"   EN: {en}")
                print(f"   VI: {vi}")
                print(f"   Expected: {en_placeholders}, Got: {vi_placeholders}")
                mod_errors += 1

            # Check 2: RichText tags and angle-bracket placeholders.
            en_tags = sorted(re.findall(r'<[^>]+>', en))
            vi_tags = sorted(re.findall(r'<[^>]+>', vi))
            if en_tags != vi_tags:
                print(f"❌ [TAG ERROR] {file_name} -> Key: '{k}'")
                print(f"   EN: {en}")
                print(f"   VI: {vi}")
                print(f"   Expected tags: {en_tags}, Got: {vi_tags}")
                mod_errors += 1

            # Check 3: real and literal escaped newlines.
            if en.count('\n') != vi.count('\n') or en.count('\\n') != vi.count('\\n'):
                print(f"❌ [NEWLINE ERROR] {file_name} -> Key: '{k}'")
                print(f"   EN newlines: {en.count(chr(10))}, VI newlines: {vi.count(chr(10))}")
                mod_errors += 1

            # Check 4: UI Length Guard (> 2.0x length of EN string for short UI elements)
            if (
                not is_preserved
                and len(en) >= 10
                and len(en) < 30
                and len(vi) > max(30, len(en) * 2.2)
                and is_translated
            ):
                print(f"⚠️  [UI LENGTH OVERFLOW] {file_name} -> Key: '{k}'")
                print(f"   EN ({len(en)}): {en}")
                print(f"   VI ({len(vi)}): {vi}")
                mod_warnings += 1

            # Quality checks: these do not fail the build, but expose incomplete or
            # placeholder translations that the old verifier counted as complete.
            if not is_preserved and vi.strip().startswith(wrapper_prefixes):
                print(f"⚠️  [WRAPPER WARNING] {file_name} -> Key: '{k}'")
                print(f"   VI: {vi}")
                mod_quality += 1

            if not is_preserved and vi.strip() == generic_resource_text and en.strip() != generic_resource_text:
                print(f"⚠️  [GENERIC TRANSLATION WARNING] {file_name} -> Key: '{k}'")
                print(f"   EN: {en}")
                mod_quality += 1

            if not is_preserved and vi.strip() and vi.strip() != en.strip():
                clean_vi = re.sub(r'<[^>]+>', '', vi)
                words = [w.lower() for w in re.findall(r'[^\W\d_]+', clean_vi, flags=re.UNICODE)]
                residual = sorted({w for w in words if w in english_signal and w not in allowed_english})
                if residual:
                    print(f"⚠️  [ENGLISH RESIDUAL WARNING] {file_name} -> Key: '{k}'")
                    print(f"   ENGLISH TOKENS: {', '.join(residual)}")
                    print(f"   VI: {vi}")
                    mod_quality += 1

        pct = (mod_translated / mod_keys * 100) if mod_keys > 0 else 0
        module_stats.append((file_name, mod_keys, mod_translated, pct, mod_errors, mod_warnings, mod_quality))
        total_keys += mod_keys
        total_translated += mod_translated
        total_errors += mod_errors
        total_warnings += mod_warnings
        total_quality_warnings += mod_quality

    print("\n📊 SUMMARY BY MODULE:")
    print("-" * 65)
    print(f"{'Module Name':<35} | {'Total':<6} | {'Done':<6} | {'Progress':<8} | {'Quality':<7}")
    print("-" * 65)
    for name, m_tot, m_done, m_pct, errs, warns, quality in module_stats:
        status_symbol = "🟢" if m_pct >= 99.9 else ("🟡" if m_pct > 0 else "⚪")
        print(f"{status_symbol} {name:<33} | {m_tot:<6} | {m_done:<6} | {m_pct:>6.1f}% | Q:{quality}")
    print("-" * 65)
    overall_pct = (total_translated / total_keys * 100) if total_keys > 0 else 0
    print(f"🎯 OVERALL PROGRESS: {total_translated} / {total_keys} keys ({overall_pct:.2f}%)")
    print(f"❌ Total Errors: {total_errors}")
    print(f"⚠️  Total Warnings: {total_warnings}")
    print(f"📝 Quality Warnings: {total_quality_warnings}")
    print("=" * 65)

    return total_errors == 0

if __name__ == '__main__':
    verify()
