import os
import subprocess
import sys

def run_cmd(cmd, cwd=None):
    print(f">> {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        print(res.stderr.strip())
    return res.returncode

def main():
    mod_root = r"D:\mod-game"
    os.makedirs(mod_root, exist_ok=True)
    
    print(f"=== COMMITTING D:\\mod-game TO GITHUB ===")
    
    # Create .gitignore in D:\mod-game
    gitignore_path = os.path.join(mod_root, ".gitignore")
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write("*.pyc\n__pycache__/\n.vs/\n*.user\n")

    # Check if git is initialized in D:\mod-game
    if run_cmd("git status", cwd=mod_root) != 0:
        run_cmd("git init", cwd=mod_root)

    # Add all files
    run_cmd("git add .", cwd=mod_root)
    
    # Commit
    msg = "Update Full Unabridged Vietnamese Localization Mod for Against The Storm"
    run_cmd(f'git commit -m "{msg}"', cwd=mod_root)
    
    print("\nLocal Git commit completed for D:\\mod-game!")
    print("To push to your remote GitHub repository, run:")
    print("  cd /d D:\\mod-game")
    print("  git remote add origin <your-github-repo-url>")
    print("  git branch -M main")
    print("  git push -u origin main")

if __name__ == "__main__":
    main()
