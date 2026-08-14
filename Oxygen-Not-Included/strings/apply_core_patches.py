#!/usr/bin/env python3
"""
Oxygen Not Included - Core Engine Translations Generator
Chạy dịch chuẩn hóa trên toàn bộ 6 Patch với các nguyên tắc:
1. Giữ nguyên 100% thương hiệu / proper nouns (Discord, Steam, Klei...)
2. Giữ nguyên 100% tên loài sinh vật (Hatch, Drecko, Puft, Pip...)
3. Dùng tiếng Việt chuẩn kỹ thuật cho máy móc & công trình (Lựa chọn 1)
4. Xưng hô Đệ tự nhiên, ngắn gọn chống tràn UI
5. Bảo toàn 100% link tags, formatting tags, placeholders.
"""

import os
import sys
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import polib

PO_PATH = os.path.join(BASE_DIR, 'strings.po')

# Bảng dịch Nguyên tố hóa học (Elements)
ELEMENT_MAP = {
    "Oxygen": "Oxy", "Carbon Dioxide": "Carbon Dioxide (CO2)", "Hydrogen": "Hydro", "Chlorine": "Clo",
    "Chlorine Gas": "Khí Clo", "Natural Gas": "Khí gas tự nhiên", "Polluted Oxygen": "Oxy ô nhiễm",
    "Water": "Nước", "Dirty Water": "Nước bẩn", "Polluted Water": "Nước ô nhiễm", "Salt Water": "Nước muối",
    "Brine": "Nước muối đậm đặc", "Crude Oil": "Dầu thô", "Petroleum": "Dầu mỏ tinh luyện",
    "Ethanol": "Ethanol", "Magma": "Dung nham", "Super Coolant": "Siêu dung dịch làm mát",
    "Sandstone": "Đá sa thạch", "Granite": "Đá hoa cương (Granite)", "Igneous Rock": "Đá mắc-ma",
    "Obsidian": "Đá hắc diệu thạch (Obsidian)", "Sedimentary Rock": "Đá trầm tích",
    "Sand": "Cát", "Dirt": "Đất", "Polluted Dirt": "Đất ô nhiễm", "Clay": "Đất sét",
    "Coal": "Than đá", "Refined Carbon": "Carbon tinh luyện", "Diamond": "Kim cương",
    "Iron Ore": "Quặng sắt", "Copper Ore": "Quặng đồng", "Gold Amalgam": "Hợp kim vàng",
    "Aluminum Ore": "Quặng nhôm", "Wolframite": "Quặng Vonfram (Wolframite)",
    "Iron": "Sắt tinh luyện", "Copper": "Đồng tinh luyện", "Gold": "Vàng tinh luyện",
    "Aluminum": "Nhôm tinh luyện", "Tungsten": "Vonfram", "Steel": "Thép",
    "Plastic": "Nhựa Polymer", "Glass": "Thủy tinh", "Lime": "Vôi sống",
    "Bleach Stone": "Đá tẩy trắng (Sinh khí clo)", "Oxylite": "Đá Oxylite (Tỏa oxy)",
    "Uranium Ore": "Quặng Uranium", "Enriched Uranium": "Uranium làm giàu"
}

# Bảng dịch Nghiên cứu & Công nghệ (Research)
RESEARCH_MAP = {
    "Basic Farming": "Nông nghiệp cơ bản",
    "Improved Oxygen": "Cải tiến hệ thống Oxy",
    "Power Regulation": "Điều tiết điện năng",
    "Internal Combustion": "Động cơ đốt trong",
    "Advanced Research": "Nghiên cứu nâng cao",
    "Sanitation": "Vệ sinh & Tẩy uế",
    "Advanced Sanitation": "Hệ thống vệ sinh nâng cao",
    "Filtration": "Lọc chất lỏng & Khí",
    "Liquid Piping": "Hệ thống ống nước",
    "Improved Ventilation": "Cải tiến thông gió",
    "Automatic Control": "Điều khiển tự động",
    "Smart Storage": "Lưu trữ thông minh",
    "Refined Renovations": "Trang trí nội thất cao cấp",
    "Smelting": "Luyện kim tinh chế",
    "Plastics": "Sản xuất nhựa",
    "Renewable Energy": "Năng lượng tái tạo",
    "Space Program": "Chương trình vũ trụ",
    "Solid Transport": "Vận chuyển chất rắn",
    "Animal Control": "Thuần hóa & Chăn nuôi",
    "Computing": "Tin học & Tự động hóa"
}

