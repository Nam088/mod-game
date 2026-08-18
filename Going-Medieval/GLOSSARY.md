# 🏰 BẢNG THUẬT NGỮ & QUY TẮC DỊCH THUẬT GOING MEDIEVAL (GLOSSARY)

> Đã đối chiếu với dữ liệu thực tế của game (`master_english.json` — 8,877 keys, version 0.20.*). Cập nhật: 2026-08-18.

---

## 1. BỐI CẢNH & TÔNG GIỌNG (TONE OF VOICE)

- **Bối cảnh**: Nước Anh thời kỳ Trung Cổ năm 1346, sau khi Đại Dịch Hạch (Black Death) xóa sổ 95% dân số. Những người sống sót tập hợp lại khai hoang, dựng trại, xây dựng lâu đài và chống lại giặc cướp.
- **Tông giọng (Tone)**: Nghiêm túc, đậm chất Trung Cổ — nhưng **DỄ HIỂU là trên hết**. Giữ không khí lịch sử, sinh tồn nhưng KHÔNG gượng ép, KHÔNG văn chương hóa.
- **Nguyên tắc vàng**:
  - **Dùng từ gần gũi, quen thuộc với người Việt** — ưu tiên từ thuần Việt thay vì từ Hán-Việt trang trọng (VD: *Khỏe mạnh* chứ không phải *Tráng kiện*, *Vui sướng* chứ không phải *Hân hoan*, *Chữa bệnh* chứ không phải *Y thuật*). Game thủ đọc là hiểu ngay, không phải tra từ điển.
  - **Dịch thoát ý, không bám sát nghĩa đen từng từ** — câu tiếng Việt phải xuôi tai, đúng ngữ pháp Việt. Nếu cần, đảo cấu trúc câu hoặc tóm gọn miễn là giữ đủ nghĩa.
  - Không dùng tiếng lóng hiện đại hay văn phong cợt nhả (trừ khi bản EN cũng hài hước — VD: perk "Lord of Misrule").
  - Giữ nguyên **toàn bộ** định dạng kỹ thuật (xem Mục 2 bên dưới).
  - Key UI ngắn (nút, tab, menu): dịch **súc tích** — tiếng Việt dài hơn tiếng Anh, tránh tràn nút.

---

## 2. QUY TẮC KỸ THUẬT BẮT BUỘC (ĐỊNH DẠNG & PLACEHOLDER)

### 2.1. Placeholder dạng `<token>` — game dùng ngoặc nhọn, KHÔNG phải `{0}`
Xuất hiện trong ~900 chuỗi sự kiện/thông báo. **Giữ nguyên y hệt, không dịch, không đổi thứ tự tùy tiện:**

`<name>` (535 lần), `<agent_name>`, `<target_name>`, `<village_name>`, `<faction_name>`, `<defender_name>`, `<attacker_name>`, `<settler_name>`, `<item_name>`, `<origin>`, `<random_villager>`, `<perk_name>`, `<role>`, `<skill_name>`, `<room_type>`, `<age>`, `<year>`, `<other_name>`, `<animal>`, `<event_name>`, `<wealth>`, `<resources>`...

> VD: `The Death of <name> <surname>` → `Cái chết của <name> <surname>`

### 2.2. Token giới tính `[He/She]` — GIỮ NGUYÊN KHÔNG DỊCH
Game tự thay bằng đại từ theo giới tính nhân vật. ~590 chuỗi dùng các biến thể:
`[He/She]`, `[he/she]`, `[his/her]`, `[him/her]`, `[His/Her]`, `[Him/Her]`, `[his/hers]`
và dạng chỉ mục: `#1[he/she]`, `#2[him/her]` (số = nhân vật thứ 1/2 trong câu).

**Quy tắc**: giữ nguyên token, viết câu tiếng Việt sao cho khi game chèn từ tiếng Anh vẫn xuôi. Không tự thay bằng "anh ấy/cô ấy".
> ⚠️ Cần test in-game (Phase 0): kiểm tra token chèn vào giữa câu tiếng Việt hiển thị có chấp nhận được không.

