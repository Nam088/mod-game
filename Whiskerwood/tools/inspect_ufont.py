import struct
import io
from fontTools.ttLib import TTFont

font_path = r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Assets\Fonts\Poppins\Poppins-Regular.ufont"

with open(font_path, "rb") as f:
    data = f.read()

print("Size:", len(data))
print("First 32 bytes:", data[:32].hex())

# Let's see if we find TTF/OTF magic: 0x00010000 ('\x00\x01\x00\x00') or 'OTTO' or 'true' or 'typ1'
for magic in [b'\x00\x01\x00\x00', b'OTTO', b'true', b'typ1']:
    idx = data.find(magic)
    if idx != -1:
        print(f"Found magic {magic} at offset {idx} (0x{idx:x})")
        # Try loading from this offset
        try:
            tt = TTFont(io.BytesIO(data[idx:]))
            cmap = tt.getBestCmap()
            print(f"  Successfully loaded TTFont from offset {idx}! Glyphs in cmap: {len(cmap)}")
        except Exception as e:
            print(f"  Failed loading from offset {idx}: {e}")
