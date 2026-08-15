---
name: game-mod-cicd-workflow
description: Hướng dẫn quy trình CI/CD tự động Build, Pack ZIP, Tăng Version và Tạo GitHub Releases cho các dự án Mod Game (Oxygen Not Included, Timberborn, Against The Storm, WorldBox). Kích hoạt khi AI thực hiện build mod, cập nhật bản dịch, đóng gói file ZIP hoặc kích hoạt phát hành bản dịch mới.
---

# 🚀 Quy Trình CI/CD & Đóng Gói Bản Dịch Đa Game (Multi-Game Modding CI/CD)

Skill này quy định quy trình chuẩn hóa từ khâu kiểm định bản dịch, tự động tăng phiên bản (SemVer), lọc và đóng gói file ZIP sạch sẽ vào thư mục `dist/`, cho đến khi tạo GitHub Release tự động.

---

## 1. 📂 Cấu Trúc Đa Game Trong Repository

Repository quản lý nhiều tựa game độc lập. Mỗi game có thư mục nguồn và thư mục `dist/` riêng:

| Game | Thư mục Mod Nguồn | Thư mục Dist | Tiền tố Tag Release | File Quản Lý Version |
|---|---|---|---|---|
| **Oxygen Not Included** | `Oxygen-Not-Included/dist/Oxygen-Not-Included-Vietnamese` | `Oxygen-Not-Included/dist` | `oni-v*` | `mod_info.yaml` |
| **Timberborn** | `Timberborn/Mods/VietnameseLanguage` | `Timberborn/dist` | `tb-v*` | `manifest.json` |
| **Against The Storm** | `Against-The-Storm/ATS_Vietnamese` | `Against-The-Storm/dist` | `ats-v*` | `version.json` |
| **WorldBox** | `WorldBox/steam_workshop_mod` | `WorldBox/dist` | `wb-v*` | `mod.json` |

---

## 2. 🛠️ Quy Trình Tự Động Hóa (Automation Workflow)

### Bước 1: Phát hiện thay đổi (Change Detection)
CI sẽ tự động chạy lệnh `git diff` giữa commit hiện tại và commit trước (`HEAD~1`):
- Nếu thay đổi xảy ra ở game nào, **chỉ game đó** được kích hoạt build và tạo release.
- Bỏ qua các commit chỉ sửa tài liệu Markdown (`.md`) hoặc file trong thư mục `dist/`.

### Bước 2: Tự Động Tăng Version (SemVer Bump)
- Mặc định tăng số bản vá (`Patch`): `1.0.1` ➔ `1.0.2`.
- Cập nhật trực tiếp vào file metadata của game (`mod_info.yaml`, `manifest.json`, `mod.json`, `version.json`).

### Bước 3: Lọc & Đóng Gói File ZIP Tinh Gọn (Clean Packaging)
- **Quy tắc vàng**: File ZIP chỉ chứa **đúng các file mod thực thi cần thiết** cho người chơi.
- **Tự động loại bỏ**: File mã nguồn script (`.py`), file test (`check_*.py`), file patch trung gian (`patch_*_ready.json`), file tạm (`.tmp`, `.log`, `.DS_Store`).
- File ZIP được tạo trực tiếp vào thư mục `<Game>/dist/<Game>-Vietnamese-Mod-v<version>.zip`.

### Bước 4: Tạo GitHub Release & Nhúng Ảnh Preview
- Tự động tạo Release với tag độc lập (`oni-v*`, `tb-v*`, `ats-v*`, `wb-v*`).
- Nhúng ảnh bìa nghệ thuật có cờ Việt Nam (`preview.png`) vào thẳng nội dung Release Notes.
- Đính kèm file `.zip` sạch sẽ để người dùng tải về cài đặt ngay.

---

## 3. 💻 Các Lệnh Thao Tác Trực Tiếp (CLI Commands)

### 1. Chạy Build & Đóng Gói Cục Bộ:
```bash
# Tự động detect game thay đổi và build:
python3 scripts/build_and_package_mods.py --game auto

# Build tất cả 4 game:
python3 scripts/build_and_package_mods.py --game all

# Build riêng 1 game và tăng version:
python3 scripts/build_and_package_mods.py --game Oxygen-Not-Included --bump
```

### 2. Kích hoạt CI/CD thủ công qua GitHub CLI:
```bash
# Kích hoạt release cho 1 game:
gh workflow run build_and_release.yml -R Nam088/mod-game -f game=Oxygen-Not-Included -f bump_version=true

# Kích hoạt release cho tất cả game:
gh workflow run build_and_release.yml -R Nam088/mod-game -f game=all -f bump_version=true
```
