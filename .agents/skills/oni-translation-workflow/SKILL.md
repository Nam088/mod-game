---
name: oni-translation-workflow
description: >-
  Hướng dẫn và phương pháp luận dịch thuật/bản địa hóa Oxygen Not Included (ONI).
  Kích hoạt khi AI thực hiện dịch các file PO, JSON batch, dịch UI, công trình, sinh vật,
  trang phục, thế giới, hoặc chạy script thẩm định bản dịch.
---

# ONI Translation Agent Guide & Methodology

Tài liệu này là **kim chỉ nam toàn diện về phương pháp luận và kỹ thuật** để AI thực hiện dịch thuật và bản địa hóa game Oxygen Not Included một cách tự động, chuẩn xác và linh hoạt cho mọi loại nội dung (PO, JSON batch, UI, Lore, Blueprints, Dialogues).

---

## 1. Tư Duy Phân Loại Ngữ Cảnh (Context Understanding)

Khi nhận một chuỗi (`msgid`) kèm mã định danh (`msgctxt`), AI phải xác định mục đích sử dụng trong game để áp dụng chiến lược dịch tương ứng:

```
                  ┌── [UI/HUD] ─────────────► Ngắn gọn, dứt khoát, chống tràn viền (<1.8x)
                  ├── [BUILDINGS/TECH] ─────► Thuật ngữ kỹ thuật/khoa học chính xác, cô đọng
                  ├── [BLUEPRINTS/OUTFIT] ──► Giữ nét văn hóa/thời trang, sáng tạo, hoa mỹ
msgctxt / Key ───┼── [CREATURES/PLANTS] ───► Tên loài sinh thái sống động, giữ tên gốc sinh vật
                  ├── [ELEMENTS/MATERIALS] ─► Danh pháp hóa học/vật liệu trực quan
                  ├── [WORLDS/ASTEROIDS] ───► Giữ tên riêng thế giới, dịch mô tả sinh tồn
                  └── [FLAVORTEXT/LORE] ────► Giữ tính châm biếm, hài hước đặc trưng của Klei
```

### Chiến lược dịch theo nhóm context:
- **`STRINGS.UI.*`**: Nút bấm, tab, tiêu đề. Ưu tiên từ ghép ngắn (1-3 từ), không đưa từ giải thích dài dòng.
- **`STRINGS.BUILDINGS.*`**: Công trình, máy móc. Chỉ dịch tên đồ vật/thiết bị, không đưa tính năng/công dụng vào tên.
- **`STRINGS.BLUEPRINTS.*`**: Trang phục, đồ trang trí. Dịch thoát nghĩa để tạo cảm giác thẩm mỹ thời trang, giữ chất chơi chữ.
- **`STRINGS.CREATURES.*`**: Sinh vật, hạt giống, phân loài. Giữ nguyên tên giống loài gốc (`Hatch`, `Drecko`, `Puft`, `Pip`, `Pacu`, `Slickster`, `Pokeshell`, `Morb`...).
- **`STRINGS.ELEMENTS.*`**: Khí, chất lỏng, quặng rắn. Dùng danh pháp hóa học thông dụng (Oxy, Hydro, Khí clo, Nước bẩn, Than chì...).
- **`STRINGS.WORLDS.*`**: Tiểu hành tinh và cụm thiên thể. Giữ nguyên tên riêng (`Terra`, `Arboria`, `Verdante`, `Rime`, `Oasisse`...) để người chơi dễ tra cứu wiki / tài liệu quốc tế.

---

## 2. Ràng Buộc Kỹ Thuật & Cú Pháp Bất Biến (Technical Invariants)

Trước khi xuất bất kỳ chuỗi dịch nào, AI phải tự kiểm tra 12 quy tắc an toàn hệ thống. Danh sách đầy đủ (placeholders, link tags, rich text tags, escape sequences, khoảng trắng đầu/cuối, đơn vị đo, thương hiệu, chống tràn UI, viết hoa/thường, dấu gạch chéo, định danh sinh vật, chuỗi rỗng) nằm tại [technical-invariants.md](./references/technical-invariants.md).

