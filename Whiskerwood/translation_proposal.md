# BẢN THIẾT KẾ DỊCH THUẬT & VIỆT HÓA WHISKERWOOD (FINAL STYLE GUIDE)
**Dự án:** Việt hóa Game Whiskerwood (Unreal Engine 5)  
**Công cụ phát triển:** Mod PAK Non-destructive Patching (`Whiskerwood-Vietnamese_P.pak`)  
**Tổng khối lượng:** 2,751 chuỗi văn bản (6 Phân hệ)  

---

## 1. PHÂN TÍCH BỐI CẢNH & TÔNG GIỌNG (LORE & TONE OF VOICE)

*Whiskerwood* mang đậm chất **ngụ ngôn chính trị - xã hội châm biếm sâu cay (tương tự Animal Farm kết hợp chủ nghĩa Thực dân Hàng hải Victoria)**:
* **The Crown (Vương Miện / Đức Vua Mèo):** Đầu não tối cao của Mẫu quốc.
* **The Claws (Quý Tộc Móng Vuốt / Quan Mèo):** Tầng lớp thống trị, quân phiệt, quý tộc Mèo nắm quyền lực tuyệt đối, áp đặt cống nạp và bóc lột.
* **The Tail (Trưởng Quan Đuôi Dài):** Danh xưng con chuột đứng đầu thuộc địa do Mèo dựng lên làm bù nhìn quản lý đám chuột thợ. Bọn Mèo gọi kẻ này một cách khinh miệt lẫn bề trên là "Cái Đuôi" ngoan ngoãn phục tùng.
* **Whiskers / Whiskerkind (Dân Râu Chuột / Họ Nhà Chuột):** Quần chúng chuột cần lao, thợ thuyền, thủy thủ lam lũ, siêng năng trên các hải đảo.

---

## 2. MA TRẬN XƯNG HÔ & HỆ THỐNG NGÔI THỨ ĐÃ THỐNG NHẤT

| Đối tượng / Nhân vật | Ngôi thứ & Danh xưng Tiếng Anh | Thuật ngữ Việt hóa Thống nhất | Ngữ cảnh & Thái độ |
| :--- | :--- | :--- | :--- |
| **Người chơi (Player)** | *Tail / Acting Tail* | **Trưởng Quan Đuôi Dài / Quyền Trưởng Quan Đuôi Dài** | Chức vụ cai quản chuột do triều đình Mèo bổ nhiệm; vừa giữ chữ *Đuôi* biểu tượng, vừa là chức danh trang trọng. |
| **Giai cấp Mèo Thống trị** | *The Claws / The Crown* | **Quý Tộc Móng Vuốt / Triều Đình Móng Vuốt** | Tầng lớp quý tộc thống trị, ban phát ân huệ mỉa mai và đòi cống nạp. Khi dân chuột nói sau lưng: *Quan Mèo*. |
| **Thanh tra Hoàng gia** | *Royal Commissioner / Duke Micalico* | **Khâm Sai Hoàng Gia / Công Tước Micalico** | Viết thư chỉ đạo từ mẫu quốc với giọng điệu trịnh thượng, bề trên. |
| **Cư dân Chuột** | *Whiskers / Colonists* | **Dân Râu Chuột / Cư Dân Chuột** | Tầng lớp lao động, cư dân trên đảo; tính nhân khẩu: *Nhân khẩu chuột*. |
| **Lời kêu gọi chuột** | *Fellow Whiskers* | **Hỡi đồng bào Chuột / Anh em Râu Chuột** | Thân mật, đoàn kết giữa những người cùng cảnh ngộ. |

---

## 3. BẢNG THUẬT NGỮ CỐT LÕI (CORE GLOSSARY)

| Thuật ngữ gốc (EN) | Thuật ngữ Thống nhất (VI) | Giải thích & Định hướng sử dụng |
| :--- | :--- | :--- |
| **Whiskerwood** | **Whiskerwood** (Giữ nguyên tên riêng) | Tên tựa game và tên thuộc địa/vương quốc loài gặm nhấm. |
| **Tax Debt** | **Cống Thuế Hoàng Gia / Định Mức Cống Nạp** | Khoản tài nguyên bắt buộc phải nộp về Mẫu quốc mỗi chu kỳ. |
| **Approval** | **Lòng Dân / Độ Tín Nhiệm** | Thước đo sự ủng hộ của cư dân chuột dành cho Trưởng quan. |
| **Whisker Conveyor** | **Băng Chuyền Cỡ Chuột** | Hệ thống băng tải cơ khí nhỏ gọn chuyên biệt của loài chuột. |
| **Jump Pad** | **Bệ Bật Hàng / Bệ Phóng Kiện Hàng** | Cơ chế dùng lò xo đẩy kiện hàng qua các tầng vách đá cao. |
| **Main Dock** | **Bến Cảng Trung Tâm** | Công trình đầu mối hàng hải quan trọng nhất để xuất khẩu và nộp cống thuế. |
| **Ferry Dock** | **Bến Phà Đảo** | Điểm trung chuyển hàng hóa và thủy thủ giữa các hòn đảo. |
| **Arco Work Ship** | **Thuyền Công Trình Arco** | Thuyền máy hơi nước chuyên dụng phục vụ xây dựng và hậu cần trên biển. |
| **Central Warehouse** | **Kho Tổng Thuộc Địa** | Trung tâm lưu trữ hàng hóa và cống phẩm của đảo. |
| **Aim Lift / Slide** | **Vận Thăng Kiện Hàng / Máng Trượt Kiện Hàng** | Thiết bị vận tải hàng hóa dốc nghiêng và thẳng đứng. |

---

## 4. KẾ HOẠCH PHÂN KỲ DỊCH THEO ĐỢT (PHASING PLAN)

| Đợt dịch | Tệp tin JSON | Khối lượng | Mục tiêu hoàn thành |
| :---: | :--- | :---: | :--- |
| **Đợt 1** | `01_Core_UI_Menus.json` | 391 chuỗi | Việt hóa 100% Giao diện chính, Cài đặt, Thanh công cụ, Tooltip, Nút bấm. |
| **Đợt 2** | `02_Buildings_Logistics.json` | 409 chuỗi | Toàn bộ Công trình, Băng chuyền, Máng trượt, Cảng biển, Kho bãi. |
| **Đợt 3** | `03_Resources_Items_Tech.json` | 350 chuỗi | Cây Công nghệ, Tài nguyên, Thực phẩm, Lương thực, Sách Luật / Chính sách. |
| **Đợt 4** | `04_Mice_Traits_Thoughts.json` | 250 chuỗi | Tính cách, Nghề nghiệp, Tâm trạng, Suy nghĩ của cư dân Chuột. |
| **Đợt 5** | `05_Nautical_Exploration_World.json` | 339 chuỗi | Tàu thuyền, Thời tiết, Mùa màng, Chuyến thám hiểm, Bản đồ đảo. |
| **Đợt 6** | `06_Quests_Events_Story.json` | 1,012 chuỗi | Cốt truyện, Thư từ Khâm sai Mèo, Hướng dẫn (Tutorial), Sự kiện ngẫu nhiên. |
