import os

wb_dir = r"D:\code\mod\world-box-vn"

files_found = []

if os.path.exists(wb_dir):
    for root, dirs, files in os.walk(wb_dir):
        for f in files:
            files_found.append(os.path.join(root, f))

print(f"Found {len(files_found)} files in WorldBox mod:")
for f in files_found[:30]:
    print(f)