### 2.3. Thẻ RichText — giữ nguyên tên thẻ
- `<style=...>...</style>` với các tên **cố định**: `Shortcut`, `AlmParagraph`, `DefaultRed`, `DefaultOrange`, `DefaultGreen`, `DefaultBlue`, `DefaultYellow`, `AltColor`, `Desc`, `LinkWorker`, `Rebellious`
- `<b>`, `</b>`, `<i>`, `</i>`
- Số lượng `\n` phải khớp với bản EN.

### 2.4. Keys KHÔNG dịch (giữ nguyên 100%)
| Key/Prefix | Số lượng | Lý do |
|---|---|---|
| `DefaultFont`, `TitleFont` | 2 | Asset path của font (có thể đổi sang font hỗ trợ tiếng Việt — test Phase 0) |
| `dev_*` | 595 | Công cụ developer, người chơi thường không thấy |
| `keycode_*` | 113 | Ký tự phím (A, B, Enter, Space...) |

> ⚠️ `verify_translation.py` sẽ đếm các key này là "chưa dịch" — chấp nhận % ảo, không chạy theo số.

---

## 3. BẢNG XƯNG HÔ & ĐẠI TỪ (PRONOUN & HIERARCHY MATRIX)

| Thuật ngữ gốc (EN) | Thuật ngữ dịch (VI) | Ngữ cảnh & Ghi chú |
| :--- | :--- | :--- |
| **Settler / Worker** | **Dân định cư / Dân làng** | Những người sống sót dưới quyền chỉ huy của người chơi. |
| **Settlement / Colony** | **Khu định cư** | Ngôi làng người chơi xây dựng (game dùng lẫn cả "colony"). |
| **Player / You** | **Bạn / Người chơi** | Ngôi thứ hai trong hướng dẫn hoặc thông báo hệ thống. |
| **Bandits / Raiders** | **Thổ phỉ / Kẻ đột kích** | Kẻ thù tấn công khu định cư. |
| **Caravan / Merchant** | **Thương đoàn / Thương nhân** | Đoàn buôn ghé thăm trao đổi hàng hóa. |
| **Faction** | **Phe phái** | Các thế lực lân cận trên bản đồ thế giới. |

### 3.1. Cấp độ kẻ thù (ghép trước danh từ chính, dùng từ tự nhiên)
| Tiền tố (EN) | Dịch (VI) | | Tiền tố (EN) | Dịch (VI) |
| :--- | :--- |---| :--- | :--- |
| Adept | Thành thạo | | Fierce | Hung hãn |
| Master | Bậc thầy | | Ruthless | Tàn nhẫn |
| Illustrious | Khét tiếng | | Brutal | Tàn bạo |
| Monstrous | Gớm ghiếc | | Barbaric | Man rợ |

> VD: `Ruthless Marauder` → *Kẻ cướp bóc tàn nhẫn*, `Adept Archer` → *Cung thủ thành thạo*
> Loại kẻ thù: **Thug** = Côn đồ, **Marauder** = Kẻ cướp bóc, **Archer** = Cung thủ.

### 3.2. Khách đến khu định cư
| EN | VI |
| :--- | :--- |
| Restitutionist Pilgrim | Người hành hương Phục Hưng |
| Oak Brethren Pilgrim | Người hành hương Huynh Đệ Cây Sồi |
| Travelling Scholar | Học giả du hành |
| Broker | Thương lái |
| Lone Traveller | Lữ khách đơn độc |
| Beggar | Kẻ ăn mày |
| Negotiator | Người đàm phán |

