#!/usr/bin/env python3
"""
Oxygen Not Included (ONI) Translation Verifier
Kiểm tra tính toàn vẹn kỹ thuật, tag định dạng, placeholder và thuật ngữ của file strings.po
"""

import os
import sys
import re
import argparse

# Import polib từ thư mục game
GAME_STRINGS_DIR = '/Users/nam088/Downloads/Oxygen-Not-Included-AnkerGames/OxygenNotIncluded/OxygenNotIncluded_Data/StreamingAssets/strings'
if GAME_STRINGS_DIR not in sys.path:
    sys.path.insert(0, GAME_STRINGS_DIR)

try:
    import polib
except ImportError:
    print("[-] Không tìm thấy thư viện polib. Vui lòng cài đặt: pip install polib")
    sys.exit(1)


class TranslationVerifier:
    def __init__(self, po_filepath):
        self.po_filepath = po_filepath
        self.po = polib.pofile(po_filepath)
        self.errors = []
        self.warnings = []
        self.stats = {
            'total': len(self.po),
            'translated': 0,
            'untranslated': 0,
            'link_tag_errors': 0,
            'placeholder_errors': 0,
            'formatting_errors': 0,
            'term_warnings': 0,
            'ui_length_warnings': 0
        }

    def extract_placeholders(self, text):
        return set(re.findall(r'\{[A-Za-z0-9_:]+\}', text))

    def extract_links(self, text):
        return set(re.findall(r'<link="([^"]+)">', text))

    def extract_html_tags(self, text):
        # Extract general tags like <b>, </b>, <i>, <color=...>, etc.
        raw_tags = re.findall(r'<[/]?[a-zA-Z0-9_=#\":\.\-]+>', text)
        clean_tags = []
        for t in raw_tags:
            # Skip link tags as they are verified separately
            if t.startswith('<link=') or t == '</link>':
                continue
            clean_tags.append(t)
        return clean_tags

    def verify_all(self):
        print(f"[*] Bắt đầu kiểm tra file: {self.po_filepath}")
        print(f"[*] Tổng số chuỗi trong file: {len(self.po):,}")

        untranslatable_brands = ['discord', 'steam workshop', 'klei fest', 'directx', 'opengl', 'vulkan', 'vsync']

        for idx, entry in enumerate(self.po):
            if not entry.msgstr or entry.msgstr.strip() == "":
                self.stats['untranslated'] += 1
                continue

            self.stats['translated'] += 1
            msgid = entry.msgid
            msgstr = entry.msgstr
            ctxt = entry.msgctxt or ""

            # 0. Kiểm tra Danh từ riêng / Thương hiệu không được dịch
            for b in untranslatable_brands:
                if b in msgid.lower() and b not in msgstr.lower():
                    warn_msg = f"[{ctxt}] Dịch mất thương hiệu/danh từ riêng '{b}'!"
                    self.warnings.append(warn_msg)

            # 1. Kiểm tra Placeholder ({0}, {1}, {Hotkey}, ...)
            orig_placeholders = self.extract_placeholders(msgid)
            trans_placeholders = self.extract_placeholders(msgstr)
            if orig_placeholders != trans_placeholders:
                missing = orig_placeholders - trans_placeholders
                extra = trans_placeholders - orig_placeholders
                err_msg = f"[{ctxt}] Sai Placeholder. Thiếu: {missing}, Thừa: {extra}"
                self.errors.append(err_msg)
                self.stats['placeholder_errors'] += 1

            # 2. Kiểm tra Link Tags (<link="ID">)
            orig_links = self.extract_links(msgid)
            trans_links = self.extract_links(msgstr)
            if orig_links != trans_links:
                missing_l = orig_links - trans_links
                extra_l = trans_links - orig_links
                err_msg = f"[{ctxt}] Hỏng thẻ Link. Thiếu link: {missing_l}, Thừa/Sai: {extra_l}"
                self.errors.append(err_msg)
                self.stats['link_tag_errors'] += 1

            # 3. Kiểm tra số lượng thẻ đóng/mở Rich Text (b, i, u, color...)
            orig_tags = self.extract_html_tags(msgid)
            trans_tags = self.extract_html_tags(msgstr)
            if len(orig_tags) != len(trans_tags):
                warn_msg = f"[{ctxt}] Chênh lệch thẻ định dạng HTML/Unity: Gốc có {len(orig_tags)} thẻ, Dịch có {len(trans_tags)} thẻ"
                self.warnings.append(warn_msg)
                self.stats['formatting_errors'] += 1

            # 4. Kiểm tra ký tự xuống dòng \n
            if msgid.count('\\n') != msgstr.count('\\n') and msgid.count('\n') != msgstr.count('\n'):
                warn_msg = f"[{ctxt}] Lệch số lượng ký tự xuống dòng (\\n)"
                self.warnings.append(warn_msg)

            # 5. Cảnh báo độ dài giao diện (UI Overflows)
            if 'STRINGS.UI.' in ctxt:
                if len(msgid) > 10 and len(msgstr) > len(msgid) * 1.8:
                    warn_msg = f"[{ctxt}] Chuỗi UI tiếng Việt quá dài (>1.8x gốc), nguy cơ tràn viền: '{msgstr[:40]}...'"
                    self.warnings.append(warn_msg)
                    self.stats['ui_length_warnings'] += 1

        self.print_report()

    def print_report(self):
        print("\n" + "=" * 60)
        print("          BÁO CÁO KẾT QUẢ THẨM ĐỊNH BẢN DỊCH ONI")
        print("=" * 60)
        print(f"Tổng số chuỗi      : {self.stats['total']:,}")
        print(f"Đã dịch (Translated): {self.stats['translated']:,}")
        print(f"Chưa dịch (Empty)  : {self.stats['untranslated']:,}")
        print("-" * 60)
        print(f"Lỗi Placeholder    : {self.stats['placeholder_errors']}")
        print(f"Lỗi Link Tags      : {self.stats['link_tag_errors']}")
        print(f"Lệch Rich Text Tags: {self.stats['formatting_errors']}")
        print(f"Cảnh báo UI Tràn   : {self.stats['ui_length_warnings']}")
        print("=" * 60)

        if self.errors:
            print("\n[!] DANH SÁCH LỖI NGHIÊM TRỌNG CẦN FIX (Tối đa 10 mẫu đầu tiên):")
            for e in self.errors[:10]:
                print(f"  ❌ {e}")
            if len(self.errors) > 10:
                print(f"  ... và còn {len(self.errors) - 10} lỗi khác.")
        else:
            print("\n✅ KHÔNG CÓ LỖI NGHIÊM TRỌNG NÀO VỀ CÚ PHÁP VÀ TAG!")

        if self.warnings:
            print(f"\n[⚠️] TỔNG SỐ CẢNH BÁO CẦN LƯU Ý: {len(self.warnings)}")
            for w in self.warnings[:5]:
                print(f"  ⚠️  {w}")


def main():
    parser = argparse.ArgumentParser(description="Xác minh tính đúng đắn của file PO Việt hóa ONI")
    parser.add_argument("po_file", nargs="?", default=f"{GAME_STRINGS_DIR}/strings_preinstalled_ko_klei.po", help="Đường dẫn file .po")
    args = parser.parse_args()

    if not os.path.isfile(args.po_file):
        print(f"[-] File không tồn tại: {args.po_file}")
        sys.exit(1)

    verifier = TranslationVerifier(args.po_file)
    verifier.verify_all()


if __name__ == '__main__':
    main()
