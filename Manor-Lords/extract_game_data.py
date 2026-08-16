import os
import shutil
import subprocess
import glob

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(CURRENT_DIR, "tools")
EXTRACTED_DIR = os.path.join(CURRENT_DIR, "extracted")
REPAK_EXE = os.path.join(TOOLS_DIR, "repak.exe")

# Fallback path if not present in tools yet
SCRATCH_REPAK = r"C:\Users\nam\.gemini\antigravity\brain\a232faf3-641a-4f84-a781-167973ba568b\scratch\tools\repak.exe"

GAME_PAKS_DIR = r"C:\Users\nam\Downloads\Compressed\Manor-Lords-AnkerGames_2\Manor Lords\ManorLords\Content\Paks"
AES_KEY = "0xD7D2FFA2744D18A7B84DFF09591C212C2068413A23BA3967F9890A6654989321"

def ensure_tools():
    os.makedirs(TOOLS_DIR, exist_ok=True)
    if not os.path.exists(REPAK_EXE) and os.path.exists(SCRATCH_REPAK):
        shutil.copy2(SCRATCH_REPAK, REPAK_EXE)
        print(f"Copied repak.exe to {REPAK_EXE}")

def extract_translation_and_fonts():
    ensure_tools()
    os.makedirs(EXTRACTED_DIR, exist_ok=True)
    
    print("Extracting Translation assets from game PAKs...")
    # pakchunk0_s16 contains Translation assets
    s16_pak = os.path.join(GAME_PAKS_DIR, "pakchunk0_s16-Windows.pak")
    if os.path.exists(s16_pak):
        cmd = [REPAK_EXE, "--aes-key", AES_KEY, "unpack", "-o", EXTRACTED_DIR, "-f", s16_pak]
        subprocess.run(cmd, check=True)
        print("Successfully extracted pakchunk0_s16-Windows.pak")
    
    # pakchunk0_s18 contains font assets
    s18_pak = os.path.join(GAME_PAKS_DIR, "pakchunk0_s18-Windows.pak")
    if os.path.exists(s18_pak):
        cmd = [REPAK_EXE, "--aes-key", AES_KEY, "unpack", "-o", EXTRACTED_DIR, "-f", s18_pak]
        subprocess.run(cmd, check=True)
        print("Successfully extracted pakchunk0_s18-Windows.pak")

if __name__ == "__main__":
    extract_translation_and_fonts()
