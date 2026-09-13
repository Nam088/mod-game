import os
import sys
import struct

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_SRC_DIR = os.path.join(PROJECT_ROOT, "tools", "fonts_source")
FONTS_BUILT_DIR = os.path.join(PROJECT_ROOT, "tools", "fonts_built")
os.makedirs(FONTS_BUILT_DIR, exist_ok=True)

def ttf_to_ufont(ttf_bytes: bytes) -> bytes:
    val0 = struct.pack("<I", len(ttf_bytes))
    tail = b"\x00\x00\x00\x00"
    return val0 + ttf_bytes + tail

def load_ttf(fname: str) -> bytes:
    fpath = os.path.join(FONTS_SRC_DIR, fname)
    with open(fpath, "rb") as fp:
        return fp.read()

def build_all_fonts():
    print("==================================================")
    print("   BUILDING 100% BE VIETNAM PRO FOR WHISKERWOOD   ")
    print("==================================================")

    bv_reg = ttf_to_ufont(load_ttf("BeVietnamPro-Regular.ttf"))
    bv_med = ttf_to_ufont(load_ttf("BeVietnamPro-Medium.ttf"))
    bv_semi = ttf_to_ufont(load_ttf("BeVietnamPro-SemiBold.ttf"))
    bv_bold = ttf_to_ufont(load_ttf("BeVietnamPro-Bold.ttf"))
    bv_extrabold = ttf_to_ufont(load_ttf("BeVietnamPro-ExtraBold.ttf"))
    
    bv_reg_it = ttf_to_ufont(load_ttf("BeVietnamPro-Italic.ttf"))
    bv_med_it = ttf_to_ufont(load_ttf("BeVietnamPro-MediumItalic.ttf"))
    bv_semi_it = ttf_to_ufont(load_ttf("BeVietnamPro-SemiBoldItalic.ttf"))
    bv_bold_it = ttf_to_ufont(load_ttf("BeVietnamPro-BoldItalic.ttf"))
    bv_extrabold_it = ttf_to_ufont(load_ttf("BeVietnamPro-ExtraBoldItalic.ttf"))

    # Map all in-game fonts to Be Vietnam Pro
    ufont_targets = {
        # LibreBaskerville -> Be Vietnam Pro Regular & Bold
        "LibreBaskerville/LibreBaskerville-Regular.ufont": bv_reg,
        "LibreBaskerville/LibreBaskerville-Bold.ufont": bv_bold,

        # Belleza -> Be Vietnam Pro Regular
        "Belleza/Belleza-Regular.ufont": bv_reg,

        # Germania_One -> Be Vietnam Pro Bold
        "Germania_One/GermaniaOne-Regular.ufont": bv_bold,

        # La_Belle_Aurore -> Be Vietnam Pro Regular (Thư từ siêu rõ, siêu êm mắt)
        "La_Belle_Aurore/LaBelleAurore-Regular.ufont": bv_reg,

        # Poppins -> Be Vietnam Pro across all 9 weights
        "Poppins/Poppins-Regular.ufont": bv_reg,
        "Poppins/Poppins-Medium.ufont": bv_med,
        "Poppins/Poppins-SemiBold.ufont": bv_semi,
        "Poppins/Poppins-Bold.ufont": bv_bold,
        "Poppins/Poppins-ExtraBold.ufont": bv_extrabold,
        "Poppins/Poppins-BoldItalic.ufont": bv_bold_it,
        "Poppins/Poppins-ExtraBoldItalic.ufont": bv_extrabold_it,
        "Poppins/Poppins-MediumItalic.ufont": bv_med_it,
        "Poppins/Poppins-SemiBoldItalic.ufont": bv_semi_it,
    }

    # Write built ufonts
    for rel_path, udata in ufont_targets.items():
        dest = os.path.join(FONTS_BUILT_DIR, rel_path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as fp:
            fp.write(udata)
        print(f"  [SAVED] {rel_path:<45}: {len(udata):,} bytes (Be Vietnam Pro)")

    print("\n✅ All 14 in-game fonts successfully mapped to BE VIETNAM PRO!")

if __name__ == "__main__":
    build_all_fonts()
