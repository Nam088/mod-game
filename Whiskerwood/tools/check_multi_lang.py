import struct
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

textdb_dir = r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB"

def get_translations_for_key(target_key):
    results = {}
    for file in sorted(os.listdir(textdb_dir)):
        if file.endswith(".uasset") and not file.startswith("Loc_Dev") and not file.startswith("Loc_Root"):
            lang = file[4:-7]
            uasset_path = os.path.join(textdb_dir, file)
            uexp_path = os.path.join(textdb_dir, file.replace(".uasset", ".uexp"))
            
            with open(uasset_path, "rb") as f:
                uasset = f.read()
            with open(uexp_path, "rb") as f:
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
            pos = 14
            for r in range(row_count):
                name_idx, name_inst = struct.unpack_from("<ii", uexp, pos)
                pos += 8
                flags = uexp[pos:pos+2]
                pos += 2
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
                
                key_name = names[name_idx] if 0 <= name_idx < len(names) else ""
                if key_name == target_key:
                    results[lang] = text
                    break
    return results

keys_to_check = [
    "story.common.intro1", # Dear Acting Tail,
    "story.common.intro2", # Dear Tail,
    "nautical.enemy.claws", # Claws
    "building.conveyor",   # Whisker Conveyor
    "claws.trustLevel.0",
    "story.quest.respect.body", # We Claws are a humble race...
]

for k in keys_to_check:
    print(f"\n=== KEY: {k} ===")
    res = get_translations_for_key(k)
    for lang, val in res.items():
        if lang in ["En", "Fr", "De", "Zh", "Ja", "Ru", "Es"]:
            print(f"  {lang:<5}: {val[:80]}")
