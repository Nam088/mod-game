# CẨM NANG & QUY TẮC DỊCH THUẬT CHI TIẾT CHO AGENT (WorldBox Translation Rules)

Chào Agent! Đây là bộ quy tắc và cẩm nang kỹ thuật dịch thuật chi tiết nhất dành cho dự án Việt hóa game WorldBox. Hãy đọc kỹ và tuân thủ tuyệt đối từng bước.

---

## 🎯 1. Nguyên Tắc Dịch Thuật Cốt Lõi (Core Translation Philosophy)

### A. Định Dạng Văn Bản & Font Chữ (Unicode NFC)
* **BẮT BUỘC sử dụng bảng mã dựng sẵn (Unicode NFC)**:
  * Tránh lỗi font hiển thị trong game.
  * Đúng: `ề` (U+1EC1), `ả` (U+1EA3).
  * Sai (tổ hợp): `ê` + `̀` = `ề`.

### B. Bảo Toàn Biến Số & Thẻ Định Dạng (Variables & Tags Protection)
* **Giữ nguyên biến số dạng `$key$`**:
  * Các biến số này được game tự động chèn dữ liệu thực tế (như tên nhân vật, số lượng).
  * Ví dụ: `$name$ has died` -> `$name$ đã hy sinh` (Giữ nguyên `$name$`).
  * Ví dụ: `$killer$ killed $name$` -> `$killer$ đã tiêu diệt $name$`.
* **Giữ nguyên thẻ định dạng HTML/Unity Rich Text**:
  * Ví dụ: `<color=#FFCC1C>$power$</color>` -> `<color=#FFCC1C>$power$</color>` (Không thay đổi thẻ màu sắc).
* **Ký tự xuống dòng `\n`**:
  * Giữ nguyên vị trí hoặc điều chỉnh sao cho ngắt dòng tự nhiên trong khung thoại game.
  * Ví dụ: `Line 1\nLine 2` -> `Dòng 1\nDòng 2`.

### C. Thuật Ngữ Gaming Thống Nhất (Terminology Glossary)
Để đảm bảo bản dịch nhất quán giữa các file, hãy sử dụng bảng thuật ngữ chuẩn dưới đây:
* **Sapient / Sapient beings** -> Sinh vật có nhận thức (hoặc Chủng tộc văn minh).
* **Biome** -> Quần xã sinh vật (hoặc Thảm thực vật).
* **Trait** -> Đặc tính.
* **Kingdom** -> Vương quốc.
* **Settlement / Village** -> Ngôi làng (hoặc Khu định cư).
* **Tribute** -> Cống vật / Cống nạp (triều đình thu từ các làng).
* **Tax** -> Thuế địa phương (làng thu từ dân).
* **Monolith** -> Phiến đá cổ (Monolith).
* **Cursed / Blessing** -> Bị nguyền rủa / Ban phước.
* **Age (World Age)** -> Kỷ nguyên.

---

## 📝 2. Ví Dụ Thực Tế Trước & Sau Khi Dịch (Concrete JSON Examples)

### Ví dụ 1: Chứa biến số và thẻ màu
* **Gốc (English)**:
  ```json
  "unlock_powers_description_any": "Watch a video and unlock <color=#FF9B1C>$power$</color> for <color=#FF9B1C>$minutes$</color> minutes!"
  ```
* **Dịch chuẩn (Vietnamese)**:
  ```json
  "unlock_powers_description_any": "Xem một đoạn quảng cáo ngắn để mở khóa quyền năng <color=#FF9B1C>$power$</color> trong vòng <color=#FF9B1C>$minutes$</color> phút!"
  ```

### Ví dụ 2: Chứa ký tự xuống dòng `\n`
* **Gốc (English)**:
  ```json
  "ad_error_description": "- No ad available\n- No internet\n- Or an error happened"
  ```
* **Dịch chuẩn (Vietnamese)**:
  ```json
  "ad_error_description": "- Không có quảng cáo khả dụng\n- Không có kết nối mạng\n- Hoặc đã xảy ra lỗi hệ thống"
  ```

---

## 📂 3. Cấu Trúc Thư Mục & Phân Tách Git

Do Git được cấu hình ẩn thư mục `extracted_locales/` để tránh làm rác lịch sử commit, bạn phải xử lý thủ công các tệp tin dịch:
* **Khi bắt đầu dịch một file mới** (Ví dụ: `world_ages.json`):
  1. Đọc nội dung tiếng Anh gốc tại: `extracted_locales/en/world_ages.json`.
  2. Tạo/Mở file tiếng Việt tại: `extracted_locales/vn/world_ages.json` và dịch.
  3. Sau khi hoàn thành và kiểm tra thành công, bạn **PHẢI** force add file đó vào Git trước khi commit:
     ```bash
     git add -f extracted_locales/vn/world_ages.json
     ```

---

## 🛠 4. Quy Trình 5 Bước Làm Việc Của Agent (Step-by-Step Workflow)

Hãy thực hiện tuần tự 5 bước dưới đây cho mỗi tệp tin dịch thuật:

### Bước 1: Nghiên Cứu Baseline
* Đọc file English tương ứng để hiểu ngữ cảnh, số lượng key, cấu trúc biến số.

### Bước 2: Dịch thuật & Ghi đè
* Tiến hành dịch thuật kỹ lưỡng. Ghi đè nội dung dịch vào file tương ứng trong thư mục `extracted_locales/vn/`.

### Bước 3: Chạy Kiểm Thử Tự Động (BẮT BUỘC)
* Chạy công cụ kiểm thử chất lượng:
  ```bash
  python verify_translation.py
  ```
* **Yêu cầu**: Kết quả trả về phải báo `✅ VERIFICATION PASSED`.
* Nếu báo lỗi `Missing` (Thiếu key) hoặc `Extra` (Thừa/Sai key), hãy sửa lại file JSON ngay lập tức và chạy lại bước 3.

### Bước 4: Đóng Gói & Cài Đặt (Merge & Install)
* Đóng gói toàn bộ bản dịch và chép đè vào thư mục mod hoạt động của game:
  ```bash
  python merge_and_copy.py
  ```

### Bước 5: Commit Git
* Thêm file dịch vào hàng chờ của Git và thực hiện commit gọn gàng:
  ```bash
  git add -f extracted_locales/vn/ten_file.json
  git commit -m "translate ten_file.json"
  ```

---

## 🚨 5. Xử Lý Sự Cố (Troubleshooting)

### A. Lỗi "VERIFICATION FAILED"
* **Nguyên nhân**: Bạn đã lỡ tay xóa mất một key nào đó trong lúc dịch, hoặc gõ sai tên key khiến cấu trúc lệch so với bản tiếng Anh.
* **Cách sửa**: Xem danh sách `Missing keys` hoặc `Extra keys` do script liệt kê trong terminal. Tìm lại key đó trong file English gốc, bổ sung lại vào file tiếng Việt rồi chạy lại `verify_translation.py`.

### B. Lỗi không hiển thị tiếng Việt trong game
* **Nguyên nhân**: File `vi.json` trong thư mục mod của game chưa được cập nhật hoặc mod C# chưa được nạp.
* **Cách sửa**:
  1. Đảm bảo đã chạy thành công `python merge_and_copy.py`.
  2. Vào game, kiểm tra xem đã bật **Experimental Mode (Chế độ thử nghiệm)** trong phần cài đặt của WorldBox chưa (Modloader chỉ chạy khi bật chế độ này).
