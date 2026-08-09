import os

p = r"C:\Users\nam\Documents\Timberborn\Mods\VietnameseLanguage\Localizations"

print("Files in VietnameseLanguage/Localizations:")
if os.path.exists(p):
    for f in os.listdir(p):
        print(f)