### 3.3. Chức vụ (Roles — gán cho dân làng)
| EN | VI | Ghi chú |
| :--- | :--- | :--- |
| Bard | Người hát rong | Kể chuyện, thơ, nhạc. |
| Librarian | Thủ thư | Trông coi thư viện, viết sách. |
| Sergeant-at-arms | Đội trưởng lính gác | Duy trì kỷ luật, thực thi công lý. |
| Chaplain | Linh mục | Chức sắc tôn giáo Restitutionist. |
| Druid | Đạo sĩ | Chức sắc tôn giáo Oak Brethren. |
| Prison Warden | Cai ngục | Trông coi tù nhân, lao động khổ sai. |

---

## 4. THUẬT NGỮ CỐT LÕI (CORE GLOSSARY)

### A. Cơ chế Game & UI
| EN | VI | Giải thích / Ghi chú |
| :--- | :--- | :--- |
| **Stability** | **Độ vững chắc** | Chỉ số vật lý kiến trúc — trần/sàn có đứng vững được không. |
| **Draft / Drafted** | **Huy động / Đã huy động** | Gọi dân làng ra trận chiến đấu. (`Undrafted Stance` = Trạng thái thường) |
| **Urgent Haul** | **Dọn đồ khẩn cấp** | Lệnh ưu tiên nhặt đồ mang về kho ngay lập tức. |
| **Deconstruct** | **Tháo dỡ** | Phá dỡ công trình đã xây. |
| **Manage / Schedule** | **Quản lý / Lịch làm việc** | Phân chia giờ làm việc, ngủ, giải trí. |
| **Almanac** | **Cẩm nang** | Sổ tay tra cứu mọi thứ trong game. |
| **Chronicle** | **Biên niên sử** | Sách nghiên cứu — đơn vị mở khóa công nghệ. |
| **Research Books** | **Sách nghiên cứu** | Tài nguyên nghiên cứu ("Allocated" = *Đã dùng*, "Available" = *Còn trống*). |
| **Impressiveness** | **Độ sang trọng** | Chất lượng phòng (xem thang ở Mục 4C). |
| **Aesthetic Value** | **Giá trị thẩm mỹ** | Chỉ số thẩm mỹ của vật thể / phòng ốc. |
| **Aesthetic Heatmap** | **Bản đồ thẩm mỹ** | Chế độ xem mức độ thẩm mỹ theo màu sắc (Heatmap). |
| **Seal the deal** | **Chốt đơn** | Nút xác nhận trao đổi với thương đoàn. |
| **Barter** | **Trao đổi / Hàng đổi hàng** | Cơ chế giao thương không tiền tệ. |

### A2. Trạng thái tâm lý tổng (Mood thresholds — 6 bậc, dịch theo thang tăng dần, từ đời thường)
| EN | VI |
| :--- | :--- |
| Joyful | Vui sướng |
| Neutral | Bình thường |
| Annoyed | Bực bội |
| Disillusioned | Thất vọng |
| Rebellious | Nổi loạn |
| Broken | Tuyệt vọng |

### B. Tín ngưỡng & Tôn giáo
| EN | VI | Ghi chú |
| :--- | :--- | :--- |
| **Oak Brethren** | **Huynh Đệ Cây Sồi** | Tín ngưỡng thờ phụng Mẹ Thiên Nhiên cổ xưa. |
| **Restitutionist** | **Hội Phục Hưng** | Tôn giáo chính thống thờ Chúa Cứu Thế. |
| **Religious Alignment** | **Xu hướng tín ngưỡng** | Độ mộ đạo của dân làng. |
| **Chaplain / Druid** | **Linh mục / Đạo sĩ** | Xem Mục 3.3. |
| **Shrine** | **Đền thờ** | Công trình thờ cúng nhỏ. |
| **Chapel** | **Nhà nguyện** | Phòng cầu nguyện (`Church of Restitution Chapel` = Nhà nguyện Phục Hưng, `Oak Brethren temple` = Đền Huynh Đệ Cây Sồi). |

