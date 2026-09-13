import os
import sys
import json
import shutil
import zipfile
import subprocess
import platform
import stat
import urllib.request
import tarfile

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(PROJECT_ROOT, "tools")
BUILD_DIR = os.path.join(PROJECT_ROOT, "build")
DIST_DIR = os.path.join(PROJECT_ROOT, "dist")
TRANS_DIR = os.path.join(PROJECT_ROOT, "translations")
EXTRACTED_DIR = os.path.join(PROJECT_ROOT, "extracted")
FONTS_BUILT_DIR = os.path.join(TOOLS_DIR, "fonts_built")
VERSION_FILE = os.path.join(PROJECT_ROOT, "version.json")

GAME_PAK_MODS_DIR = r"C:\Users\nam\Downloads\Compressed\Whiskerwood-AnkerGames\Whiskerwood\Whiskerwood\Content\Paks\~mods"

sys.path.append(TOOLS_DIR)
from uasset_patcher import patch_loc_en
from build_vietnamese_fonts import build_all_fonts

def get_repak_exe():
    """Trả về đường dẫn repak binary đúng theo platform (Windows/Linux CI), tự download nếu chưa có."""
    is_windows = platform.system() == "Windows"
    repak_name = "repak.exe" if is_windows else "repak"
    repak_path = os.path.join(TOOLS_DIR, repak_name)

    if os.path.exists(repak_path):
        if not is_windows:
            os.chmod(repak_path, os.stat(repak_path).st_mode | stat.S_IEXEC)
        return repak_path

    # Tìm download URL từ GitHub API (latest release)
    print(f"[*] Đang tìm repak binary cho {platform.system()} từ GitHub releases...")
    api_url = "https://api.github.com/repos/trumank/repak/releases/latest"
    req = urllib.request.Request(api_url, headers={"User-Agent": "mod-game-builder"})
    with urllib.request.urlopen(req) as resp:
        release = json.loads(resp.read().decode('utf-8'))

    asset_url = None
    asset_name = None
    for asset in release.get("assets", []):
        n = asset["name"]
        if is_windows and "windows-msvc" in n and n.endswith(".zip"):
            asset_url = asset["browser_download_url"]
            asset_name = n
            break
        if not is_windows and "linux" in n and (n.endswith(".tar.xz") or n.endswith(".tar.gz")):
            asset_url = asset["browser_download_url"]
            asset_name = n
            break

    if not asset_url:
        raise RuntimeError(f"Không tìm thấy repak binary cho {platform.system()} trong release {release.get('tag_name')}")

    print(f"[*] Đang tải repak ({asset_name}) từ {asset_url}...")
    archive_path = os.path.join(TOOLS_DIR, asset_name)
    urllib.request.urlretrieve(asset_url, archive_path)

    if asset_name.endswith(".zip"):
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(TOOLS_DIR)
    elif asset_name.endswith((".tar.xz", ".tar.gz")):
        mode = "r:xz" if asset_name.endswith(".tar.xz") else "r:gz"
        with tarfile.open(archive_path, mode) as tf:
            for member in tf.getmembers():
                if member.name.endswith("repak") or member.name.endswith("repak.exe"):
                    member.name = os.path.basename(member.name)
                    tf.extract(member, TOOLS_DIR)

    if os.path.exists(archive_path):
        os.remove(archive_path)

    if not is_windows and os.path.exists(repak_path):
        os.chmod(repak_path, os.stat(repak_path).st_mode | stat.S_IEXEC)

    return repak_path

def get_mod_version():
    if os.path.exists(VERSION_FILE):
        try:
            with open(VERSION_FILE, "r", encoding="utf-8") as f:
                return json.load(f).get("version", "0.1.0")
        except Exception:
            pass
    return "0.1.0"

