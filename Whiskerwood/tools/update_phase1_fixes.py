import json
import os
import re

# Read translate_phase1.py
script_path = r"D:\code\mod-game\Whiskerwood\tools\translate_phase1.py"
with open(script_path, "r", encoding="utf-8") as f:
    content = f.read()

replacements = {
    '"action.ship.dismiss": "Giải Phóng Tàu"': '"action.ship.dismiss": "Cho Tàu Rời Bến"',
    '"toolbar.masonry": "Thợ Nề"': '"toolbar.masonry": "Công Trình Đá"',
    '"aa.quality.ultraquality": "Chất Lượng Cao"': '"aa.quality.ultraquality": "Siêu Chất Lượng"',
    '"settings.a.ui": "Giao Diện"': '"settings.a.ui": "Âm Giao Diện"',
    '"action.acceptDefeat": "Thu Dọn Tổn Thất & Rời Đi"': '"action.acceptDefeat": "Vớt Vát Thiệt Hại & Rời Đi"',
    '"toolbar.navigation": "Lối Đi & Cầu Nối"': '"toolbar.navigation": "Đường Đi Bộ"',
    '"action.disableAllInputs": "Ngắt Mọi Ngõ Vào"': '"action.disableAllInputs": "Ngừng Nhận Hàng Vào"',
    '"tooltip.dockStorage": "Hàng Tồn Tại Cảng"': '"tooltip.dockStorage": "Hàng Tại Bến Cảng"',
    '"tooltip.shipStorage": "Khoang Chứa Hàng Của Tàu"': '"tooltip.shipStorage": "Khoang Hàng Của Tàu"',
    '"settings.g.vsync": "Đồng Bộ Khung Hình (VSync)"': '"settings.g.vsync": "Đồng Bộ Dọc (VSync)"',
    '"settings.dpiscale": "Tỉ Lệ Giao Diện (UI Scale)"': '"settings.dpiscale": "Tỉ Lệ Giao Diện"',
    '"hoverNotif.occupied": "Đã Có Người Chiếm"': '"hoverNotif.occupied": "Đã Kín Chỗ"',
    '"settings.keybind.OpenEventQueue": "Xem Tin Nhắn"': '"settings.keybind.OpenEventQueue": "Xem Bảng Tin Sự Kiện"',
    '"menu.quitdesktopheader": "Thoát Ra Màn Hình"': '"menu.quitdesktopheader": "Thoát Ra Desktop"',
    '"toolbar.minetool": "Đào Mỏ"': '"toolbar.minetool": "Khai Mỏ"',
    '"action.assignFreeShip": "Gán Tàu Mới"': '"action.assignFreeShip": "Điều Tàu Mới"',
    '"action.heater.overdrive.desc": "Tiêu hao gấp đôi nhiên liệu để tăng mạnh nhiệt lượng."': '"action.heater.overdrive.desc": "Tiêu hao gấp đôi nhiên liệu để tăng thêm nhiệt lượng."',
    '"settings.g.vfxq": "Hiệu Ứng & Thời Tiết"': '"settings.g.vfxq": "Chất Lượng Hiệu Ứng & Thời Tiết"',
    '"settings.g.ppq": "Xử Lý Hậu Kỳ"': '"settings.g.ppq": "Chất Lượng Hậu Kỳ"',
    '"menu.loadcolony": "Tải Trò Chơi"': '"menu.loadcolony": "Tải Game"',
    '"toolbar.bulldoze": "Phá Hủy"': '"toolbar.bulldoze": "Phá Dỡ"',
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

print(f"Updated {replaced} / {len(replacements)} translations in translate_phase1.py!")
