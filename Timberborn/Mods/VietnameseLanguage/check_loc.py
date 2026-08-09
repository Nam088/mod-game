import zipfile
import csv
import io
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def check_loc():
    zip_path = r'C:\Users\nam\Downloads\Compressed\Timberborn-AnkerGames\Timberborn\Timberborn_Data\StreamingAssets\Modding\Localizations.zip'
    vi_csv_path = r'C:\Users\nam\Documents\Timberborn\Mods\VietnameseLanguage\Localizations\viVN.csv'

    if not os.path.exists(vi_csv_path):
        print(f"Lỗi: Không tìm thấy file viVN.csv tại {vi_csv_path}")
        return

    # Read original enUS.csv
    with zipfile.ZipFile(zip_path, 'r') as z:
        with z.open('enUS.csv') as f:
            en_content = f.read().decode('utf-8-sig')
            en_reader = list(csv.DictReader(io.StringIO(en_content)))

    en_dict = {r['ID']: r['Text'] for r in en_reader}

    # Read viVN.csv
    with open(vi_csv_path, 'r', encoding='utf-8-sig') as f:
        vi_reader = list(csv.DictReader(f))

    vi_dict = {r['ID']: r['Text'] for r in vi_reader}

    print("==================================================")
    print("   BÁO CÁO KIỂM TRA BẢN DỊCH VIỆT HÓA TIMBERBORN  ")
    print("==================================================")
    print(f"Tổng số Key trong enUS.csv: {len(en_dict)}")
    print(f"Tổng số Key trong viVN.csv: {len(vi_dict)}")

    missing_keys = [k for k in en_dict if k not in vi_dict]
    print(f"Key bị thiếu: {len(missing_keys)}")

    untranslated = []
    translated_count = 0

    for k, en_text in en_dict.items():
        vi_text = vi_dict.get(k, '')
        if vi_text == en_text and re.search(r'[a-zA-Z]{2,}', en_text):
            clean_text = re.sub(r'\{[0-9]+\}|<[^>]+>|[0-9\.:,%\-\s]', '', en_text)
            if len(clean_text) > 0:
                untranslated.append((k, en_text, vi_text))
        else:
            translated_count += 1

    percentage = (translated_count / len(en_dict)) * 100
    print(f"Số Key ĐÃ Việt hóa: {translated_count} / {len(en_dict)} ({percentage:.1f}%)")
    print(f"Số Key CHƯA Việt hóa (trùng tiếng Anh): {len(untranslated)}")
    print("==================================================")

    if untranslated:
        print("\nDanh sách 15 Key chưa được Việt hóa gần nhất:")
        for k, en_t, vi_t in untranslated[:15]:
            print(f" - [{k}]: '{en_t}'")

if __name__ == '__main__':
    check_loc()
