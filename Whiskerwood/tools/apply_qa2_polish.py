import json
import os

script_path = r"D:\code\mod-game\Whiskerwood\tools\translate_phase1.py"
with open(script_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    '"settings.g.holdToBulldoze": "Nhấn Giữ Để Phá Hủy"': '"settings.g.holdToBulldoze": "Nhấn Giữ Để Phá Dỡ"',
    '"settings.keybind.BulldozeTool": "Phá Hủy"': '"settings.keybind.BulldozeTool": "Phá Dỡ"',
    '"Bật/tắt chế độ phá hủy. Nhấn giữ để dỡ bỏ công trình': '"Bật/tắt chế độ phá dỡ. Nhấn giữ để dỡ bỏ công trình',
    '"settings.keybind.minetool": "Đào Mỏ"': '"settings.keybind.minetool": "Khai Mỏ"',
    '"action.sendToSea": "Đưa Ra Biển"': '"action.sendToSea": "Cho Ra Khơi"',
    '"menu.compilingshaders": "Đang Tải Shader Trước"': '"menu.compilingshaders": "Đang Tải Trước Shader"',
    '"tooltip.totalFood": "Tổng Thức Ăn Dự Trữ"': '"tooltip.totalFood": "Tổng Lương Thực Ăn Được"',
    '"error.mustbeempty": "Kho phải trống hoàn toàn."': '"error.mustbeempty": "Phải dọn sạch đồ bên trong."',
    '"settings.keybind.rotCW": "Xoay Camera Theo Chiều Kim Đồng Hồ"': '"settings.keybind.rotCW": "Xoay Camera Thuận KĐH"',
    '"settings.keybind.rotCCW": "Xoay Camera Ngược Chiều Kim Đồng Hồ"': '"settings.keybind.rotCCW": "Xoay Camera Ngược KĐH"',
    '"settings.keybind.slice": "Bật/Tắt Cắt Tầng Quan Sát"': '"settings.keybind.slice": "Bật/Tắt Cắt Tầng"',
    '"settings.keybind.cycleVariant": "Kiểu Biến Thể Tiếp Theo"': '"settings.keybind.cycleVariant": "Biến Thể Tiếp Theo"',
}

replaced = 0
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        replaced += 1
    else:
        print(f"[WARN] Not found: {old}")

with open(script_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Applied {replaced} / {len(replacements)} polish items to translate_phase1.py!")
