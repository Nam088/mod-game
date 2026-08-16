import os
import sys
import shutil
import subprocess
import json

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(CURRENT_DIR, "tools")
BUILD_DIR = os.path.join(CURRENT_DIR, "build")
DIST_DIR = os.path.join(CURRENT_DIR, "dist")
TRANS_DIR = os.path.join(CURRENT_DIR, "translations")
EXTRACTED_DIR = os.path.join(CURRENT_DIR, "extracted")

REPAK_EXE = os.path.join(TOOLS_DIR, "repak.exe")
GAME_PAKS_DIR = r"C:\Users\nam\Downloads\Compressed\Manor-Lords-AnkerGames_2\Manor Lords\ManorLords\Content\Paks"
MODS_SUBDIR = os.path.join(GAME_PAKS_DIR, "~mods")

def ensure_fonts_downloaded():
    import urllib.request
    import re
    
    custom_fonts_dir = os.path.join(CURRENT_DIR, "custom_fonts")
    os.makedirs(custom_fonts_dir, exist_ok=True)
    
    alegreya_upright = os.path.join(custom_fonts_dir, "Alegreya-SemiBold.ttf")
    
    # Chỉ tải font đứng thẳng, KHÔNG tải italic
    if not os.path.exists(alegreya_upright):
        print("[*] Đang tự động tải font Alegreya SemiBold (đứng thẳng) từ Google Fonts...")
        url = "https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,600&subset=vietnamese"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req) as resp:
                css = resp.read().decode('utf-8')
            font_urls = re.findall(r'src:\s*url\((https://fonts\.gstatic\.com/[^)]+)\)', css)
            if font_urls:
                with urllib.request.urlopen(font_urls[0]) as fresp, open(alegreya_upright, 'wb') as fout:
                    fout.write(fresp.read())
                print("[✓] Đã tải font Alegreya SemiBold đứng thẳng thành công!")
        except Exception as e:
            print(f"[!] Cảnh báo tải font: {e}")

def inject_custom_fonts():
    ensure_fonts_downloaded()

    custom_fonts_dir = os.path.join(CURRENT_DIR, "custom_fonts")
    alegreya_upright = os.path.join(custom_fonts_dir, "Alegreya-SemiBold.ttf")

    if not os.path.exists(alegreya_upright):
        alegreya_upright = os.path.join(custom_fonts_dir, "Alegreya-Bold.ttf")

    # === CLEAN BUILD FONT DIRS trước khi inject để xóa file stale từ lần chạy trước ===
    loc1_build = os.path.join(BUILD_DIR, "ManorLords", "Content", "ManorLords", "Fonts")
    loc2_build = os.path.join(BUILD_DIR, "ManorLords", "Content", "UWG", "fonts")
    for d in [loc1_build, loc2_build]:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)
    print("[*] Cleaned font build directories...")
    loc1_extract = os.path.join(EXTRACTED_DIR, "ManorLords", "Content", "ManorLords", "Fonts")
    if os.path.exists(alegreya_upright):
        shutil.copy2(alegreya_upright, os.path.join(loc1_build, "Mikadan_Regular.ufont"))
        shutil.copy2(alegreya_upright, os.path.join(loc1_build, "Favarotta-Heavy.ufont"))
    for f in ["Mikadan_Regular.uasset", "Mikadan_Regular.uexp", "Favarotta-Heavy.uasset", "Favarotta-Heavy.uexp"]:
        src = os.path.join(loc1_extract, f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(loc1_build, f))

    # 2. Location 2: ManorLords/Content/UWG/fonts/ (100% Font Đứng Thẳng)
    loc2_build = os.path.join(BUILD_DIR, "ManorLords", "Content", "UWG", "fonts")
    loc2_extract = os.path.join(EXTRACTED_DIR, "ManorLords", "Content", "UWG", "fonts")
    os.makedirs(loc2_build, exist_ok=True)
    if os.path.exists(alegreya_upright):
        shutil.copy2(alegreya_upright, os.path.join(loc2_build, "Mikadan_Regular.ufont"))
        shutil.copy2(alegreya_upright, os.path.join(loc2_build, "favarotta_italic.ufont"))  # override bằng bản đứng
    for f in [
        "Mikadan_Regular.uasset", "Mikadan_Regular.uexp",
        "Mikadan_Regular_Font.uasset", "Mikadan_Regular_Font.uexp",
        # KHÔNG copy favarotta_italic.uasset/uexp gốc (có Italic=true metadata -> gây nghiêng)
        "CombinedFont_Mikadan.uasset", "CombinedFont_Mikadan.uexp",
        "CombinedFont_SemiBold.uasset", "CombinedFont_SemiBold.uexp",
        "CombinedFont_SemiBold1.uasset", "CombinedFont_SemiBold1.uexp"
    ]:
        src = os.path.join(loc2_extract, f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(loc2_build, f))

    # 3. SairaCondensed: thay tất cả bản nghiêng bằng bản đứng thẳng
    saira_medium = os.path.join(loc2_extract, "SairaCondensed-Medium.ufont")
    saira_semibold = os.path.join(loc2_extract, "SairaCondensed-SemiBold.ufont")
    saira_extra_medium = os.path.join(loc2_extract, "SairaExtraCondensed-MediumItalic.ufont")
    saira_extra_semibold = os.path.join(loc2_extract, "SairaExtraCondensed-SemiBoldItalic.ufont")
    roboto_upright = os.path.join(loc2_extract, "RobotoCondensed-VariableFont_wght.ufont")

    if os.path.exists(saira_medium) and os.path.exists(saira_semibold):
        shutil.copy2(saira_medium,   os.path.join(loc2_build, "SairaCondensed-Regular.ufont"))
        shutil.copy2(saira_medium,   os.path.join(loc2_build, "SairaCondensed-Medium.ufont"))
        shutil.copy2(saira_medium,   os.path.join(loc2_build, "SairaCondensed-MediumItalic.ufont"))
        shutil.copy2(saira_semibold, os.path.join(loc2_build, "SairaCondensed-SemiBold.ufont"))
        shutil.copy2(saira_semibold, os.path.join(loc2_build, "SairaCondensed-Bold.ufont"))
        for f in os.listdir(loc2_extract):
            if f.startswith("SairaCondensed") and (f.endswith(".uasset") or f.endswith(".uexp")):
                shutil.copy2(os.path.join(loc2_extract, f), os.path.join(loc2_build, f))

    # SairaExtraCondensed italic -> override bằng bản đứng thẳng tương ứng
    saira_extra_upright_medium = os.path.join(loc2_extract, "SairaCondensed-Medium.ufont")
    saira_extra_upright_semibold = os.path.join(loc2_extract, "SairaCondensed-SemiBold.ufont")
    if os.path.exists(saira_extra_medium):
        shutil.copy2(saira_extra_upright_medium, os.path.join(loc2_build, "SairaExtraCondensed-MediumItalic.ufont"))
        for f in os.listdir(loc2_extract):
            if f.startswith("SairaExtraCondensed-MediumItalic") and (f.endswith(".uasset") or f.endswith(".uexp")):
                shutil.copy2(os.path.join(loc2_extract, f), os.path.join(loc2_build, f))
    if os.path.exists(saira_extra_semibold):
        # SairaExtraCondensed-SemiBoldItalic -> dùng chính file của nó nhưng thay ufont bằng medium upright
        shutil.copy2(saira_extra_upright_medium, os.path.join(loc2_build, "SairaExtraCondensed-SemiBoldItalic.ufont"))
        for f in os.listdir(loc2_extract):
            if f.startswith("SairaExtraCondensed-SemiBoldItalic") and (f.endswith(".uasset") or f.endswith(".uexp")):
                shutil.copy2(os.path.join(loc2_extract, f), os.path.join(loc2_build, f))

    # RobotoCondensed-Italic -> override bằng bản đứng thẳng (dùng file ufont đứng thẳng của Roboto)
    roboto_italic_ufont = os.path.join(loc2_extract, "RobotoCondensed-Italic-VariableFont_wght.ufont")
    if os.path.exists(roboto_upright):
        # Roboto upright ufont thay thế italic ufont
        shutil.copy2(roboto_upright, os.path.join(loc2_build, "RobotoCondensed-Italic-VariableFont_wght.ufont"))
        for f in os.listdir(loc2_extract):
            if "Italic" in f and f.startswith("RobotoCondensed") and (f.endswith(".uasset") or f.endswith(".uexp")):
                shutil.copy2(os.path.join(loc2_extract, f), os.path.join(loc2_build, f))

    print("[✓] Injected 100% upright fonts - không còn font nghiêng nào trong pak!")

