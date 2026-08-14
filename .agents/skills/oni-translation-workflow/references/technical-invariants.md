# ONI Translation Technical Invariants (12 Quy Tắc)

Trước khi xuất bất kỳ chuỗi dịch nào, AI phải tự kiểm tra 12 quy tắc an toàn hệ thống sau.

---

1. **Bảo toàn Placeholders & Biến động (Placeholders & Formatters):**
   - Mọi token dạng `{0}`, `{1}`, `{Hotkey}`, `{Key}`, `{Item}`, `{Amount}`, `{Time}` phải giữ nguyên 100% về số lượng và tên biến.
   - Không được đổi thứ tự hoặc dịch nội dung trong dấu ngoặc nhọn `{}`. Nếu gặp cấu trúc logic mở rộng như `{0:plural:one|many}` hay `{0:gender:he|she|they}`, phải bảo toàn nguyên vẹn cấu trúc cú pháp.
   - Giữ nguyên các ký hiệu phím bấm và nút chuột: `[SPACE]`, `[TAB]`, `[ENTER]`, `[ESC]`, `[LMB]`, `[RMB]`, `[MMB]`.

2. **Bảo toàn Cú Pháp Thẻ Liên Kết (Link Tags):**
   - Cấu trúc: `<link="TARGET_ID">Text To Translate</link>`
   - **Chỉ dịch `Text To Translate`**, giữ nguyên 100% `TARGET_ID` và dấu ngoặc kép. `TARGET_ID` là khóa engine Unity mở Codex bách khoa toàn thư.

3. **Bảo toàn Thẻ Định Dạng Rich Text (HTML / Unity Tags):**
   - Toàn bộ thẻ đóng/mở: `<b>...</b>`, `<i>...</i>`, `<u>...</u>`, `<color=#HEX>...</color>`, `<size=...>...</size>`, `<style=...>...</style>`, `<smallcaps>...</smallcaps>`, `<indent=...>`, `<sup>...</sup>`, `<sub>...</sub>`.
   - Phải bảo đảm số lượng thẻ mở = số lượng thẻ đóng và đúng thứ tự lồng nhau.

4. **Bảo toàn Ký Tự Điều Khiển & Xuống Dòng (Escape Sequences):**
   - Giữ nguyên số lượng và vị trí ký tự `\n` (xuống dòng) và `\t` (tab thụt đầu dòng). Không tự ý gộp đoạn hoặc xóa `\n`.

5. **Bảo toàn Khoảng Trắng Đầu / Cuối (Leading / Trailing Whitespace):**
   - Nếu chuỗi gốc bắt đầu hoặc kết thúc bằng dấu cách `" "` hay dấu chấm/hai chấm `":"`, chuỗi dịch phải giữ nguyên y hệt để tránh dính chữ vào các giá trị số hiển thị cạnh bên.

6. **Bảo toàn Đơn Vị Đo Lường & Hậu Tố Kỹ Thuật (Units & Suffixes):**
   - Giữ nguyên các ký hiệu chuẩn: `kg`, `g`, `mg`, `kDTU/s`, `DTU/s`, `W`, `kW`, `kJ`, `lux`, `rad`, `°C`, `K`, `kcal`.

7. **Bảo toàn Thương Hiệu & Tên Bên Thứ Ba:**
   - Không dịch: `Discord`, `Steam`, `Steam Workshop`, `Klei`, `Klei Fest`, `DirectX`, `OpenGL`, `Vulkan`, `Unity`, `VSync`, `Twitch`, `YouTube`, `Reddit`.

8. **Quy Tắc Chống Tràn Viền Giao Diện (UI Overflow Prevention):**
   - Với chuỗi UI, độ dài tiếng Việt tối đa không vượt quá **1.8 lần** chuỗi tiếng Anh gốc (ngưỡng khớp với `verify_translation.py`).

9. **Quy Tắc Viết Hoa/Thường Đồng Bộ (Case Sensitivity & Capitalization):**
   - Giữ nguyên phong cách viết hoa của chuỗi gốc:
     - Chuỗi gốc viết hoa toàn bộ `ALL CAPS` $\rightarrow$ Bản dịch phải viết hoa toàn bộ `ALL CAPS`.
     - Chuỗi gốc viết hoa đầu từ `Title Case` $\rightarrow$ Bản dịch viết hoa chuẩn `Title Case` hoặc chữ đầu câu.
     - Chuỗi gốc viết thường $\rightarrow$ Bản dịch viết thường.

10. **Không Dùng Dấu Xuyệt Chéo `/` Trong Nhãn Trạng Thái & Cảnh Báo:**
    - Tránh dùng dấu gạch chéo trong nhãn icon trạng thái ngắn (Ví dụ: dịch `Mất điện` thay vì `Mất điện / Thiếu điện`).

11. **Quy Chuẩn Định Danh Sinh Vật (Critter Detailed Naming):**
    - Giữ nguyên tên gốc tiếng Anh của loài, kèm phần giải nghĩa/đặc tính tiếng Việt trong ngoặc đơn dạng **`TênGốc (Chi tiết Tiếng Việt)`** để vừa dễ tra cứu quốc tế vừa trực quan dễ hiểu:
      - Họ Hatch: `Hatch` $\rightarrow$ **`Hatch (Bọ Ăn Đá)`**, `Stone Hatch` $\rightarrow$ **`Stone Hatch (Bọ Ăn Đá Cứng)`**, `Sage Hatch` $\rightarrow$ **`Sage Hatch (Bọ Ăn Rác/Đất Mùn)`**, `Smooth Hatch` $\rightarrow$ **`Smooth Hatch (Bọ Luyện Kim)`**, `Hatchling` $\rightarrow$ **`Hatch Con`** (hoặc `Hatchling (Bọ Con)`).
      - Các loài khác: `Drecko (Thằn Lằn Bò Tường)`, `Pacu (Cá Nhiệt Đới)`, `Pip (Sóc Trồng Cây)`, `Puft (Bóng Khí Lọc Phân)`, `Slickster (Sâu Dầu)`, `Pokeshell (Cua Gai Ra Cát)`... (Chi tiết xem tại [glossary.md](./glossary.md)).

12. **Bảo Toàn Chuỗi Rỗng (Empty Strings) & Ký Hiệu Đơn:**
    - Nếu chuỗi gốc là rỗng `""` hoặc chỉ có ký hiệu toán học (`+`, `-`, `%`, `x`), giữ nguyên không sửa đổi.
