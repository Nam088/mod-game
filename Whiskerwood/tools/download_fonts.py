import urllib.request
import os
import io
from fontTools.ttLib import TTFont

sys_fonts_dir = r"D:\code\mod-game\Whiskerwood\tools\fonts_source"
os.makedirs(sys_fonts_dir, exist_ok=True)

urls = {
    "Poppins-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf",
    "Poppins-Bold.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Bold.ttf",
    "Poppins-Medium.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Medium.ttf",
    "Poppins-SemiBold.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-SemiBold.ttf",
    "Poppins-ExtraBold.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-ExtraBold.ttf",
    "Poppins-BoldItalic.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-BoldItalic.ttf",
    "Poppins-MediumItalic.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-MediumItalic.ttf",
    "Poppins-SemiBoldItalic.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-SemiBoldItalic.ttf",
    "Poppins-ExtraBoldItalic.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-ExtraBoldItalic.ttf",
    "LibreBaskerville-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/librebaskerville/LibreBaskerville-Regular.ttf",
    "LibreBaskerville-Bold.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/librebaskerville/LibreBaskerville-Bold.ttf",
}

vi_sample = "àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵ"

for name, url in urls.items():
    dest = os.path.join(sys_fonts_dir, name)
    if not os.path.exists(dest):
        print(f"Downloading {name}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as resp, open(dest, 'wb') as out:
                out.write(resp.read())
        except Exception as e:
            print(f"  Failed to download {name}: {e}")
            continue
            
    # Check Vietnamese coverage
    try:
        tt = TTFont(dest)
        cmap = tt.getBestCmap()
        missing = [c for c in vi_sample if ord(c) not in cmap]
        if not missing:
            print(f"  [OK] {name}: Full Vietnamese glyph support ({len(cmap)} total glyphs)")
        else:
            print(f"  [MISSING] {name}: Missing {len(missing)} chars")
    except Exception as e:
        print(f"  Error checking {name}: {e}")
