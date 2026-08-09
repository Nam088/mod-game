import os
import subprocess

def run_cmd(cmd, cwd):
    print(f">> {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr:
        print(res.stderr.strip())
    return res.returncode

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)
    
    print("=== COMMITTING ALL GAME MODS TO GITHUB ===")
    
    # 1. Against The Storm
    ats_dir = os.path.join(root_dir, "Against-The-Storm")
    if os.path.exists(ats_dir):
        print("\n--- Extracting EN & Building Against The Storm ---")
        run_cmd("python export_en_json.py", cwd=ats_dir)
        run_cmd("python build_combine_vi.py", cwd=ats_dir)
        run_cmd("python deploy_to_game.py", cwd=ats_dir)

    # 2. Timberborn
    tb_dir = os.path.join(root_dir, "Timberborn")
    if os.path.exists(tb_dir):
        print("\n--- Extracting EN & Deploying Timberborn ---")
        run_cmd("python export_en_from_game.py", cwd=tb_dir)
        run_cmd("python export_csv_mod.py", cwd=tb_dir)
        run_cmd("python deploy_to_game.py", cwd=tb_dir)

    # 3. Git Add & Commit
    print("\n--- Staging & Committing to Git ---")
    run_cmd("git add -A", cwd=root_dir)
    msg = "Clean up temporary scripts and consolidate project structure"
    run_cmd(f'git commit -m "{msg}"', cwd=root_dir)
    
    print("\nLocal Git commit completed for all game mods!")
    print("To push to your remote GitHub repository, run:")
    print("  cd /d D:\\mod-game")
    print("  git remote add origin <your-github-repo-url>")
    print("  git branch -M main")
    print("  git push -u origin main")

if __name__ == "__main__":
    main()
