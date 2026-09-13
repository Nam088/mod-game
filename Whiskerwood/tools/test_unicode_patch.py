import struct
import json
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
orig_uasset = os.path.join(project_root, "extracted", "Whiskerwood", "Content", "Data", "TextDB", "Loc_En.uasset")
orig_uexp = os.path.join(project_root, "extracted", "Whiskerwood", "Content", "Data", "TextDB", "Loc_En.uexp")
master_json = os.path.join(project_root, "translations", "Whiskerwood_Loc_En_Master.json")

with open(master_json, "r", encoding="utf-8") as f:
    entries = json.load(f)

# Put some Vietnamese sample translations
entries[0]["target_vi"] = "Lối đi & Đường lát đá"
entries[1]["target_vi"] = "Nhiệt lượng & Tiện ích"
entries[2]["target_vi"] = "Nhà ở & Nơi trú ẩn"
entries[3]["target_vi"] = "Dịch vụ & Tiện ích công cộng"
entries[4]["target_vi"] = "Nghiên cứu & Phát minh"

from uasset_patcher import patch_loc_en

test_uasset = os.path.join(project_root, "scratch", "Loc_En.uasset")
test_uexp = os.path.join(project_root, "scratch", "Loc_En.uexp")

patch_loc_en(entries, orig_uasset, orig_uexp, test_uasset, test_uexp)

# Read back with parser
with open(test_uasset, "rb") as f:
    uasset = f.read()
with open(test_uexp, "rb") as f:
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
print(f"Read back {row_count} rows from test file:")
pos = 14
for r in range(5):
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
    print(f"Row {r}: key='{names[name_idx]}' (s_len={s_len}) -> '{text}'")