# Bảng dịch Kiểu phòng (Rooms)
ROOM_MAP = {
    "Latrine": "Nhà vệ sinh cơ bản",
    "Washroom": "Phòng vệ sinh hiện đại",
    "Barracks": "Phòng ngủ tập thể",
    "Bedroom": "Phòng ngủ riêng",
    "Mess Hall": "Phòng ăn tập thể",
    "Great Hall": "Đại sảnh tiệc",
    "Kitchen": "Nhà bếp",
    "Hospital": "Bệnh viện",
    "Massage Clinic": "Phòng mát-xa thư giãn",
    "Recreation Room": "Phòng giải trí",
    "Park": "Công viên cây xanh",
    "Nature Reserve": "Khu bảo tồn thiên nhiên",
    "Stable": "Chuồng nuôi sinh vật",
    "Laboratory": "Phòng thí nghiệm",
    "Power Plant": "Nhà máy điện"
}

# Bảng dịch Món ăn & Thực phẩm (Items / Food)
FOOD_MAP = {
    "Mush Bar": "Bánh bột thô",
    "Fried Mush Bar": "Bánh bột chiên",
    "Lice Loaf": "Bánh mì hạt rận",
    "Pickled Meal": "Hạt chua muối",
    "Gristle Berry": "Quả mọng nướng",
    "Stuffed Berry": "Bánh quả mọng kẹp kem",
    "Omelette": "Trứng rán",
    "Cooked Meat": "Thịt nướng BBQ",
    "Barbeque": "Thịt nướng BBQ",
    "Frost Bun": "Bánh bao lúa mì tuyết",
    "Pepper Bread": "Bánh mì ớt cay",
    "Mushroom Wrap": "Bánh cuộn nấm",
    "Spicy Tofu": "Đậu phụ sốt cay",
    "Surf'n'Turf": "Bò bít tết kèm hải sản",
    "Frost Burger": "Burger băng tuyết thượng hạng"
}

def translate_element_name(text):
    m = re.match(r'(<link="[^"]+">)(.*?)(</link>)', text)
    if m:
        p, name, s = m.groups()
        if name in ELEMENT_MAP:
            return f"{p}{ELEMENT_MAP[name]}{s}"
    elif text in ELEMENT_MAP:
        return ELEMENT_MAP[text]
    return None

def translate_research_name(text):
    m = re.match(r'(<link="[^"]+">)(.*?)(</link>)', text)
    if m:
        p, name, s = m.groups()
        if name in RESEARCH_MAP:
            return f"{p}{RESEARCH_MAP[name]}{s}"
    elif text in RESEARCH_MAP:
        return RESEARCH_MAP[text]
    return None

def translate_room_name(text):
    m = re.match(r'(<link="[^"]+">)(.*?)(</link>)', text)
    if m:
        p, name, s = m.groups()
        if name in ROOM_MAP:
            return f"{p}{ROOM_MAP[name]}{s}"
    elif text in ROOM_MAP:
        return ROOM_MAP[text]
    return None

def translate_food_name(text):
    m = re.match(r'(<link="[^"]+">)(.*?)(</link>)', text)
    if m:
        p, name, s = m.groups()
        if name in FOOD_MAP:
            return f"{p}{FOOD_MAP[name]}{s}"
    elif text in FOOD_MAP:
        return FOOD_MAP[text]
    return None


def run_full_pipeline():
    po = polib.pofile(PO_PATH)
    total_updated = 0

    print("[*] Đang nạp và xử lý toàn bộ 6 Patch...")
    for entry in po:
        if not entry.msgctxt:
            continue
        ctxt = entry.msgctxt
        msgid = entry.msgid
        res = None

        if 'ELEMENTS.' in ctxt and (ctxt.endswith('.NAME') or '.ELEMENTS.' in ctxt):
            res = translate_element_name(msgid)
        elif 'RESEARCH.TECH.' in ctxt and ctxt.endswith('.NAME'):
            res = translate_research_name(msgid)
        elif 'ROOMS.TYPES.' in ctxt and ctxt.endswith('.NAME'):
            res = translate_room_name(msgid)
        elif 'ITEMS.FOOD.' in ctxt and ctxt.endswith('.NAME'):
            res = translate_food_name(msgid)

        if res and res != entry.msgstr:
            entry.msgstr = res
            total_updated += 1

    po.save(PO_PATH)
    print(f"[✓] Đã cập nhật thêm {total_updated} chuỗi vào strings.po!")


if __name__ == '__main__':
    run_full_pipeline()
