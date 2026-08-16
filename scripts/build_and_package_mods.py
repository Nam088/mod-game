#!/usr/bin/env python3
import os, sys, json, zipfile, shutil, subprocess, re

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GAMES_CONFIG = {
    "Oxygen-Not-Included": {
        "name": "Oxygen Not Included",
        "slug": "oxygen-not-included",
        "tag_prefix": "oni",
        "dir": "Oxygen-Not-Included",
        "version_files": [
            {
                "type": "yaml_regex",
                "path": "Oxygen-Not-Included/dist/Oxygen-Not-Included-Vietnamese/mod_info.yaml",
                "pattern": r"(version:\s*)([\d\.]+)",
            },
            {
                "type": "yaml_regex",
                "path": "Oxygen-Not-Included/mod_info.yaml",
                "pattern": r"(version:\s*)([\d\.]+)",
            }
        ],
        "dist_dir": "Oxygen-Not-Included/dist",
        "mod_package_dir": "Oxygen-Not-Included/dist/Oxygen-Not-Included-Vietnamese",
        "zip_prefix": "Oxygen-Not-Included-Vietnamese",
    },
    "Timberborn": {
        "name": "Timberborn",
        "slug": "timberborn",
        "tag_prefix": "tb",
        "dir": "Timberborn",
        "version_files": [
            {
                "type": "json",
                "path": "Timberborn/Mods/VietnameseLanguage/manifest.json",
                "key": "Version"
            }
        ],
        "dist_dir": "Timberborn/dist",
        "mod_package_dir": "Timberborn/Mods/VietnameseLanguage",
        "zip_prefix": "Timberborn-Vietnamese-Mod",
    },
    "Against-The-Storm": {
        "name": "Against The Storm",
        "slug": "against-the-storm",
        "tag_prefix": "ats",
        "dir": "Against-The-Storm",
        "version_files": [
            {
                "type": "json",
                "path": "Against-The-Storm/version.json",
                "key": "version",
                "create_if_missing": True,
                "default_version": "1.0.0"
            }
        ],
        "dist_dir": "Against-The-Storm/dist",
        "mod_package_dir": "Against-The-Storm/ATS_Vietnamese",
        "zip_prefix": "Against-The-Storm-Vietnamese-Mod",
    },
    "WorldBox": {
        "name": "WorldBox",
        "slug": "worldbox",
        "tag_prefix": "wb",
        "dir": "WorldBox",
        "version_files": [
            {
                "type": "json",
                "path": "WorldBox/steam_workshop_mod/mod.json",
                "key": "Version"
            }
        ],
        "dist_dir": "WorldBox/dist",
        "mod_package_dir": "WorldBox/steam_workshop_mod",
        "zip_prefix": "WorldBox-Vietnamese-Mod",
    },
    "Manor-Lords": {
        "name": "Manor Lords",
        "slug": "manor-lords",
        "tag_prefix": "ml",
        "dir": "Manor-Lords",
        "version_files": [
            {
                "type": "json",
                "path": "Manor-Lords/version.json",
                "key": "version",
                "create_if_missing": True,
                "default_version": "1.0.0"
            }
        ],
        "dist_dir": "Manor-Lords/dist",
        "mod_package_dir": "Manor-Lords/dist",
        "zip_prefix": "Manor-Lords-Vietnamese-Mod",
    }
}

def bump_semver(version_str, bump_type="patch"):
    parts = [int(p) for p in version_str.strip().split(".")]
    while len(parts) < 3: parts.append(0)
    if bump_type == "patch": parts[2] += 1
    elif bump_type == "minor": parts[1] += 1; parts[2] = 0
    elif bump_type == "major": parts[0] += 1; parts[1] = 0; parts[2] = 0
    return ".".join(str(p) for p in parts)

def get_current_version(game_cfg):
    for vf in game_cfg["version_files"]:
        fpath = os.path.join(BASE_DIR, vf["path"])
        if not os.path.exists(fpath):
            if vf.get("create_if_missing"):
                os.makedirs(os.path.dirname(fpath), exist_ok=True)
                with open(fpath, "w", encoding="utf-8") as f:
                    json.dump({vf["key"]: vf.get("default_version", "1.0.0")}, f, indent=2)
                return vf.get("default_version", "1.0.0")
            continue
        if vf["type"] == "json":
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(vf["key"], "1.0.0")
        elif vf["type"] == "yaml_regex":
            with open(fpath, "r", encoding="utf-8") as f:
                c = f.read()
                m = re.search(vf["pattern"], c)
                if m: return m.group(2)
    return "1.0.0"