def compile_datatables():
    converter_proj = os.path.join(CURRENT_DIR, "tools", "DataTableConverter", "DataTableConverter.csproj")
    if os.path.exists(converter_proj) and shutil.which("dotnet"):
        try:
            print("[*] Đang tự động biên dịch 39 DataTables sang binary UE5.5...")
            subprocess.run(["dotnet", "run", "--project", converter_proj], cwd=CURRENT_DIR, check=True)
            print("[✓] Đã biên dịch DataTables thành công!")
        except Exception as e:
            print(f"[!] Cảnh báo biên dịch DataTables: {e}")

def pack_mod():
    compile_datatables()
    inject_custom_fonts()
    os.makedirs(DIST_DIR, exist_ok=True)
    pak_output = os.path.join(DIST_DIR, "pakchunk99-Vietnamese_P.pak")
    
    print("Packing mod files into pakchunk99-Vietnamese_P.pak...")
    cmd = [
        REPAK_EXE,
        "pack",
        "--version", "V11",
        "--mount-point", "../../../",
        BUILD_DIR,
        pak_output
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print(f"Error packing: {res.stderr}")
        return False
    
    print(f"Packed successfully: {pak_output} ({os.path.getsize(pak_output):,} bytes)")
    return pak_output

def deploy_to_game(pak_path):
    if not os.path.exists(GAME_PAKS_DIR):
        print(f"Game Paks directory not found at: {GAME_PAKS_DIR}")
        return
    
    os.makedirs(MODS_SUBDIR, exist_ok=True)
    dest_path = os.path.join(MODS_SUBDIR, os.path.basename(pak_path))
    try:
        shutil.copy2(pak_path, dest_path)
        print(f"Deployed mod to game: {dest_path}")
    except PermissionError:
        print(f"[NOTE] Game is running holding the pak file. Mod pak will be deployed next time game closes.")
    except Exception as e:
        print(f"[WARN] Could not copy to game folder: {e}")

if __name__ == "__main__":
    pak = pack_mod()
    if pak:
        deploy_to_game(pak)
