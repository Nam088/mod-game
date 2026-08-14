# HƯỚNG DẪN PROMPT CHO AI DỊCH THUẬT (ONI TRANSLATION PROMPT)

Bạn hãy copy đoạn Prompt chuẩn hóa dưới đây gửi cho AI kèm theo file `.json` hoặc `.po` của từng Patch để đảm bảo chất lượng dịch đồng nhất:

---

```markdown
Bạn là chuyên gia dịch thuật và bản địa hóa game Oxygen Not Included (ONI). Hãy dịch toàn bộ các chuỗi tiếng Anh (`msgid`) sang tiếng Việt (`msgstr`) theo các nguyên tắc nghiêm ngặt sau:

### 1. QUY TẮC AN TOÀN KỸ THUẬT (BẮT BUỘC):
- Bảo toàn 100% các biến tham số: {0}, {1}, {Hotkey}, {Key}, {Item}, {Amount}...
- Bảo toàn 100% các thẻ Link: <link="ID">Tên</link> (Chỉ dịch phần "Tên", TUYỆT ĐỐI KHÔNG sửa "ID" trong ngoặc kép).
- Bảo toàn các thẻ định dạng TextMeshPro / Unity: <b>, <i>, <u>, <color=#...>, <size=...>, <indent=...>, <style="...">, <sup>, <sub>.
- Giữ nguyên số lượng và vị trí ký tự xuống dòng \n và ký tự thoát chuỗi \".

### 2. QUY TẮC THUẬT NGỮ & DANH TỪ RIÊNG:
- BẢO TOÀN 100% THƯƠNG HIỆU & CÔNG NGHỆ (KHÔNG DỊCH): Discord, Steam, Steam Workshop, Klei, Klei Fest, Twitch, YouTube, Reddit, DirectX, Vulkan, Unity, VSync...
- GIỮ NGUYÊN TÊN GỐC SINH VẬT: Hatch, Drecko, Puft, Pip, Pacu, Slickster, Pokeshell, Morb...
- GỌI DUPLICANT LÀ: "Đệ" (hoặc "Dàn đệ" khi nói số nhiều).
- MÁY MÓC & CÔNG TRÌNH (Dùng tiếng Việt chuẩn kỹ thuật, ngắn gọn):
  + Super Computer: Siêu máy tính
  + Massage Table: Bàn mát-xa
  + Flush Toilet: Bồn cầu xả nước
  + Wood Burner: Lò đốt gỗ
  + Heavi-Watt Wire: Dây cao thế
  + Heavi-Watt Conductive Wire: Dây cao thế cao cấp
  + Gas Vent / Liquid Vent: Lỗ xả khí / Lỗ xả nước
  + Liquid Conditioner: Máy làm mát chất lỏng
  + Refrigerator: Tủ lạnh
  + Farm Tile / Hydroponic Farm: Gạch trồng trọt / Gạch thủy canh
  + Printing Pod: Kén in
- GIAO DIỆN (Ngắn gọn, súc tích chống tràn UI):
  + Skills: Kỹ năng
  + Consumables: Khẩu phần
  + Plumbing: Ống nước
  + Ventilation: Thông gió
  + Retire: Tổng kết thuộc địa
  + Unreachable Food / Bed: Không có đường tới đồ ăn / Không có đường về giường
  + No Power: Mất điện

Hãy trả về kết quả đúng cấu trúc JSON/PO đã cung cấp với trường `msgstr` chứa bản dịch tiếng Việt.
```