> **Quy tắc song song tôn giáo (QUAN TRỌNG)**: game viết mọi hiệu ứng tâm lý thành 2 biến thể:
> - Bản Christian → dùng **Chúa** (số ít): *"God willed this defeat"* → *"Chúa đã định đoạt thất bại này"*
> - Bản Pagan → dùng **chư thần** (số nhiều): *"The Gods allowed this defeat"* → *"Chư thần đã để mặc thất bại này"*
> Luôn giữ cặp song song tương ứng, không trộn lẫn.

### C. Kiến trúc & Phòng ốc (theo dữ liệu game — `room_type_*`)
| EN | VI | Ghi chú |
| :--- | :--- | :--- |
| **Great hall** | **Đại sảnh** | Phòng ăn và hội họp chính. |
| **Chamber** | **Phòng riêng** | Game gọi phòng ngủ riêng là *Chamber* (không dùng Bedroom). |
| **Shared Chamber** | **Phòng chung** | Phòng ngủ tập thể. |
| **`<name>`'s Chamber** | **Phòng của `<name>`** | Giữ token. |
| **Spare room** | **Phòng trống** | Phòng mặc định chưa gán công năng. |
| **Workshop** | **Xưởng chế tác** | Khu vực đặt bàn thợ. |
| **Kitchen** | **Nhà bếp** | Chế biến món ăn. |
| **Library** | **Thư viện** | Nghiên cứu, viết sách. |
| **Infirmary** | **Phòng bệnh** | Chữa trị vết thương, dưỡng bệnh. |
| **Prison Cell** | **Phòng giam** | Giam giữ tù nhân. |
| **Stockpile / Cellar** | **Bãi chứa / Hầm chứa** | Lưu kho và hầm lạnh bảo quản đồ ăn. |
| **Brewery** → game không có room type này; dùng **Brewing** = **Nấu rượu** (sản xuất). | | |

**Thang sang trọng của phòng (Impressiveness — dịch tăng dần đều, không trùng bậc):**
`Awful` = Tồi tệ → `Uninspiring` = Tẻ nhạt → `Modest` = Bình thường → `Good` = Tốt → `Superior` = Đẹp đẽ → `Luxurious` = Sang trọng → `Opulent` = Lộng lẫy → `Palatial` = Như hoàng cung.

**Vật liệu xây dựng thường gặp:** Clay = Đất sét, Clay Brick = Gạch đất sét, Limestone = Đá vôi, Wicker = Mây tre đan, Merlon = Tường răng cưa (trên bờ thành), Portcullis = Cổng sắt kéo lên được, Grated Door = Cửa song sắt, Reinforced Door = Cửa gia cố.

### D. Kỹ năng (theo `skill_name_*` thực tế trong game — 14 kỹ năng)
| EN | VI | Ghi chú |
| :--- | :--- | :--- |
| **Carpentry** | **Mộc** | Chế tác đồ gỗ, cung tên. |
| **Construction** | **Xây dựng** | Làm gạch, đẽo đá, thi công (game KHÔNG có skill "Masonry"). |
| **Smithing** | **Rèn** | Skill rèn vũ khí/giáp kim loại ("Blacksmithing" chỉ là tên research → *Rèn đúc*). |
| **Tailoring** | **May mặc** | Dệt vải, may áo quần, giáp da. |
| **Botany** | **Nông nghiệp** | Trồng trọt, thu hoạch thảo mộc. |
| **Culinary** | **Nấu nướng** | Bếp núc, pha thịt. |
| **Medicine** | **Chữa bệnh** | Băng bó, trị thương, nấu rượu thuốc. |
| **Marksman** | **Bắn cung** | Cung, nỏ. |
| **Melee** | **Cận chiến** | Kiếm, rìu, chùy, thương. |
| **Speechcraft** | **Giao tiếp** | Thương thuyết, mua bán, động viên. |
| **Mining** | **Khai mỏ** | Đào đất, khai thác đá và quặng. |
| **Animal Handling** | **Chăn nuôi** | Thuần hóa, săn bắn, câu cá. |
| **Intellectual** | **Học thức** | Nghiên cứu nhanh hơn (key game: `skill_name_Intelectual`). |
| **Art** | **Hội họa** | Vẽ tranh, tác phẩm nghệ thuật. |
| **Basic Skill** (`skill_name_None`) | **Kỹ năng cơ bản** | Việc không cần kỹ năng. |

