import struct

with open(r"D:\code\mod-game\Whiskerwood\extracted\Whiskerwood\Content\Data\TextDB\Loc_En.uexp", "rb") as f:
    uexp = f.read()

footer_val, = struct.unpack_from("<I", uexp, len(uexp) - 4)
print(f"Original uexp footer int32: {footer_val} (hex: {hex(footer_val)})")
print(f"Original uasset size: {83348} (hex: {hex(83348)})")
