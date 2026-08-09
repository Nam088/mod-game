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
    ats_combine = os.path.join(root_dir, "Against-The-Storm", "build_combine_vi.py")
    if os.path.exists(ats_combine):
        print("\n--- Processing Against The Storm ---")
        run_cmd(f"python {ats_combine}", cwd=os.path.join(root_dir, "Against-The-Storm"))
        run_cmd(f"python Localization_Patches/export_en_master.py", cwd=os.path.join(root_dir, "Against-The-Storm"))

    # 2. Timberborn
    tb_deploy = os.path.join(root_dir, "Timberborn", "deploy_to_game.py")
    if os.path.exists(tb_deploy):
        print("\n--- Processing Timberborn ---")
        run_cmd(f"python {tb_deploy}", cwd=os.path.join(root_dir, "Timberborn"))

    # 3. Git Add & Commit
    print("\n--- Staging & Committing to Git ---")
    run_cmd("git add .", cwd=root_dir)
    msg = "Update full build, export, and deploy scripts for Against The Storm & Timberborn"
    run_cmd(f'git commit -m "{msg}"', cwd=root_dir)
    
    print("\nLocal Git commit completed for all game mods!")
    print("To push to your remote GitHub repository, run:")
    print("  cd /d D:\\mod-game")
    print("  git remote add origin <your-github-repo-url>")
    print("  git branch -M main")
    print("  git push -u origin main")

if __name__ == "__main__":
    main()
