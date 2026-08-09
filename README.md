# 🎮 MOD-GAME REPOSITORY

Kho lưu trữ mã nguồn, công cụ và bản dịch Việt hóa cho các tựa game PC.

---

## 🌩️ 1. Against The Storm (`mod-game/Against-The-Storm`)

### 📌 Giới Thiệu Game:
**Against the Storm** là tựa game xây dựng thành phố kết hợp yếu tố sinh tồn roguelite trong thế giới kỳ ảo đen tối. Người chơi đóng vai Quan Tổng Đốc (Viceroy) được Nữ Hoàng cử đi khai phá hoang dã, xây dựng chuỗi các khu định cư để thu thập tài nguyên và rèn lại các Phong Ấn Cổ Đại trước khi Bão Blight quét sạch thế giới.

### 🛠️ Chi Tiết Mod Việt Hóa:
- **Tình trạng dịch**: **100% Hoàn thành (8,190+ keys)**.
- **Tính năng nổi bật**:
  - Dịch đầy đủ 100% nguyên văn chi tiết từng câu chữ (không tóm tắt), giữ nguyên toàn bộ biến tham số `{0}`, `{1}` và định dạng thẻ hiệu ứng.
  - Tích hợp **Plugin C# Dual Font Override** (`AgainstTheStorm_VietnameseMod.dll`): tự động thay thế phông chữ mặc định của game bằng phông chữ **Arial** (cho UI) và **Georgia** (cho Tiêu đề & Bách Khoa Toàn Thư Wiki), khắc phục 100% lỗi phông chữ Tiếng Việt không bị mất dấu hay lỗi ký tự.
  - Chuẩn hóa bộ thuật ngữ gamer (Hearth = *Lò Sưởi*, Resolve = *Ý Chí*, Glade = *Vùng Rừng*, Cornerstone = *Đá Nền*, Blightstorm = *Bão Blight*, Citadel = *Hoàng Thành Tro Tàn*, Prestige = *Prestige*).

### 📁 Cấu Trúc Thư Mục:
```text
mod-game/Against-The-Storm/
├── ATS_Vietnamese/
│   ├── AgainstTheStorm_VietnameseMod.dll  # Plugin C# override font UI & Wiki
│   ├── vi.json                            # Master tệp Việt hóa (8,190 keys)
│   ├── vi_translation.json                # Tệp nạp trực tiếp cho plugin game
│   └── vi_patch_1_ready.json -> patch_17 # Các patch dịch theo từng phần
└── Localization_Patches/
    ├── patch_1.json -> patch_17.json      # 17 patch gốc Tiếng Anh
    ├── en.json                            # Master tệp gốc Tiếng Anh (8,142 keys)
    └── export_en_master.py                # Script xuất tổng hợp tệp en.json
```

---

## 🦫 2. Timberborn (`mod-game/Timberborn`)

### 📌 Giới Thiệu Game:
**Timberborn** là tựa game xây dựng thành phố xã hội loài hải ly độc đáo trong bối cảnh thế giới hậu tận thế con người đã diệt vong. Người chơi điều khiển một trong hai chủng tộc hải ly (Folktails yêu thiên nhiên hoặc Iron Teeth công nghiệp) xây dựng công trình gỗ nhiều tầng, quản lý nguồn nước, đập ngăn nước và chống chọi qua các mùa hạn hán khốc liệt.

### 🛠️ Chi Tiết Mod Việt Hóa:
- **Tình trạng dịch**: Bản mod ngôn ngữ chuẩn hóa cấu trúc **`VietnameseLanguage`**.
- **Tính năng nổi bật**:
  - Cấu trúc Mod chính thức hỗ trợ sẵn cơ chế Modding của Timberborn thông qua tệp `manifest.json` và thư mục `Localizations/`.
  - Tệp dịch Việt hóa chuẩn hóa `viVN.csv` chứa toàn bộ từ vựng công trình, chủng tộc hải ly, thanh nhu cầu, hàng hóa gỗ và các sự kiện mùa hạn hán/nước độc.
  - Tích hợp công cụ tự động kiểm tra `check_loc.py` để đối chiếu từ vựng giữa `enUS.csv` và `viVN.csv`.

### 📁 Cấu Trúc Thư Mục:
```text
mod-game/Timberborn/
├── Mods/
│   ├── VietnameseLanguage/
│   │   ├── manifest.json                  # Tệp khai báo thông tin Mod Timberborn
│   │   ├── check_loc.py                   # Script đối chiếu kiểm tra key dịch
│   │   └── Localizations/
│   │       ├── viVN.csv                   # Tệp dịch Tiếng Việt chuẩn của game
│   │       ├── viVN_names.csv             # Danh sách tên gọi chuẩn
│   │       └── enUS.csv                   # Tệp đối chiếu Tiếng Anh gốc
│   ├── VietnameseLanguage_Mod.zip         # Gói Mod nén sẵn để cài đặt
│   └── enUS_Original.zip                  # Gói ngôn ngữ gốc dự phòng
└── Original_Localizations/                # Toàn bộ tệp ngôn ngữ gốc của game
```

---

## 🚀 Hướng Dẫn Git & Đẩy Lên GitHub:

Để đẩy toàn bộ bộ mod này lên Repository của bạn trên GitHub, hãy chạy các lệnh sau trong terminal:

```bash
cd /d D:\mod-game
git remote add origin <URL-Repository-GitHub-Cua-Ban>
git branch -M main
git push -u origin main
```
