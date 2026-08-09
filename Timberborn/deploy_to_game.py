import os
import shutil
import zipfile

def package_tb_mod():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mod_src = os.path.join(base_dir, "Mods", "VietnameseLanguage")
    zip_output = os.path.join(base_dir, "Mods", "VietnameseLanguage_Mod.zip")
    
    if not os.path.exists(mod_src):
        print(f"Error: {mod_src} not found!")
        return

    with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(mod_src):
            for file in files:
                full_p = os.path.join(root, file)
                rel_p = os.path.relpath(full_p, os.path.join(base_dir, "Mods"))
                zipf.write(full_p, rel_p)

    print(f"Successfully packaged Timberborn Mod ZIP to: {zip_output}")

def deploy_tb_mod(documents_tb_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_mod = os.path.join(base_dir, "Mods")
    target_mod = os.path.join(documents_tb_path, "Mods")
    
    if not os.path.exists(documents_tb_path):
        print(f"Error: Documents Timberborn path '{documents_tb_path}' not found!")
        return

    os.makedirs(target_mod, exist_ok=True)
    shutil.copytree(src_mod, target_mod, dirs_exist_ok=True)
    print(f"Successfully deployed Timberborn Mod to: {target_mod}")

if __name__ == "__main__":
    package_tb_mod()
    default_doc_path = r"C:\Users\nam\Documents\Timberborn"
    deploy_tb_mod(default_doc_path)
