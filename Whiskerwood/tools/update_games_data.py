import json

def update_games_data():
    path = r'D:\code\mod-game\docs\assets\data\games-data.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    whiskerwood_entry = {
        "id": "whiskerwood",
        "title": "Whiskerwood",
        "genre": "Xây Dựng Thuộc Địa & Quản Lý Chuỗi Cung Ứng Hơi Nước",
        "badge": "100% Hoàn Thiện",
        "version": "v0.1.0 (Unreal Engine 5)",
        "keys_count": "2,751 keys (Tier S)",
        "rating": "5.0 ★★★★★",
        "image": "assets/images/whiskerwood_preview.png",
        "screenshot": "assets/images/whiskerwood_preview.jpg",
        "download_url": "https://github.com/Nam088/mod-game/releases/download/ww-v0.1.0/Whiskerwood-Vietnamese-Mod-v0.1.0.zip",
        "github_folder": "https://github.com/Nam088/mod-game/tree/master/Whiskerwood",
        "tagline": "Xây dựng thuộc địa làng chuột thời Victoria, chuỗi cung ứng cơ khí & đối phó cống thuế loài Mèo",
        "description": "Bản dịch Việt hóa trọn vẹn 100% (2.751 chuỗi) cho Whiskerwood (Unreal Engine 5). Bản địa hóa toàn diện hệ thống băng chuyền cơ khí, máng trượt, phễu nạp, thang nâng, lò sưởi hơi nước, tâm lý và cảm xúc bầy chuột, hàng hải thám hiểm đại dương, chuỗi sắc lệnh cống thuế của Phe Móng Vuốt (Claws) và cao trào cuộc khởi nghĩa của Stormie.",
        "highlights": [
            "Việt hóa 100% (2.751 keys) - Đạt chuẩn Blind QA Tier S (9.1/10) với 0 lỗi cú pháp.",
            "Tích hợp sẵn font tiếng Việt có dấu chuẩn Unreal Engine 5 trong file PAK.",
            "Chuẩn hóa hệ thống logistics cơ khí: Băng Chuyền, Máng Trượt, Phễu Nạp, Bệ Phóng, Bộ Lọc, Nồi Hơi, Tháp Sàng Khoáng Sản.",
            "Văn phong ngụ ngôn Victoria đặc sắc: Giọng điệu bề trên bóc lột của loài Mèo đối lập với sự cần cù, tình nghĩa của bầy chuột."
        ],
        "install_guide": [
            "Tải file `Whiskerwood-Vietnamese-Mod-v0.1.0.zip` về máy.",
            "Giải nén file `Whiskerwood-Vietnamese_P.pak` vào thư mục: `[Thư Mục Cài Game]\\Whiskerwood\\Content\\Paks\\~mods\\` (tạo thư mục `~mods` nếu chưa có).",
            "Khởi động game Whiskerwood và thưởng thức 100% tiếng Việt tự động nạp mượt mà!"
        ],
        "preview_terms": [
            {"en": "Approval", "vi": "Lòng Dân", "cat": "Chỉ số"},
            {"en": "The Claws", "vi": "Phe Móng Vuốt", "cat": "Phe phái"},
            {"en": "Tail / Acting Tail", "vi": "Trưởng Làng / Quyền Trưởng Làng", "cat": "Danh xưng"},
            {"en": "Whisker Conveyor", "vi": "Băng Chuyền Chở Chuột", "cat": "Logistics"},
            {"en": "Input Hopper", "vi": "Phễu Nạp Hàng", "cat": "Logistics"},
            {"en": "Jump Pad", "vi": "Bệ Bắn Hàng / Bệ Phóng Chuột", "cat": "Cơ khí"},
            {"en": "Charcoal Furnace", "vi": "Lò Than Củi", "cat": "Công trình"},
            {"en": "Fine Tea", "vi": "Trà Thượng Hạng", "cat": "Tài nguyên"},
            {"en": "Ballast Rocks", "vi": "Đá Dằn Tàu", "cat": "Hàng hải"},
            {"en": "Work Dock", "vi": "Bến Tàu Thợ", "cat": "Công trình"},
            {"en": "Cold Snap", "vi": "Đợt Rét Đậm", "cat": "Thời tiết"},
            {"en": "Overtime Continuation", "vi": "Gia Hạn Tự Động Làm Thêm Giờ", "cat": "Chính sách"}
        ]
    }
    
    # Check if already present
    data = [g for g in data if g.get("id") != "whiskerwood"]
    # Insert at beginning
    data.insert(0, whiskerwood_entry)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully updated games-data.json with Whiskerwood! Total games: {len(data)}")

if __name__ == '__main__':
    update_games_data()
