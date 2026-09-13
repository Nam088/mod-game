import os
import shutil
import zipfile

def setup():
    src = r'C:\Users\nam\.gemini\antigravity-cli\brain\5b338661-4e47-429f-8594-24deb51cf7a9\whiskerwood_preview_1789291628744.jpg'
    
    # Copy images
    destinations = [
        r'D:\code\mod-game\docs\assets\images\whiskerwood_preview.png',
        r'D:\code\mod-game\docs\assets\images\whiskerwood_preview.jpg',
        r'D:\code\mod-game\Whiskerwood\whiskerwood_preview.png',
        r'D:\code\mod-game\Whiskerwood\preview.png'
    ]
    
    for dest in destinations:
        shutil.copy2(src, dest)
        print(f"Copied image to: {dest}")
        
    # Create ZIP distribution package
    zip_path = r'D:\code\mod-game\Whiskerwood\Whiskerwood-Vietnamese-Mod-v0.1.0.zip'
    pak_file = r'D:\code\mod-game\Whiskerwood\Whiskerwood-Vietnamese_P.pak'
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(pak_file, 'Whiskerwood-Vietnamese_P.pak')
        # Add a quick Readme in ZIP
        readme_content = """WHISKERWOOD - BẢN DỊCH TIẾNG VIỆT (VIETNAMESE MOD)
Tác giả: Nam088
Phiên bản: v0.1.0 (Unreal Engine 5)
Tương thích: Bản quyền Steam, Epic Games, GOG

HƯỚNG DẪN CÀI ĐẶT:
1. Sao chép tệp 'Whiskerwood-Vietnamese_P.pak' vào thư mục:
   [Thư Mục Cài Game]\\Whiskerwood\\Content\\Paks\\~mods\\
   (Nếu chưa có thư mục '~mods', hãy tạo một thư mục mới có tên là '~mods').

2. Khởi động game Whiskerwood. Toàn bộ giao diện, công trình, chuỗi cung ứng,
   tâm lý bầy chuột và cốt truyện sẽ tự động hiển thị Tiếng Việt 100%!

Chúc bạn có những giờ phút xây dựng thuộc địa làng chuột thật vui vẻ!
"""
        zf.writestr('HUONG_DAN_CAI_DAT.txt', readme_content)
        
    print(f"Created release package: {zip_path} ({os.path.getsize(zip_path):,} bytes)")

if __name__ == '__main__':
    setup()
