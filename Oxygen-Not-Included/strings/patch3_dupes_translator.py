#!/usr/bin/env python3
"""
Patch 3: Dàn Đệ, Thuộc tính, Kỹ năng & Bệnh tật Translator for ONI
Áp dụng:
- Xưng hô Đệ tự nhiên.
- Dịch chuẩn xác các chỉ số sinh tồn và kỹ năng.
- Bảo toàn thẻ {0}, {Hotkey}, <link>, <b>...
"""

import sys, re
sys.path.insert(0, '/Users/nam088/code/nam088/mod-game/Oxygen-Not-Included/strings')
import polib

DUPE_EXACT = {
    "Air Consumption Rate": "Tốc độ tiêu thụ dưỡng khí",
    "Creativity": "Sáng tạo",
    "Athletics": "Thể lực (Tốc độ chạy)",
    "Bladder": "Mức bàng quang",
    "Agriculture": "Nông nghiệp",
    "Husbandry": "Chăn nuôi",
    "Cooking": "Nấu ăn",
    "Digging": "Đào bới",
    "Machinery": "Vận hành máy",
    "Caring": "Y tế & Chăm sóc",
    "Strength": "Sức mạnh (Gánh vác)",
    "Science": "Khoa học (Nghiên cứu)",
    "Piloting": "Lái tàu vũ trụ",
    "Tidying": "Dọn dẹp",
    "Construction": "Xây dựng",
    "Rocketry": "Tên lửa",
    "Stress": "Căng thẳng",
    "Morale": "Tinh thần",
    "Calories": "Năng lượng Calo",
    "Health": "Máu (Sinh lực)",
    "Immunity": "Miễn dịch",
    "Decor Expectation": "Yêu cầu trang trí",
    "Food Expectation": "Yêu cầu chất lượng món ăn",
    "Food Poisoning": "Ngộ độc thực phẩm",
    "Slimelung": "Vi khuẩn phổi (Slimelung)",
    "Zombie Spores": "Bào tử Zombie",
    "Radiation Sickness": "Nhiễm độc phóng xạ",
    "Hypothermia": "Hạ thân nhiệt",
    "Heat Stroke": "Sốc nhiệt",
    "Scalding": "Bỏng nhiệt",
    "Suffocating": "Đang ngạt thở",
    "Starving": "Đang đói lả",
    "Tantrum": "Cơn tam bành (Đập phá)",
    "Binge Eating": "Ăn vô độ xả căng thẳng",
    "Ugly Crier": "Khóc lóc thảm thiết",
    "Stress Vomiter": "Nôn mửa do xì-trét",
    "Overjoyed": "Cực kỳ hưng phấn",
    "Sparkle Streaker": "Chạy phát sáng phấn khích",
    "Super Productive": "Làm việc siêu năng suất",
    "Balloon Artist": "Thổi bóng bay tặng đồng đội",
    "Sticker Bomber": "Dán hình dán vui nhộn"
}

DUPE_DESC = {
    "Air Consumption determines how much <link=\"OXYGEN\">Oxygen</link> a Duplicant requires per minute to live.": "Tốc độ tiêu thụ dưỡng khí xác định lượng <link=\"OXYGEN\">Oxy</link> mà Đệ cần mỗi phút để duy trì sự sống.",
    "Determines how quickly a Duplicant produces <style=\"KKeyword\">Artwork</style>.": "Quyết định tốc độ Đệ tạo ra các tác phẩm <style=\"KKeyword\">Trang trí nghệ thuật</style>.",
    "Determines a Duplicant's default runspeed.": "Quyết định tốc độ chạy di chuyển cơ bản của Đệ.",
    "Determines how quickly a Duplicant's <style=\"KKeyword\">Bladder</style> fills or depletes.": "Quyết định mức độ làm đầy hoặc xả của <style=\"KKeyword\">Bàng quang</style> của Đệ.",
    "Determines how quickly and efficiently a Duplicant cultivates <style=\"KKeyword\">Plants</style>.": "Quyết định tốc độ và hiệu quả của Đệ khi chăm sóc <style=\"KKeyword\">Cây trồng</style>."
}

po = polib.pofile('/Users/nam088/code/nam088/mod-game/Oxygen-Not-Included/strings/strings.po')

count = 0
for e in po:
    if e.msgctxt and 'DUPLICANTS' in e.msgctxt:
        if e.msgid in DUPE_EXACT:
            e.msgstr = DUPE_EXACT[e.msgid]
            count += 1
        elif e.msgid in DUPE_DESC:
            e.msgstr = DUPE_DESC[e.msgid]
            count += 1

po.save('/Users/nam088/code/nam088/mod-game/Oxygen-Not-Included/strings/strings.po')
print(f'Applied Patch 3 dupe translations to {count} entries.')
