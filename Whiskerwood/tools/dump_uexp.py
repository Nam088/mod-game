with open(r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_En.uexp", "rb") as f:
    uexp = f.read()

for i in range(0, 160, 16):
    chunk = uexp[i:i+16]
    hex_str = " ".join(f"{b:02x}" for b in chunk)
    ascii_str = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
    print(f"{i:04x}:  {hex_str:<48}  {ascii_str}")
