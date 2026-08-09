import json

ats_en = json.load(open(r"D:\mod-game\Against-The-Storm\Localization_Patches\en.json", encoding="utf-8"))
tb_en = json.load(open(r"D:\mod-game\Timberborn\en.json", encoding="utf-8"))

print("=== VERIFICATION SAMPLE KEYS ===")

print("1. Against The Storm sample keys:")
ats_keys = list(ats_en.items())[:3]
for k, v in ats_keys:
    print(f"   [{k}] -> {v}")

print("\n2. Timberborn sample keys:")
tb_keys = list(tb_en.items())[:3]
for k, v in tb_keys:
    print(f"   [{k}] -> {v}")