### E. Đặc tính (Perks — 170 perk: dịch TỰ NHIÊN, GẦN GŨI, đọc là hiểu)
Mẫu chuẩn đã chốt (dịch các perk còn lại theo phong cách này):
| EN | VI | | EN | VI |
| :--- | :--- |---| :--- | :--- |
| Vigorous | Tràn đầy sức sống | | Gourmet | Sành ăn |
| Robust | Khỏe mạnh | | Gluttonous | Phàm ăn |
| Infirm | Ốm yếu | | Austere | Khắc khổ |
| Moribund | Sắp chết | | Congenial | Dễ gần |
| Night Owl | Cú đêm | | Outgoing | Cởi mở |
| Early Bird | Dậy sớm | | Churl | Thô lỗ |
| Somnolent | Hay ngủ gật | | Contemplative | Trầm tư |
| Forty Winks | Thích chợp mắt | | Industrious | Siêng năng |
| Hedonist | Thích hưởng lạc | | Lord of Misrule | Chúa tể tiệc tùng |
| Listless | Uể oải | | Sluggardly | Lười nhác |
| Benevolent | Nhân từ | | Laggardly | Chậm chạp |
| Ruthless | Tàn nhẫn | | Fleet Footed | Nhanh chân |
| Brawler | Hay gây gổ | | Whirlwind | Lanh lẹ |
| Disfigured | Dị dạng | | Brawny | Cơ bắp cuồn cuộn |
| Ill-favoured | Xấu xí | | Hefty | Đô con |
| Winsome | Duyên dáng | | Strapping | Vóc dáng lực lưỡng |
| Fair | Ưa nhìn | | Washout | Yếu ớt |
| Ravishing | Tuyệt sắc | | Dullard | Đần độn |
| Swigger | Bợm rượu | | Wise | Thông thái |
| Punch Drunk | Say bí tỉ | | Erudite | Uyên bác |
| Lightweight | Dễ say | | Bloodlust | Khát máu |
| Heat Resistant | Chịu nóng | | Callous | Vô cảm |
| Cold Hardy | Chịu rét | | Cannibal | Ăn thịt người |
| Hot-blooded | Máu nóng | | Wicche | Phù thủy |
| Chilly | Hay lạnh | | Ascetic | Khổ hạnh |
| Vulnerable | Dễ tổn thương | | Green Thumb | Mát tay |
| Elf Shot | Trúng tà | | Dainty | Kiểu cách |
| Snow White | Da trắng tuyết | | Precious | Khó chiều |

> Elf Shot = bệnh dân gian cho là do yêu tinh bắn tên; giữ sắc thái mê tín Trung Cổ.

### F. Sản xuất & Lao động (`name_prod_*`)
| EN | VI | | EN | VI |
| :--- | :--- |---| :--- | :--- |
| Butchering | Pha thịt | | Brewing | Nấu rượu |
| Fermenting | Lên men | | Firing clay | Nung đất sét |
| Cutting stone | Xẻ đá | | Sewing | May vá |
| Pickling | Muối chua | | Packaging | Đóng gói |
| Preparing ingredients | Sơ chế nguyên liệu | | Preparing healing remedies | Chế thuốc |
| Dismantle items | Tháo dỡ vật phẩm | | Smelt items | Nấu chảy vật phẩm |

### G. Thời tiết & Sự kiện môi trường
| EN | VI |
| :--- | :--- |
| Hailstorm | Mưa đá |
| Heat wave | Đợt nắng nóng |
| Cold snap | Đợt rét đậm |
| Thunderstorm | Dông bão |

