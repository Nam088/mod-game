import struct

with open(r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_En.uexp", "rb") as f:
    orig = f.read()

with open(r"D:\code\mod-game\Whiskerwood\build\Whiskerwood\Content\Data\TextDB\Loc_En.uexp", "rb") as f:
    patched = f.read()

print(f"Orig size: {len(orig)}, Patched size: {len(patched)}")

# Find first difference
min_len = min(len(orig), len(patched))
for i in range(min_len):
    if orig[i] != patched[i]:
        print(f"First diff at offset 0x{i:x} ({i}): orig=0x{orig[i]:02x}, patched=0x{patched[i]:02x}")
        print("Orig surrounding:", orig[max(0, i-16):min(len(orig), i+32)].hex())
        print("Patched surrounding:", patched[max(0, i-16):min(len(patched), i+32)].hex())
        break
else:
    print("Files are identical up to min_len!")
