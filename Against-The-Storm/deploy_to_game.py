import os
import shutil

def deploy_ats_mod(game_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_plugin = os.path.join(base_dir, "ATS_Vietnamese")
    
    target_plugin = os.path.join(game_path, "BepInEx", "plugins", "ATS_Vietnamese")
    
    if not os.path.exists(game_path):
        print(f"Error: Game path '{game_path}' not found!")
        return

    os.makedirs(target_plugin, exist_ok=True)
    shutil.copytree(src_plugin, target_plugin, dirs_exist_ok=True)
    print(f"Successfully deployed ATS Vietnamese Mod to: {target_plugin}")

if __name__ == "__main__":
    default_path = r"C:\Users\nam\Downloads\Compressed\Against-The-Storm-AnkerGames\Against the Storm"
    deploy_ats_mod(default_path)
