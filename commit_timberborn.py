import os
import subprocess

def main():
    tb_dir = r"D:\mod-game\Timberborn"
    if not os.path.exists(tb_dir):
        print(f"Directory {tb_dir} does not exist.")
        return

    print(f"=== COMMITTING TIMBERBORN TO GITHUB ===")
    
    # Run git add & commit from D:\mod-game
    root_dir = r"D:\mod-game"
    
    res = subprocess.run("git add Timberborn/", shell=True, capture_output=True, text=True, cwd=root_dir)
    print("git add:", res.stdout or res.stderr)
    
    msg = "Add Timberborn Vietnamese Mod and Localizations from Documents"
    res = subprocess.run(f'git commit -m "{msg}"', shell=True, capture_output=True, text=True, cwd=root_dir)
    print("git commit:", res.stdout or res.stderr)

if __name__ == "__main__":
    main()