def update_version(game_cfg, new_version):
    for vf in game_cfg["version_files"]:
        fpath = os.path.join(BASE_DIR, vf["path"])
        if not os.path.exists(fpath) and not vf.get("create_if_missing"): continue
        if vf["type"] == "json":
            data = {}
            if os.path.exists(fpath):
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            data[vf["key"]] = new_version
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        elif vf["type"] == "yaml_regex":
            with open(fpath, "r", encoding="utf-8") as f:
                c = f.read()
            new_c = re.sub(vf["pattern"], r"\g<1>" + new_version, c)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_c)

def build_game_mod(game_key, auto_bump=False, bump_type="patch"):
    cfg = GAMES_CONFIG[game_key]
    print("\n=======================================================")
    print("🔨 ĐANG BUILD & ĐÓNG GÓI CHO GAME: " + cfg["name"] + " (" + game_key + ")")
    print("=======================================================")
    current_ver = get_current_version(cfg)
    target_ver = current_ver
    if auto_bump:
        target_ver = bump_semver(current_ver, bump_type)
        print("[*] Tự động tăng version: " + current_ver + " -> " + target_ver)
        update_version(cfg, target_ver)
    else:
        print("[*] Giữ nguyên version: " + target_ver)

    if game_key == "Oxygen-Not-Included":
        po_path = os.path.join(BASE_DIR, "Oxygen-Not-Included/strings/strings.po")
        dist_mod_dir = os.path.join(BASE_DIR, cfg["mod_package_dir"])
        os.makedirs(dist_mod_dir, exist_ok=True)
        shutil.copy(po_path, os.path.join(dist_mod_dir, "strings.po"))
        sys.path.insert(0, os.path.join(BASE_DIR, "Oxygen-Not-Included/strings"))
        try:
            import polib
            po = polib.pofile(po_path)
            po.save_as_mofile(os.path.join(dist_mod_dir, "strings.mo"))
            po.save_as_mofile(os.path.join(BASE_DIR, "Oxygen-Not-Included/strings/strings.mo"))
            print("[✓] Đã biên dịch strings.mo cho Oxygen Not Included")
        except Exception as e:
            print("[!] Cảnh báo biên dịch MO: " + str(e))

    if game_key == "Manor-Lords":
        ml_dir = os.path.join(BASE_DIR, "Manor-Lords")
        dist_dir = os.path.join(BASE_DIR, cfg["dist_dir"])
        os.makedirs(dist_dir, exist_ok=True)
        pak_path = os.path.join(dist_dir, "pakchunk99-Vietnamese_P.pak")
        
        converter_proj = os.path.join(ml_dir, "tools", "DataTableConverter", "DataTableConverter.csproj")
        if os.path.exists(converter_proj) and shutil.which("dotnet"):
            try:
                subprocess.run(["dotnet", "run", "--project", converter_proj], cwd=ml_dir, check=True)
                subprocess.run([sys.executable, os.path.join(ml_dir, "build_and_deploy_mod.py")], cwd=ml_dir, check=True)
                print("[✓] Đã recompile và build pak cho Manor Lords")
            except Exception as e:
                print(f"[!] Cảnh báo build PAK: {e}")
        
        zip_name = cfg["zip_prefix"] + "-v" + target_ver + ".zip"
        zip_path = os.path.join(dist_dir, zip_name)
        if os.path.exists(zip_path): os.remove(zip_path)
        
        readme_path = os.path.join(dist_dir, "Huong_Dan_Cai_Dat.txt")
        banner_path = os.path.join(ml_dir, "banner.jpg")
        
        print(f"[*] Đóng gói Manor Lords Mod ZIP vào {zip_path}...")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            if os.path.exists(pak_path):
                zipf.write(pak_path, "pakchunk99-Vietnamese_P.pak")
                zipf.write(pak_path, "ManorLords/Content/Paks/~mods/pakchunk99-Vietnamese_P.pak")
            if os.path.exists(banner_path):
                zipf.write(banner_path, "preview_banner.jpg")
            if os.path.exists(readme_path):
                zipf.write(readme_path, "Huong_Dan_Cai_Dat.txt")
                
        zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
        print(f"[✓] Đã tạo thành công: {zip_name} ({zip_size_mb:.2f} MB)")
        return {
            "game_key": game_key,
            "name": cfg["name"],
            "version": target_ver,
            "zip_name": zip_name,
            "zip_path": zip_path,
            "tag": cfg["tag_prefix"] + "-v" + target_ver
        }

    dist_dir = os.path.join(BASE_DIR, cfg["dist_dir"])
    os.makedirs(dist_dir, exist_ok=True)
    zip_name = cfg["zip_prefix"] + "-v" + target_ver + ".zip"
    zip_path = os.path.join(dist_dir, zip_name)
    if os.path.exists(zip_path): os.remove(zip_path)
    src_mod_dir = os.path.join(BASE_DIR, cfg["mod_package_dir"])
    folder_name_in_zip = os.path.basename(src_mod_dir)
    print("[*] Đóng gói thư mục " + src_mod_dir + " vào " + zip_path + "...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(src_mod_dir):
            for file in files:
                # Loại bỏ file rác, file tạm, file test không cần thiết cho người chơi
                ext = os.path.splitext(file)[1].lower()
                fname = file.lower()
                if ext in ['.zip', '.tmp', '.py', '.log', '.bak', '.ds_store'] or fname.startswith('check_') or 'patch_' in fname:
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.join(folder_name_in_zip, os.path.relpath(file_path, src_mod_dir))
                zipf.write(file_path, arcname)
    zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"[✓] Đã tạo thành công: {zip_name} ({zip_size_mb:.2f} MB)")
    return {
        "game_key": game_key,
        "name": cfg["name"],
        "version": target_ver,
        "zip_name": zip_name,
        "zip_path": zip_path,
        "tag": cfg["tag_prefix"] + "-v" + target_ver
    }

