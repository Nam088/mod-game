import os
import sys
import shutil
import zipfile
from build_mod_csv import build_csv

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def deploy():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Build latest Vietnamese.csv
    csv_file = build_csv()
    
    # 2. Target user mods directory for Going Medieval
    user_docs = os.path.join(os.environ.get('USERPROFILE', r'C:\Users\nam'), 'Documents')
    foxy_mod_dir = os.path.join(user_docs, 'Foxy Voxel', 'Going Medieval', 'Mods', 'VietnameseLocalization')
    foxy_loc_dir = os.path.join(foxy_mod_dir, 'Data', 'Localization')
    
    os.makedirs(foxy_loc_dir, exist_ok=True)
    
    # Copy ModInfo.json
    shutil.copy2(os.path.join(base_dir, 'ModInfo.json'), os.path.join(foxy_mod_dir, 'ModInfo.json'))
    
    # Copy PreviewTranslation.png
    preview_path = os.path.join(base_dir, 'PreviewTranslation.png')
    if os.path.exists(preview_path):
        shutil.copy2(preview_path, os.path.join(foxy_mod_dir, 'PreviewTranslation.png'))
        
    # Copy Vietnamese.csv
    shutil.copy2(csv_file, os.path.join(foxy_loc_dir, 'Vietnamese.csv'))
    
    print(f"✅ Successfully deployed mod to: {foxy_mod_dir}")

    # 3. Create Distribution ZIP in dist/
    dist_dir = os.path.join(base_dir, 'dist')
    os.makedirs(dist_dir, exist_ok=True)
    zip_name = 'GoingMedieval-VietnameseMod-v1.0.0.zip'
    zip_path = os.path.join(dist_dir, zip_name)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(os.path.join(base_dir, 'ModInfo.json'), 'VietnameseLocalization/ModInfo.json')
        if os.path.exists(preview_path):
            zf.write(preview_path, 'VietnameseLocalization/PreviewTranslation.png')
        zf.write(csv_file, 'VietnameseLocalization/Data/Localization/Vietnamese.csv')
        
    print(f"📦 Built distribution package: {zip_path} ({os.path.getsize(zip_path)} bytes)")

if __name__ == '__main__':
    deploy()
