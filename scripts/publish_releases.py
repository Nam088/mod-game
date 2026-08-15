#!/usr/bin/env python3
import os
import sys
import json
import subprocess

def main():
    if not os.path.exists("build_results.json"):
        print("Không tìm thấy build_results.json, bỏ qua release.")
        return
    
    with open("build_results.json", "r", encoding="utf-8") as f:
        results = json.load(f)
        
    for res in results:
        tag = res["tag"]
        name = f"{res['name']} Việt Hóa v{res['version']}"
        zip_path = res["zip_path"]
        zip_name = res["zip_name"]
        
        body = f"### 🎮 Bản Việt Hóa {res['name']} - Phiên bản v{res['version']}\n\n"
        body += f"- 📦 **File cài đặt Mod**: `{zip_name}`\n"
        body += "- 🚀 Tự động build và đóng gói bởi GitHub Actions CI/CD.\n\n"
        body += "**Hướng dẫn cài đặt:**\n"
        body += "1. Tải file `.zip` đính kèm bên dưới.\n"
        body += "2. Giải nén thư mục mod vào thư mục Mod tương ứng của game.\n"
        body += "3. Khởi động game và kích hoạt ngôn ngữ Tiếng Việt."
        
        print(f"[*] Đang tạo GitHub Release cho {tag}...")
        subprocess.run(["gh", "release", "delete", tag, "--yes"], check=False)
        subprocess.run(["git", "push", "origin", f":refs/tags/{tag}"], check=False)
        
        cmd = [
            "gh", "release", "create", tag,
            zip_path,
            "--title", name,
            "--notes", body
        ]
        subprocess.run(cmd, check=True)
        print(f"[✓] Đã tạo release {tag} thành công với asset: {zip_path}")

if __name__ == "__main__":
    main()