def detect_changed_games(base_ref=None):
    if not base_ref:
        cmd = ["git", "diff", "--name-only", "HEAD~1", "HEAD"]
    else:
        cmd = ["git", "diff", "--name-only", base_ref, "HEAD"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        changed_files = res.stdout.strip().splitlines()
    except Exception:
        res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        changed_files = [line[3:].strip() for line in res.stdout.splitlines() if len(line) > 3]
    changed_games = set()
    for f in changed_files:
        for g_key, g_cfg in GAMES_CONFIG.items():
            if f.startswith(g_cfg["dir"] + "/") or f == g_cfg["dir"]:
                if not f.startswith(g_cfg["dist_dir"] + "/"):
                    changed_games.add(g_key)
    return list(changed_games)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Multi-game Mod Builder & Release Manager")
    parser.add_argument("--game", choices=list(GAMES_CONFIG.keys()) + ["all", "auto"], default="auto")
    parser.add_argument("--bump", action="store_true")
    parser.add_argument("--bump-type", choices=["patch", "minor", "major"], default="patch")
    parser.add_argument("--base-ref", default=None)
    parser.add_argument("--output-json", default=None)
    args = parser.parse_args()
    games_to_build = []
    if args.game == "all":
        games_to_build = list(GAMES_CONFIG.keys())
    elif args.game == "auto":
        detected = detect_changed_games(args.base_ref)
        if not detected:
            for g_key, g_cfg in GAMES_CONFIG.items():
                dist_dir = os.path.join(BASE_DIR, g_cfg["dist_dir"])
                if not os.path.exists(dist_dir) or not any(f.endswith(".zip") for f in os.listdir(dist_dir)):
                    games_to_build.append(g_key)
        else:
            print(f"[*] Phát hiện thay đổi ở các game: {detected}")
            games_to_build = detected
    else:
        games_to_build = [args.game]
    results = []
    for g in games_to_build:
        res = build_game_mod(g, auto_bump=args.bump, bump_type=args.bump_type)
        results.append(res)
    if args.output_json:
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n[✓] Đã xuất kết quả ra {args.output_json}")
    print("\n=== HOÀN TẤT BUILD TẤT CẢ GAME YÊU CẦU ===")

if __name__ == "__main__":
    main()
