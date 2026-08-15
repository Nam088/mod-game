# 📜 QUY TẮC & TRIẾT LÝ DỊCH THUẬT GAME MODDING (TRANSLATION RULES)

Tài liệu này là bộ quy chuẩn bắt buộc mà AI Assistant / Agent phải tuân thủ nghiêm ngặt trong suốt quá trình Việt hóa các tựa game quản lý, mô phỏng và chiến thuật (Oxygen Not Included, Timberborn, Against The Storm, WorldBox, v.v.).

---

## 🎯 1. Triết Lý & Văn Phong Dịch Thuật

1. **Thuần Việt, Tự Nhiên & Dễ Hiểu (Player-First Localization):**
   - Không dịch máy móc thô cứng kiểu "word-by-word" từ Google Translate.
   - Sử dụng ngôn từ giàu tính hình tượng, gần gũi và hài hước đúng tinh thần của tựa game.
   - Câu cú gãy gọn, văn phong thoát ý, chuẩn ngữ pháp tiếng Việt.

2. **Dung Hòa Giữa Thuật Ngữ Việt Hóa & Thuật Ngữ Gốc (Hybrid Naming):**
   - **Đối với Sinh Vật / Nhân Vật Độc Quyền (Critters / Unique Beings):** Ưu tiên cấu trúc `[Tên Tiếng Việt Gợi Hình] ([Tên Tiếng Anh Gốc])` (Ví dụ: `Bọ Ăn Đá (Hatch)`, `Thằn Lằn Lông Sợi (Drecko)`, `Sóc Đất Trồng Cây (Pip)`). Giúp người chơi mới hiểu ngay công dụng, người chơi cũ vẫn dễ dàng tra cứu Wiki quốc tế.
   - **Đối với Cây Trồng, Thực Phẩm & Tài Nguyên (Plants, Food, Elements):** Ưu tiên **Thuần Việt 100%** (Ví dụ: `Cây Bột Trùng`, `Cây Băng Hàn`, `Dây Leo Muối`, `Đất Bẩn`, `Nước Bẩn`, `Khí CO2`).
   - **Đối với Menu Xây Dựng & Nút Bấm UI (Build Menu & Buttons):** Đặt tên **ngắn gọn tối đa (1 – 2 từ)** để tránh tràn viền giao diện (Ví dụ: `Căn Cứ`, `Oxy`, `Điện`, `Cấp Nước`, `Ống Khí`, `Nội Thất`, `Tinh Chế`, `Y Tế`, `Tự Động`).

---

## 🛡️ 2. Bảo Toàn Cú Pháp Kỹ Thuật (Technical Integrity)

1. **Giữ Nguyên 100% Thẻ Link & Code Tags:**
   - Tuyệt đối không thay đổi, không dịch và không làm sai lệch ID bên trong các thẻ liên kết game:
     - Đúng: `<link="HATCH">Bọ Ăn Đá (Hatch)</link>`
     - Sai: `<link="BO_AN_DA">Bọ Ăn Đá</link>` hoặc `<link="HATCH">Bọ Ăn Đá` (quên đóng thẻ).
2. **Bảo Toàn Placeholder & Biến Số (Variables):**
   - Giữ nguyên các biến số hệ thống như `{0}`, `{1}`, `{Hotkey}`, `{Name}`, `{Amount}`, `{Percent}`.
3. **Đồng Bộ Thẻ Định Dạng Rich Text / HTML:**
   - Các thẻ trang trí như `<b>`, `<i>`, `<color=#...>`, `<style="...">`, `<smallcaps>`, `<indent=...>` phải có thẻ đóng mở đầy đủ và khớp chính xác với chuỗi gốc.
4. **Chuẩn Hóa Ký Tự Xuống Dòng (`\n`):**
   - Số lượng ký tự xuống dòng thực tế giữa các đoạn văn phải tương ứng chính xác với file gốc của Klei / Eremite / Re-Logic.

---

## 🔍 3. Quy Trình Kiểm Định Bắt Buộc Trước Khi Phát Hành

Mỗi khi chỉnh sửa file dịch, Agent PHẢI thực hiện đầy đủ 3 bước kiểm tra:
1. **Chạy Script Thẩm Định Kỹ Thuật:** Đảm bảo **0 Lỗi Placeholder, 0 Lỗi Link Tags, 0 Lỗi Rich Text**.
2. **Kiểm Tra Tràn Viền Giao Diện (UI Overflows):** Rút gọn các chuỗi văn bản dài hơn 1.8 lần chuỗi gốc trên thanh menu hoặc nút bấm.
3. **Đồng Bộ Với Bách Khoa Toàn Thư (Codex / Wiki Trong Game):** Mọi tên gọi trong thế giới game phải khớp 100% với tiêu đề bài viết trong thư viện Codex tra cứu.
