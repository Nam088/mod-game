---
name: manor-lords-localization-workflow
description: >-
  Hướng dẫn và phương pháp luận dịch thuật/bản địa hóa Manor Lords (Unreal Engine 5.5).
  Kích hoạt khi AI thực hiện dịch thuật các DataTable JSON, xử lý font chữ UE5,
  kiểm tra cú pháp rich text thẻ icon/highlight, hoặc biên dịch binary mod cho Manor Lords.
---

# Manor Lords Localization Workflow & Rule Guide

Tài liệu này là **kim chỉ nam toàn diện về quy chuẩn dịch thuật, kỹ thuật Unreal Engine 5.5 và phương pháp luận bản địa hóa** cho tựa game chiến thuật thời trung cổ **Manor Lords**.

---

## 1. Bối Cảnh Lịch Sử & Văn Phong (Context & Tone of Voice)

Manor Lords lấy bối cảnh **Châu Âu thế kỷ 14 (Đế chế La Mã Thần thánh / Franconia)** với lối chơi xây dựng lãnh địa, quản lý nông nô, thuế khóa và chiến trận trung cổ thực tế.

- **Văn phong tổng thể:** Trầm ấm, cổ phong trung cổ vừa phải nhưng dễ hiểu cho người chơi hiện đại. Không dùng từ Hán-Việt tối nghĩa hay phong cách tiên hiệp/kiếm hiệp.
- **Tôn giáo & Lãnh địa:** Theo chuẩn thuật ngữ Công giáo & Phong kiến Tây Âu:
  - `Shrine` ➔ **Đền thánh** / **Khám thờ** (tránh dịch là "Miếu thờ" mang phong cách Á Đông).
  - `Burgage Plot` ➔ **Nhà dân** / **Đất chia lô**.
  - `Lord` / `Baron` ➔ **Lãnh chúa** / **Nam tước**.
  - `Retinue` ➔ **Đội cận vệ**.
  - `Militia` ➔ **Dân quân**.
  - `Garrison Space` ➔ **Chỗ đóng quân**.
  - `Treasury` ➔ **Ngân khố**.
  - `Influence` ➔ **Uy danh**.
  - `Regional Wealth` ➔ **Tài sản Vùng**.
  - `Ale` ➔ **Bia mạch nha** (hoặc Bia Ale).
  - `Gambeson` ➔ **Áo giáp vải** (giáp chần bông trung cổ).
  - `Mail Armor` ➔ **Giáp xích**.
  - `Plate Armor` ➔ **Giáp tấm**.

---

## 2. Quy Tắc Cú Pháp Bất Biến (Rich Text & Tag Invariants)

Unreal Engine 5 sử dụng bộ parser Rich Text đặc thù. Khi dịch JSON trong `Manor-Lords/translations/`, AI **BẮT BUỘC** tuân thủ các quy tắc sau:

### 2.1. Quy tắc khoảng trắng giữa các thẻ (Critical):
- **Phải luôn có dấu cách** giữa thẻ đóng tự đóng `<img ... />` và thẻ `<h>` mở:
  - ❌ `SAI`: `<img id="stable"/><h>Chỗ chuồng</>` (sẽ gây lỗi parser, in literal chữ `<h>` ra màn hình)
  - ✅ **ĐÚNG**: `<img id="stable"/> <h>Chỗ chuồng</>`
- **Phải có dấu cách** giữa chữ thường và thẻ mở `<img...>`:
  - ❌ `SAI`: `tiêu thụ<img id="Food"/>`
  - ✅ **ĐÚNG**: `tiêu thụ <img id="Food"/>`
- **Phải có dấu cách** giữa thẻ đóng `</>` và từ tiếp theo (trừ dấu câu):
  - ❌ `SAI`: `<h>Lãnh chúa</>và quân đội`
  - ✅ **ĐÚNG**: `<h>Lãnh chúa</> và quân đội`

### 2.2. Chuẩn hóa tên thẻ:
- Thẻ highlight: `<h>Nội dung</>` (viết thường chữ `h`, không viết `<H>`).
- Thẻ in nghiêng: `<i>Nội dung</i>` hoặc `<i>Nội dung</>`.
- Thẻ màu đỏ / cảnh báo: `<r>Nội dung</r>` hoặc `<r>Nội dung</>`.
- Thẻ xuống dòng: `{br}` (giữ nguyên).
- Không tự ý dịch `id` bên trong thẻ `<img id="ItemID_12"/>`.

---

## 3. Kiến Trúc Kỹ Thuật & Build Pipeline

Manor Lords lưu trữ text dịch trong 39 file binary `DataTable` thuộc đường dẫn:
`ManorLords/Content/Translation/HoodedHorse/DT_Translation_*.uasset`

### 3.1. Biên dịch Binary (DataTableConverter):
- Công cụ C# `tools/DataTableConverter` chịu trách nhiệm patch trực tiếp `FString` (UTF-16 LE) vào binary UE5.5.
- Cấu trúc FString:
  - Tiếng Anh (ASCII): `Length > 0`, byte 8-bit + null-terminator `0x00`.
  - Tiếng Việt (Unicode): `Length = -charCount`, byte 16-bit UTF-16 LE + null-terminator `0x00 0x00`.

### 3.2. Quản lý Font Chữ (No-Italics Policy):
- Game mặc định dùng các font `Alegreya`, `Favarotta`, `SairaCondensed`, `RobotoCondensed`.
- **Chính sách font:** Toàn bộ text tiếng Việt sử dụng font đứng thẳng (**Alegreya Medium 500** hoặc Regular 400).
- Không inject file font `Italic` hoặc `Italic=true` metadata để tránh chữ bị nghiêng/xô lệch trong UI.
- Thư mục build fonts luôn được dọn dẹp (`clean`) trước khi đóng gói `.pak`.

---

## 4. Quy Trình Làm Việc Chuẩn (Workflow Steps)

1. **Chỉnh sửa / Cập nhật dịch thuật:**
   - Sửa nội dung trường `"vi"` trong các file JSON tại `Manor-Lords/translations/`.
   - Giữ nguyên `"key"`, `"en"`, `"offset"`, `"length"`.
2. **Kiểm tra cú pháp thẻ:**
   - Chạy script kiểm tra cú pháp tag để đảm bảo không bị dính thẻ `<img .../> <h>`.
3. **Biên dịch & Đóng gói Mod:**
   - Chạy `python build_and_deploy_mod.py`.
   - Script sẽ tự động:
     1. Chạy `DataTableConverter` (Release mode) để compile 39 DataTables sang binary.
     2. Tải/Inject font Alegreya tiếng Việt đứng thẳng.
     3. Gọi `repak` để đóng gói thành `pakchunk99-Vietnamese_P.pak`.
     4. Tự động copy vào thư mục game `~mods`.
4. **Deploy & Kiểm thử:**
   - Kiểm tra UI game thực tế, quan sát hiển thị icon, độ đậm/nghiêng của font chữ và độ mượt mà của câu văn.