def build():
    print("==================================================")
    print("      BUILDING WHISKERWOOD VIETNAMESE MOD         ")
    print("==================================================")

    version_str = get_mod_version()
    print(f"[*] Phiên bản Mod: v{version_str}")

    # 1. Merge translations
    json_files = [f for f in sorted(os.listdir(TRANS_DIR)) if f.endswith(".json") and not f.endswith("Master.json")]
    all_entries = []
    
    for jf in json_files:
        fpath = os.path.join(TRANS_DIR, jf)
        with open(fpath, "r", encoding="utf-8") as f:
            entries = json.load(f)
            all_entries.extend(entries)
            
    print(f"Loaded total {len(all_entries)} translation entries from {len(json_files)} files.")

    # 2. Patch Loc_En asset
    orig_uasset = os.path.join(EXTRACTED_DIR, "Whiskerwood", "Content", "Data", "TextDB", "Loc_En.uasset")
    orig_uexp = os.path.join(EXTRACTED_DIR, "Whiskerwood", "Content", "Data", "TextDB", "Loc_En.uexp")
    
    out_uasset = os.path.join(BUILD_DIR, "Whiskerwood", "Content", "Data", "TextDB", "Loc_En.uasset")
    out_uexp = os.path.join(BUILD_DIR, "Whiskerwood", "Content", "Data", "TextDB", "Loc_En.uexp")
    
    patch_loc_en(all_entries, orig_uasset, orig_uexp, out_uasset, out_uexp)

    # 3. Build & Integrate 100% Be Vietnam Pro Fonts
    print("[FONTS] Building Be Vietnam Pro font assets...")
    build_all_fonts()

    dest_fonts_dir = os.path.join(BUILD_DIR, "Whiskerwood", "Content", "Assets", "Fonts")
    
    if os.path.exists(dest_fonts_dir):
        shutil.rmtree(dest_fonts_dir)
    os.makedirs(dest_fonts_dir, exist_ok=True)

    font_count = 0
    for root, dirs, files in os.walk(FONTS_BUILT_DIR):
        for f in files:
            if f.endswith(".ufont"):
                src_file = os.path.join(root, f)
                rel_path = os.path.relpath(src_file, FONTS_BUILT_DIR)
                target_file = os.path.join(dest_fonts_dir, rel_path)
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                shutil.copy2(src_file, target_file)
                font_count += 1
                
    print(f"[SUCCESS] Deployed {font_count} BE VIETNAM PRO .ufont files into mod build:")
    print("  - LibreBaskerville (Sách & Tiêu đề) -> Be Vietnam Pro Regular & Bold")
    print("  - Belleza (Tiêu đề thanh mảnh)      -> Be Vietnam Pro Regular")
    print("  - Germania_One (Antique / Title)    -> Be Vietnam Pro Bold")
    print("  - La_Belle_Aurore (Thư từ / Ký tự)  -> Be Vietnam Pro Regular (siêu rõ, êm mắt)")
    print("  - Poppins (Giao diện UI & HUD)      -> Be Vietnam Pro (đủ 9 biến thể Regular, Medium, Bold, Italic)")

    # 4. Pack into .pak file
    repak_bin = get_repak_exe()
    out_pak = os.path.join(PROJECT_ROOT, "Whiskerwood-Vietnamese_P.pak")
    print(f"\nPacking {BUILD_DIR} into {out_pak} using {repak_bin}...")
    
    cmd = [
        repak_bin,
        "pack",
        "--version", "V11",
        BUILD_DIR,
        out_pak
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] repak pack failed: {res.stderr}")
        return False
        
    print(f"[SUCCESS] Successfully built: {out_pak} (Size: {os.path.getsize(out_pak):,} bytes)")

    # 5. Deploy to local game ~mods folder (only if NOT running in CI)
    is_ci = os.environ.get("CI") == "true"
    if not is_ci and os.path.exists(os.path.dirname(GAME_PAK_MODS_DIR)):
        os.makedirs(GAME_PAK_MODS_DIR, exist_ok=True)
        target_pak = os.path.join(GAME_PAK_MODS_DIR, "Whiskerwood-Vietnamese_P.pak")
        try:
            shutil.copy2(out_pak, target_pak)
            print(f"[DEPLOYED] Successfully copied mod to game folder:\n  -> {target_pak}")
        except PermissionError:
            print(f"[NOTE] Game Whiskerwood hiện đang chạy và khóa file PAK.")
            print(f"       File PAK mới ({out_pak}) đã sẵn sàng. Vui lòng tắt game rồi copy đè!")

    # 6. Create release package ZIP in both root and dist/
    os.makedirs(DIST_DIR, exist_ok=True)
    zip_name = f"Whiskerwood-Vietnamese-Mod-v{version_str}.zip"
    zip_paths = [
        os.path.join(PROJECT_ROOT, zip_name),
        os.path.join(DIST_DIR, zip_name)
    ]
    
    readme_txt = f"""WHISKERWOOD - BẢN DỊCH TIẾNG VIỆT (VIETNAMESE MOD)
Tác giả: Nam088
Phiên bản: v{version_str} (Unreal Engine 5)
Tương thích: Bản quyền Steam, Epic Games, GOG

ĐIỂM NỔI BẬT VỀ FONT CHỮ (BE VIETNAM PRO):
- Tích hợp 100% họ font BE VIETNAM PRO cao cấp:
  * Kiểu chữ Geometric Sans-Serif chuẩn quốc tế được thiết kế chuyên biệt cho Tiếng Việt.
  * Tỉ lệ hình học 1:1 với font Poppins gốc của game, độ thoáng dấu thanh điệu tuyệt đối.
  * Hiển thị cực kỳ thanh thoát, êm mắt, hiện đại và không bị lỗi ô vuông trên mọi độ phân giải.

HƯỚNG DẪN CÀI ĐẶT:
1. Sao chép tệp 'Whiskerwood-Vietnamese_P.pak' vào thư mục:
   [Thư Mục Cài Game]\\Whiskerwood\\Content\\Paks\\~mods\\
   (Nếu chưa có thư mục '~mods', hãy tạo một thư mục mới có tên là '~mods').

2. Khởi động game Whiskerwood. Toàn bộ giao diện, công trình, chuỗi cung ứng,
   tâm lý bầy chuột và cốt truyện sẽ tự động hiển thị Tiếng Việt 100%!

Chúc bạn có những giờ phút xây dựng thuộc địa làng chuột thật vui vẻ!
"""

    for zp in zip_paths:
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(out_pak, "Whiskerwood-Vietnamese_P.pak")
            zf.writestr("HUONG_DAN_CAI_DAT.txt", readme_txt)
        print(f"[RELEASE ZIP] Created {zp} ({os.path.getsize(zp):,} bytes)")
        
    return True

if __name__ == "__main__":
    build()
