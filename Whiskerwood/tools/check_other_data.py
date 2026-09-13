import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

data_dir = r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data"

uasset_files = []
for root, dirs, files in os.walk(data_dir):
    for f in files:
        if f.endswith(".uasset") and "TextDB" not in root:
            uasset_files.append(os.path.join(root, f))

print(f"Found {len(uasset_files)} non-TextDB uasset files in Content/Data.")

# Sample check some files to see if they contain TextDB key references or raw strings
for fpath in uasset_files[:10]:
    rel = os.path.relpath(fpath, data_dir)
    print(f" - {rel}")
