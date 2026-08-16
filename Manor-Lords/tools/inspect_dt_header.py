import struct

uexp_path = r"d:\mod-game\Manor-Lords\extracted\ManorLords\Content\Translation\HoodedHorse\DT_Translation_BuildingNames.uexp"

with open(uexp_path, "rb") as f:
    data = f.read()

# UE4/UE5 DataTable Export serialized binary:
# Header: 4 bytes (zeros or table header)
# NumRows: int32 (number of rows)
# For each row:
#   RowName: FName (Index int32, Number int32)
#   Row Struct Data (Properties serialized)

print("First 32 bytes of uexp:")
print(data[:32].hex())
num_rows, = struct.unpack_from("<i", data, 4)
print(f"NumRows at offset 4: {num_rows}")
