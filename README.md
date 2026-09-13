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

## 🏰 4. Going Medieval (`mod-game/Going-Medieval`)

### 📌 Giới Thiệu Game:
**Going Medieval** là tựa game mô phỏng quản lý sinh tồn, xây dựng lâu đài và thuộc địa Trung Cổ 3D thời kỳ hậu dịch hạch 1346. Người chơi lãnh đạo những người sống sót khai hoang, xây dựng pháo đài nhiều tầng với hệ thống vật lý chịu lực (Stability), phân công lao động, quản lý tâm lý, tín ngưỡng tôn giáo và phòng thủ trước các đợt tấn công của thổ phỉ.

### 🛠️ Chi Tiết Mod Việt Hóa:
- **Tình trạng dịch**: Đang tiến hành bản địa hóa toàn diện **8,877 keys** chuẩn hóa theo cấu trúc Mod I2 Localization.
- **Tính năng nổi bật**:
  - Cấu trúc Mod chính thức nạp trực tiếp qua `Mods/VietnameseLocalization/Data/Localization/Vietnamese.csv` và `ModInfo.json`.
  - Tách dữ liệu thành 7 tệp JSON phân hệ trong `translations/` để kiểm soát chất lượng dịch thuật.
  - Bộ công cụ hoàn chỉnh: `verify_translation.py` (thẩm định cú pháp RichText, biến số, độ dài UI), `export_csv_mod.py` (biên dịch CSV) và `deploy_to_game.py` (hot-deploy 1-click vào thư mục cài đặt game).




---

## 🐭 5. Whiskerwood (`mod-game/Whiskerwood`)

### 📌 Giới Thiệu Game:
**Whiskerwood** là tựa game mô phỏng xây dựng thành phố, sinh tồn và tự động hóa chuỗi cung ứng logistics cơ khí hơi nước trong thế giới ngụ ngôn loài chuột thời kỳ Victoria (Unreal Engine 5). Người chơi vào vai Trưởng Làng, lãnh đạo bầy chuột tha hương khai hoang quần đảo hoang sơ, xây dựng hệ thống băng tải, máng trượt, sưởi ấm mùa đông và chống chọi trước sự cai trị bóc lột của loài Mèo (Phe Móng Vuốt).

### 🛠️ Chi Tiết Mod Việt Hóa:
- **Tình trạng dịch**: **100% Hoàn thành (2,751 keys - Đạt chuẩn Blind QA Tier S 9.1/10)**.
- **Tính năng nổi bật**:
  - Bản dịch thuần Việt 100%, tuân thủ nghiêm ngặt quy chuẩn sinh thái loài chuột (Mouse Ecology Lore): loại bỏ hoàn toàn từ ngữ loài người ("người làm", "người dân" ➔ "cư dân chuột", "chuột thợ", "đồng loại", "bầy chuột").
  - Chuẩn hóa toàn bộ hệ thống cơ khí & logistics: *Băng Chuyền, Máng Trượt, Phễu Nạp, Bệ Phóng/Bắn Hàng, Tháp Sàng, Nồi Hơi*.
  - Chuyển ngữ đầy đủ toàn bộ thư từ nhiệm vụ cốt truyện Hồi I & Hồi II, đối phó áp bức thu thuế của Công Tước Mèo Micalico và cuộc khởi nghĩa của Stormie.
  - Định dạng Standalone PAK Mod (`Whiskerwood-Vietnamese_P.pak`), tích hợp sẵn font tiếng Việt UE5, cài đặt cực nhanh chỉ bằng cách copy vào thư mục `Content\Paks\~mods\`.
  - Bộ công cụ hoàn chỉnh: `verify_translation.py`, `uasset_patcher.py` và `build_and_deploy_mod.py`.

---

## 👑 6. Manor Lords (`mod-game/Manor-Lords`)

### 📌 Giới Thiệu Game:
**Manor Lords** là tựa game chiến thuật thời gian thực kết hợp xây dựng thành phố thời Trung Cổ thế kỷ 14 cực kỳ chân thực trên nền tảng Unreal Engine 5.5. Game mô phỏng chi tiết đời sống nông thôn, lưới đường tự do, canh tác luân canh mùa vụ và các trận đại chiến quy mô lớn.

### 🛠️ Chi Tiết Mod Việt Hóa:
- **Tình trạng dịch**: Dự án bản địa hóa chuyên sâu theo chuẩn cấu trúc DataTable UAsset của Unreal Engine 5.5.
- **Tính năng nổi bật**:
  - Trích xuất và patch trực tiếp chuỗi bản dịch vào DataTable nhị phân của game.
  - Tích hợp bộ công cụ chuyển đổi DataTable, đóng gói `repak.exe` và kiểm định cú pháp.

---

## 🧪 7. Oxygen Not Included (`mod-game/Oxygen-Not-Included`)

### 📌 Giới Thiệu Game:
**Oxygen Not Included** là tựa game mô phỏng quản lý không gian và thuộc địa sinh tồn trên tiểu hành tinh vũ trụ nổi tiếng của Klei Entertainment. Người chơi phải điều phối các nhân bản (Duplicants) khai khoáng, xây dựng mạng lưới điện, khí oxy, nước, nhiệt động lực học và chuỗi thức ăn để sinh tồn trong lòng tiểu hành tinh.

### 🛠️ Chi Tiết Mod Việt Hóa:
- **Tình trạng dịch**: Bản mod ngôn ngữ chuẩn hóa theo cơ chế Localization của Klei.
- **Tính năng nổi bật**:
  - Bản dịch tiếng Việt chuẩn ngữ pháp và thuật ngữ khoa học vật lý, hóa học, nhiệt động học.
  - Tích hợp cấu trúc phát hành qua file PO/strings và đóng gói phân phối độc lập.

---

## 🚀 Hướng Dẫn Git & Đẩy Lên GitHub:

Để đẩy toàn bộ bộ mod này lên Repository của bạn trên GitHub, hãy chạy các lệnh sau trong terminal:

```bash
cd /d D:\code\mod-game
git remote add origin <URL-Repository-GitHub-Cua-Ban>
git branch -M main
git push -u origin main
```

