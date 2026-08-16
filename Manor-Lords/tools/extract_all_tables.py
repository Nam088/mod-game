import os
import struct
import json
import glob

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HOOD_DIR = os.path.join(CURRENT_DIR, "..", "extracted", "ManorLords", "Content", "Translation", "HoodedHorse")
TRANS_DIR = os.path.join(CURRENT_DIR, "..", "translations")
os.makedirs(TRANS_DIR, exist_ok=True)

def extract_strings_from_uexp(uexp_path):
    with open(uexp_path, "rb") as f:
        data = f.read()
    
    pos = 0
    extracted = []
    # Search for FString: length (int32) followed by string bytes and \0
    while pos < len(data) - 4:
        length, = struct.unpack_from("<i", data, pos)
        if 1 < length < 2000 and pos + 4 + length <= len(data):
            s_bytes = data[pos+4:pos+4+length]
            if s_bytes[-1] == 0:
                try:
                    s = s_bytes[:-1].decode("utf-8")
                    # Filter out binary junk or non-displayable strings
                    if len(s) >= 1 and not any(ord(c) < 32 and c not in '\r\n\t' for c in s):
                        extracted.append({
                            "offset": pos,
                            "length": length,
                            "text": s
                        })
                        pos += 4 + length - 1
                except:
                    pass
        pos += 1
    return extracted

def scan_all_tables():
    uexp_files = sorted(glob.glob(os.path.join(HOOD_DIR, "*.uexp")))
    total_strings = 0
    summary = {}
    
    for uexp in uexp_files:
        name = os.path.splitext(os.path.basename(uexp))[0]
        items = extract_strings_from_uexp(uexp)
        summary[name] = len(items)
        total_strings += len(items)
        
        # Save raw extraction to JSON for inspection
        json_out = os.path.join(TRANS_DIR, f"{name}.json")
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
            
    print(f"Scanned {len(uexp_files)} tables, total string occurrences: {total_strings}")
    for name, count in summary.items():
        print(f"  {name:35s}: {count:5d} strings")

if __name__ == "__main__":
    scan_all_tables()
