import os
import sys
import io
from fontTools.ttLib import TTFont

sys.stdout.reconfigure(encoding='utf-8')

vi_sample = "àáảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ"

def check_font(fpath):
    with open(fpath, "rb") as f:
        data = f.read()
    
    font_bytes = data[4:]
    tt = TTFont(io.BytesIO(font_bytes))
    cmap = tt.getBestCmap()
    missing = [c for c in vi_sample if ord(c) not in cmap]
    return len(missing) == 0, missing, len(cmap)

fonts_dir = r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Assets\Fonts"
for root, dirs, files in os.walk(fonts_dir):
    for f in files:
        if f.endswith(".ufont"):
            fpath = os.path.join(root, f)
            rel = os.path.relpath(fpath, fonts_dir)
            try:
                ok, missing, total = check_font(fpath)
                if ok:
                    print(f"[OK] {rel:<38} : Full Vietnamese support! (Glyphs: {total})")
                else:
                    print(f"[MISSING] {rel:<34} : Missing {len(missing)}/134 chars: {''.join(missing[:15])}... (Total Glyphs: {total})")
            except Exception as e:
                print(f"[ERR] {rel:<35} : {e}")
