#!/usr/bin/env python3
"""
Cập nhật Patch 2: Công trình & Máy móc với thuật ngữ gọt giũa theo Lựa chọn 1 (Khuyên dùng)
- Cực kỳ ngắn gọn, thuận miệng, đúng phong cách dân chơi ONI.
- Bảo toàn 100% link tags, placeholder, HTML tags.
"""

import sys, re
sys.path.insert(0, '/Users/nam088/code/nam088/mod-game/Oxygen-Not-Included/strings')
import polib

BUILDING_NAMES = {
    # Tinh chỉnh theo Lựa chọn 1 ngắn gọn, chuẩn xác
    "Super Computer": "Siêu máy tính",
    "Massage Table": "Bàn mát-xa",
    "Flush Toilet": "Bồn cầu xả nước",
    "Wood Burner": "Lò đốt gỗ",
    "Heavi-Watt Wire": "Dây cao thế",
    "Heavi-Watt Conductive Wire": "Dây cao thế cao cấp",
    "Gas Vent": "Lỗ xả khí",
    "High Pressure Gas Vent": "Lỗ xả khí áp suất cao",
    "Liquid Vent": "Lỗ xả nước",
    "Liquid Conditioner": "Máy làm mát chất lỏng",
    "Refrigerator": "Tủ lạnh",
    "Farm Tile": "Gạch trồng trọt",
    "Hydroponic Farm": "Gạch thủy canh",
    "Printing Pod": "Kén in",
    
    # Các công trình khác duy trì chuẩn ngắn gọn
    "Nuclear Apothecary": "Hiệu thuốc hạt nhân",
    "Soldering Station": "Bàn hàn linh kiện",
    "Disease Clinic": "Phòng khám bệnh",
    "Airborne Critter Lure": "Bẫy sinh vật bay",
    "Airborne Critter Condo": "Nhà trú sinh vật bay",
    "Thermo Regulator": "Máy làm mát khí",
    "Deodorizer": "Máy lọc không khí",
    "Algae Distiller": "Máy chưng cất tảo",
    "Algae Terrarium": "Hộp tảo quang hợp",
    "Apothecary": "Bàn bào chế thuốc",
    "Arcade Cabinet": "Máy game thùng",
    "Artifact Analysis Station": "Trạm phân tích cổ vật",
    "Artifact Transport Module": "Khoang chở cổ vật",
    "Space Cadet Centrifuge": "Máy ly tâm phi hành",
    "Robo-Miner": "Máy đào tự động",
    "Battery": "Bình ắc quy nhỏ",
    "Jumbo Battery": "Bình ắc quy lớn",
    "Battery Module": "Khoang ắc quy tên lửa",
    "Smart Battery": "Bình ắc quy thông minh",
    "Beach Chair": "Ghế bãi biển",
    "Cot": "Giường đơn",
    "Camping Cot": "Giường cắm trại",
    "Lab Cot": "Giường thí nghiệm",
    "Stargazer Cot": "Giường ngắm sao",
    "Comfy Bed": "Giường êm ái",
    "Ladder Bed": "Giường kèm thang",
    "Luxury Bed": "Giường cao cấp",
    "Outhouse": "Nhà vệ sinh thô sơ",
    "Shower": "Phòng tắm",
    "Wash Basin": "Chậu rửa tay",
    "Hand Sanitizer": "Bình rửa tay sát khuẩn",
    "Electrolyzer": "Máy điện phân nước",
    "Water Sieve": "Máy lọc nước",
    "Coal Generator": "Máy phát điện than",
    "Hydrogen Generator": "Máy phát điện hydro",
    "Natural Gas Generator": "Máy phát điện khí gas",
    "Petroleum Generator": "Máy phát điện dầu mỏ",
    "Manual Generator": "Máy phát điện thủ công",
    "Solar Panel": "Pin mặt trời",
    "Steam Turbine": "Tua bin hơi nước",
    "Power Transformer": "Máy biến áp",
    "Power Transformer (Small)": "Máy biến áp nhỏ",
    "Large Power Transformer": "Máy biến áp lớn",
    "Wire": "Dây điện",
    "Conductive Wire": "Dây điện cao cấp",
    "Wire Bridge": "Cầu vượt dây điện",
    "High-Wattage Wire Bridge": "Cầu vượt dây cao thế",
    "Conductive Wire Bridge": "Cầu vượt dây điện cao cấp",
    "Gas Pump": "Máy bơm khí",
    "Mini Gas Pump": "Máy bơm khí mini",
    "Gas Pipe": "Ống dẫn khí",
    "Insulated Gas Pipe": "Ống khí cách nhiệt",
    "Radiant Gas Pipe": "Ống khí tản nhiệt",
    "Gas Conduit Bridge": "Cầu vượt ống khí",
    "Gas Filter": "Bộ lọc khí",
    "Gas Valve": "Van điều tiết khí",
    "Gas Shutoff": "Van ngắt khí tự động",
    "Gas Reservoir": "Bồn chứa khí",
    "Liquid Pump": "Máy bơm nước",
    "Mini Liquid Pump": "Máy bơm nước mini",
    "Liquid Pipe": "Ống dẫn nước",
    "Insulated Liquid Pipe": "Ống nước cách nhiệt",
    "Radiant Liquid Pipe": "Ống nước tản nhiệt",
    "Liquid Conduit Bridge": "Cầu vượt ống nước",
    "Liquid Filter": "Bộ lọc nước",
    "Liquid Valve": "Van điều tiết nước",
    "Liquid Shutoff": "Van ngắt nước tự động",
    "Liquid Reservoir": "Bồn chứa nước",
    "Microbe Musher": "Máy ép thực phẩm",
    "Electric Grill": "Bếp nướng điện",
    "Gas Range": "Bếp gas",
    "Ration Box": "Thùng chứa khẩu phần",
    "Planter Box": "Hộp trồng cây",
    "Critter Drop-off": "Điểm tập kết sinh vật",
    "Critter Pick-up": "Điểm đón sinh vật",
    "Critter Feeder": "Máng ăn sinh vật",
    "Grooming Station": "Trạm chải lông",
    "Shearing Station": "Trạm xén lông",
    "Incubator": "Lồng ấp trứng",
    "Fish Feeder": "Máng cho cá ăn",
    "Fish Release": "Điểm thả cá",
    "Rock Crusher": "Máy nghiền đá",
    "Metal Refinery": "Lò luyện kim",
    "Glass Forge": "Lò đúc thủy tinh",
    "Oil Refinery": "Nhà máy lọc dầu",
    "Polymer Press": "Máy ép nhựa",
    "Desalinator": "Máy khử muối",
    "Research Center": "Bàn nghiên cứu",
    "Telescope": "Kính viễn vọng",
    "Virtual Planetarium": "Cung thiên văn"
}

def translate_building_name(text):
    m = re.match(r'(<link="[^"]+">)(.*?)(</link>)', text)
    if m:
        prefix, name, suffix = m.groups()
        if name in BUILDING_NAMES:
            return f"{prefix}{BUILDING_NAMES[name]}{suffix}"
    elif text in BUILDING_NAMES:
        return BUILDING_NAMES[text]
    return None

po = polib.pofile('/Users/nam088/code/nam088/mod-game/Oxygen-Not-Included/strings/strings.po')

count = 0
for e in po:
    if e.msgctxt and ('BUILDING' in e.msgctxt or 'BLUEPRINTS' in e.msgctxt):
        trans = translate_building_name(e.msgid)
        if trans:
            e.msgstr = trans
            count += 1

po.save('/Users/nam088/code/nam088/mod-game/Oxygen-Not-Included/strings/strings.po')
print(f'Applied refined building translations to {count} entries.')
