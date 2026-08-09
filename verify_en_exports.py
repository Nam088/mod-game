import json

ats_en = json.load(open(r"D:\mod-game\Against-The-Storm\Localization_Patches\en.json", encoding="utf-8"))
tb_en = json.load(open(r"D:\mod-game\Timberborn\en.json", encoding="utf-8"))

print("=== VERIFICATION RESULTS ===")
print(f"1. Against The Storm master en.json: {len(ats_en)} keys")
print(f"   Sample key (Building_Hearth_Name): {ats_en.get('Building_Hearth_Name')}")

print(f"\n2. Timberborn master en.json: {len(tb_en)} keys")
print(f"   Sample key (Building.LogPile.DisplayName): {tb_en.get('Building.LogPile.DisplayName')}")
