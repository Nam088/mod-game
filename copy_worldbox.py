import os
import shutil

src_wb = r"D:\code\mod\world-box-vn"
dest_wb = r"D:\mod-game\WorldBox"

if os.path.exists(src_wb):
    # Copy all files ignoring .git directory
    def ignore_git(dir, files):
        return [f for f in files if f == '.git']
        
    shutil.copytree(src_wb, dest_wb, ignore=ignore_git, dirs_exist_ok=True)
    print("Successfully copied WorldBox mod from D:\\code\\mod\\world-box-vn to D:\\mod-game\\WorldBox!")
else:
    print(f"Error: {src_wb} does not exist!")
