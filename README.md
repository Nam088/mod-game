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
  - Tích hợp **Plugin C# Dual Font Override** (`AgainstTheStorm_VietnameseMod.dll`): tự động thay thế phông chữ mặc định của game bằng phông chữ **Arial** (UI) và **Georgia** (Tiêu đề & Wiki), khắc phục 100% lỗi phông chữ Tiếng Việt.
  - Chuẩn hóa bộ thuật ngữ gamer (Hearth = *Lò Sưởi*, Resolve = *Ý Chí*, Glade = *Vùng Rừng*, Cornerstone = *Đá Nền*, Blightstorm = *Bão Blight*, Citadel = *Hoàng Thành Tro Tàn*, Prestige = *Prestige*).

---

## 🦫 2. Timberborn (`mod-game/Timberborn`)

### 📌 Giới Thiệu Game:
**Timberborn** là tựa game xây dựng thành phố xã hội loài hải ly độc đáo trong bối cảnh thế giới hậu tận thế con người đã diệt vong. Người chơi điều khiển một trong hai chủng tộc hải ly (Folktails yêu thiên nhiên hoặc Iron Teeth công nghiệp) xây dựng công trình gỗ nhiều tầng, quản lý nguồn nước, đập ngăn nước và chống chọi qua các mùa hạn hán khốc liệt.

### 🛠️ Chi Tiết Mod Việt Hóa:
- **Tình trạng dịch**: Bản mod ngôn ngữ chuẩn hóa cấu trúc **`VietnameseLanguage`**.
- **Tính năng nổi bật**:
  - Cấu trúc Mod chính thức hỗ trợ sẵn cơ chế Modding của Timberborn thông qua tệp `manifest.json` và thư mục `Localizations/`.
  - Tệp dịch Việt hóa chuẩn hóa `viVN.csv` chứa toàn bộ từ vựng công trình, chủng tộc hải ly, thanh nhu cầu, hàng hóa gỗ và các sự kiện mùa hạn hán.
  - Tích hợp công cụ trích xuất Tiếng Anh trực tiếp `export_en_from_game.py` tách riêng các tệp CSV (`enUS.csv`, `enUS_names.csv`...).

---

## 🌍 3. WorldBox (`mod-game/WorldBox`)

### 📌 Giới Thiệu Game:
**WorldBox - God Simulator** là tựa game mô phỏng thần thánh thế giới cát (sandbox god simulator). Người chơi hóa thân thành vị thần tối cao, sáng tạo thế giới, gieo rắc sự sống với các chủng tộc Con Người, Tộc Tiên, Tộc Lùn, Tộc Quỷ Orc, tạo ra các thảm họa thiên nhiên, chiến tranh hoặc xây dựng các đế chế hùng mạnh.

### 🛠️ Chi Tiết Mod Việt Hóa:
- **Tình trạng dịch**: Bản mod Việt hóa toàn diện **WorldBox Vietnamese Mod (Nam088)**.
- **Tính năng nổi bật**:
  - Dịch đầy đủ các giao diện thần thánh, bảng thuộc tính sinh vật, chủng tộc, vũ khí, hiệu ứng phép thuật và bảng thành tựu.
  - Tích hợp bộ script trích xuất `extract_locales.py`, kiểm tra đối chiếu `verify_translation.py` và gộp bản dịch tự động `merge_and_copy.py`.
  - Đóng gói sẵn bản phát hành `WorldBox-Vietnamese-Mod-v1.0.0-Nam088.zip`.

---

## 🚀 Hướng Dẫn Git & Đẩy Lên GitHub:

Để đẩy toàn bộ bộ mod này lên Repository của bạn trên GitHub, hãy chạy các lệnh sau trong terminal:

```bash
cd /d D:\mod-game
git remote add origin <URL-Repository-GitHub-Cua-Ban>
git branch -M main
git push -u origin main
```