### H. Nghiên cứu (Research — giữ số La Mã)
> `Agriculture III` → *Nông nghiệp III*, `Armourer II` → *Đóng giáp II*, `Blacksmithing` → *Rèn đúc*, `Brewing` → *Nấu rượu*, `Chemistry I/II` → *Hóa học I/II*.

### I. Chủ đề trò chuyện, tính cách, biệt hiệu (flavor — dịch tự do, đời thường, giữ chút chất Trung Cổ)
- `topic_smalltalk_*` (105): chủ đề chuyện phiếm ("the weather" → *thời tiết*, "the merits of turnips" → *củ cải có gì hay*).
- `bg_recent_name_*` (264): xuất thân/biệt hiệu dân làng ("Apostate" → *Kẻ bỏ đạo*, "Uprooted" → *Kẻ mất gốc*, "Penitent" → *Người sám hối*).
- `reaction_*` (41): mảnh câu cảm xúc ("seemed" → *có vẻ*, "shocked" → *sốc*).

---

## 5. PHÂN KỲ DỊCH THEO ĐỢT (map với 66 file patch đã chia nhỏ)

| Đợt | Phân hệ | File patch | Keys |
| :--- | :--- | :--- | :--- |
| **Đợt 1** 🔥 | Hướng dẫn & Almanac | `patch_01` → `patch_02` | 185 |
| **Đợt 2** | Sự kiện, phe phái, thương mại | `patch_03` → `patch_06` | 516 |
| **Đợt 3** | Dân làng, kỹ năng, chiến đấu, tâm lý | `patch_07` → `patch_11` | 697 |
| **Đợt 4** | Công trình, nội thất, phòng ốc | `patch_12` → `patch_19` | 1,159 |
| **Đợt 5** | Vũ khí, giáp, tài nguyên, lương thực | `patch_20` → `patch_29` | 1,354 |
| **Đợt 6** | Menu, cài đặt, HUD, cảnh báo | `patch_30` → `patch_35` | 778 |
| **Đợt 7** | UI tổng quát và chuỗi hệ thống | `patch_36` → `patch_66` | 4,188 |

**Tổng: 8,877 keys** (các key `dev_*`, `keycode_*` và font được giữ nguyên có chủ đích).

---

## 6. CHECKLIST MỖI ĐỢT DỊCH

1. Đọc lại Mục 2 (quy tắc kỹ thuật) trước khi dịch.
2. Dịch nhất quán theo bảng thuật ngữ; gặp thuật ngữ mới → **bổ sung ngay vào file này**.
3. Chạy `python3 verify_translation.py` → mục tiêu **0 ERROR** (placeholder/tag/newline).
4. Review cảnh báo `[UI LENGTH OVERFLOW]` — ưu tiên rút gọn key UI ngắn.
5. Commit riêng từng đợt.

### Trạng thái bản dịch 66 patch

- [x] Patch 01–02: Hướng dẫn và Cẩm nang.
- [x] Patch 03–06: Sự kiện, phe phái và thương mại.
- [x] Patch 07–11: Dân làng, kỹ năng, chiến đấu và tâm lý.
- [x] Patch 12–19: Công trình, nội thất và phòng ốc.
- [x] Patch 20–29: Vũ khí, giáp, tài nguyên và lương thực.
- [x] Patch 30–35: Menu, cài đặt, HUD và cảnh báo.
- [x] Patch 36–66: UI tổng quát, kỹ năng, chức vụ, cốt truyện phe phái và chuỗi hệ thống (đã hoàn tất 100% 8.877/8.877 key, dọn sạch toàn bộ 436 wrapper giả, khôi phục 111 mô tả tài nguyên và dịch chuẩn chuỗi lai).
- [x] Bảo toàn placeholder, gender token, rich-text tag và newline.
- [x] Build `Vietnamese.csv` đủ 8.877 key theo thứ tự master.
- [x] Verifier kỹ thuật: 8.877/8.877 key, 0 lỗi.
- [x] Rà soát và dịch hết các chuỗi còn giữ nguyên tiếng Anh/lai Anh–Việt.
