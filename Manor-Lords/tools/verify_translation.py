#!/usr/bin/env python3
"""
Manor Lords (Unreal Engine 5.5) Translation Verifier
Kiểm tra tính toàn vẹn kỹ thuật, thẻ định dạng UE, placeholder, và cảnh báo tràn UI cho các file JSON bản dịch
"""

import os
import sys
import re
import json
import glob

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TRANS_DIR = os.path.join(CURRENT_DIR, "..", "translations")

class ManorLordsVerifier:
    def __init__(self, trans_dir=TRANS_DIR):
        self.trans_dir = trans_dir
        self.errors = []
        self.warnings = []
        self.stats = {
            'total_files': 0,
            'total_strings': 0,
            'translated': 0,
            'untranslated': 0,
            'placeholder_errors': 0,
            'tag_errors': 0,
            'ui_length_warnings': 0,
        }

    def extract_placeholders(self, text):
        # Extract {0}, {1}, {Amount}, {br}, {PlayerName}, etc.
        return set(re.findall(r'\{[A-Za-z0-9_:]+\}', text))

    def extract_ue_tags(self, text):
        # Extract UE RichText tags: <h>, </>, <img id="..."/>, <style="..."/>, <color=...>, etc.
        tags = re.findall(r'<[/]?[a-zA-Z0-9_=#\":\.\- ]+[/]?>', text)
        return tags

    def verify_file(self, json_path):
        filename = os.path.basename(json_path)
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                entries = json.load(f)
            except Exception as e:
                self.errors.append(f"[{filename}] Lỗi cú pháp JSON: {e}")
                return

        self.stats['total_files'] += 1

        for idx, entry in enumerate(entries):
            self.stats['total_strings'] += 1
            key = entry.get('key', f'row_{idx}')
            en = entry.get('en', '')
            vi = entry.get('vi', '')

            if vi == "" and en != "":
                self.stats['untranslated'] += 1
                continue

            self.stats['translated'] += 1

            # 1. Kiểm tra Placeholders ({0}, {br}, {ItemName}, ...)
            orig_ph = self.extract_placeholders(en)
            trans_ph = self.extract_placeholders(vi)
            if orig_ph != trans_ph:
                missing = orig_ph - trans_ph
                extra = trans_ph - orig_ph
                err_msg = f"[{filename} | Key: {key}] Sai Placeholder. Thiếu: {missing}, Thừa: {extra}"
                self.errors.append(err_msg)
                self.stats['placeholder_errors'] += 1

            # 2. Kiểm tra UE RichText Tags (<h>, </>, <img id="..."/>)
            orig_tags = self.extract_ue_tags(en)
            trans_tags = self.extract_ue_tags(vi)
            if len(orig_tags) != len(trans_tags):
                warn_msg = f"[{filename} | Key: {key}] Chênh lệch số lượng thẻ UE RichText: Gốc ({len(orig_tags)}) != Dịch ({len(trans_tags)})"
                self.warnings.append(warn_msg)
                self.stats['tag_errors'] += 1

            # 3. Kiểm tra ký tự xuống dòng \n
            if en.count('\n') != vi.count('\n'):
                warn_msg = f"[{filename} | Key: {key}] Lệch số lượng ký tự xuống dòng (\\n)"
                self.warnings.append(warn_msg)

            # 4. Cảnh báo độ dài giao diện (UI Overflows)
            if 'Menu' in filename or 'MainUI' in filename or 'BuildingNames' in filename:
                if len(en) > 8 and len(vi) > len(en) * 1.85:
                    warn_msg = f"[{filename} | Key: {key}] Chuỗi UI tiếng Việt quá dài (>1.85x gốc): '{vi[:40]}...'"
                    self.warnings.append(warn_msg)
                    self.stats['ui_length_warnings'] += 1

    def verify_all(self):
        json_files = sorted(glob.glob(os.path.join(self.trans_dir, "*.json")))
        print(f"[*] Bắt đầu kiểm tra {len(json_files)} file JSON trong: {self.trans_dir}")

        for jf in json_files:
            self.verify_file(jf)

        self.print_report()

    def print_report(self):
        print("\n" + "=" * 65)
        print("       BÁO CÁO KẾT QUẢ THẨM ĐỊNH BẢN DỊCH MANOR LORDS")
        print("=" * 65)
        print(f"Tổng số tập tin JSON: {self.stats['total_files']}")
        print(f"Tổng số chuỗi       : {self.stats['total_strings']:,}")
        print(f"Đã dịch (Translated): {self.stats['translated']:,}")
        print(f"Chưa dịch (Empty)   : {self.stats['untranslated']:,}")
        if self.stats['total_strings'] > 0:
            progress = (self.stats['translated'] / self.stats['total_strings']) * 100
            print(f"Tiến độ hoàn thành  : {progress:.2f}%")
        print("-" * 65)
        print(f"Lỗi Placeholder     : {self.stats['placeholder_errors']}")
        print(f"Lệch RichText Tags  : {self.stats['tag_errors']}")
        print(f"Cảnh báo tràn UI    : {self.stats['ui_length_warnings']}")
        print("=" * 65)

        if self.errors:
            print("\n[!] DANH SÁCH LỖI NGHIÊM TRỌNG CẦN SỬA (Tối đa 10 lỗi đầu):")
            for e in self.errors[:10]:
                print(f"  ❌ {e}")
        if self.warnings:
            print(f"\n[⚠️] TỔNG SỐ CẢNH BÁO CẦN LƯU Ý: {len(self.warnings)}")
            for w in self.warnings:
                print(f"  ⚠️  {w}")

    def report_empty_keys(self):
        json_files = sorted(glob.glob(os.path.join(self.trans_dir, "*.json")))
        for jf in json_files:
            fname = os.path.basename(jf)
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
            for idx, entry in enumerate(data):
                if entry.get("vi") == "" and entry.get("en") != "":
                    print(f"  [EMPTY] {fname} | Key: {entry.get('key')} | EN: '{entry.get('en')}'")

if __name__ == "__main__":
    verifier = ManorLordsVerifier()
    verifier.verify_all()
    print("\n[*] Chi tiết các chuỗi còn trống (nếu có):")
    verifier.report_empty_keys()

