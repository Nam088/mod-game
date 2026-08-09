import os

p = r"D:\mod-game\Timberborn\Mods\VietnameseLanguage\Localizations"

print("Files in Timberborn mod Localizations:")
if os.path.exists(p):
    for f in os.listdir(p):
        print(" -", f)