Ba quy tắc hay bị bỏ sót nhất, cần nhớ ngay khi đọc chuỗi:
- **Quy tắc 1, 2, 3:** không đổi placeholder `{...}`, không đổi `TARGET_ID` trong `<link="...">`, số thẻ rich text mở phải bằng số thẻ đóng.
- **Quy tắc 8:** chuỗi UI dịch tối đa 1.8 lần độ dài gốc.
- **Quy tắc 11:** tên sinh vật giữ nguyên tiếng Anh, kèm chú thích trong ngoặc đơn (chi tiết tại [glossary.md](./references/glossary.md)).

---

## 3. Phong Cách & Văn Phong Bản Địa Hóa (Tone, Voice & Grammar)

- **Xưng hô nhân vật trung tâm:** Luôn dịch `Duplicant(s)` thành **`Đệ`** / **`Các Đệ`** (văn phong thân thuộc, độc đáo của cộng đồng ONI Việt Nam).
- **Hài hước & Châm biếm (Flavortext):** Các câu châm biếm của Klei trong mô tả đồ vật/công trình cần dịch thoát nghĩa, tự nhiên, hóm hỉnh.
- **Tiếng Việt hiện đại:** Ưu tiên từ ngữ trong sáng, trực quan; tránh dịch thô kiểu "Google Translate" (word-by-word) và tránh lạm dụng từ Hán-Việt cổ.
- **Tính nhất quán (Consistency):** Cùng một danh từ/thuật ngữ trong cùng một chuỗi PO/JSON phải được dịch thống nhất. Tham khảo từ vựng cốt lõi tại [glossary.md](./references/glossary.md).

---

## 4. Quy Trình Thực Thi Dịch Thuật Của AI (Step-by-Step Execution)

Khi thực hiện dịch bất kỳ tập tin nào (PO, JSON batch, script patch):

1. **Bước 1: Trích xuất & Phân tích cấu trúc**
   - Đọc dữ liệu nguồn, tách chuỗi `msgid` và ngữ cảnh `msgctxt`.
   - Phân lập các thẻ `<link="...">`, Rich Text tags và `{placeholders}` bằng Regex trước khi dịch.

2. **Bước 2: Xử lý dịch thuật theo ngữ cảnh**
   - Áp dụng nguyên tắc ngắn gọn cho UI và kỹ thuật cho công trình/vật liệu.
   - Ghép lại các thẻ và biến nguyên bản vào chuỗi tiếng Việt.

3. **Bước 3: Tự động Thẩm Định (Self-Verification Loop)**
   - Kiểm tra chéo:
     - Số lượng placeholders trước và sau khi dịch.
     - Số lượng link tags và rich text tags (`<smallcaps>`, `<b>`, `<i>`...).
     - Ký tự xuống dòng `\n`.
   - Chạy script kiểm tra của dự án (chạy đúng đường dẫn, chạy nhầm file của mod khác sẽ ra kết quả sai vì mỗi mod có script riêng):
     ```bash
     python3 Oxygen-Not-Included/strings/verify_translation.py <đường_dẫn_file>.po
     ```
   - Đọc kết quả báo cáo: nếu phát hiện lỗi hoặc cảnh báo tràn UI, tự động tinh chỉnh lại chuỗi dịch cho đến khi đạt chuẩn hoàn toàn.
   - **Lưu ý phạm vi:** script chỉ tự động kiểm tra placeholder, link tag, số lượng thẻ rich text (không kiểm tra thứ tự lồng nhau), `\n`, và cảnh báo tràn UI cho một danh sách thương hiệu giới hạn. Các quy tắc 5, 6, 9, 10, 11, 12 ở Mục 2 (khoảng trắng đầu/cuối, đơn vị đo, viết hoa/thường, dấu gạch chéo, định danh sinh vật, chuỗi rỗng) không được script kiểm tra tự động, AI vẫn phải tự rà soát thủ công trước khi coi bản dịch là hoàn tất.
