import os
import zipfile

def extract_exact_en_files_timberborn(game_dir=r"C:\Users\nam\Downloads\Compressed\Timberborn-AnkerGames"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "Extracted_EN")
    os.makedirs(output_dir, exist_ok=True)

    zip_path = os.path.join(game_dir, "Timberborn", "Timberborn_Data", "StreamingAssets", "Modding", "Localizations.zip")
    
    if not os.path.exists(zip_path):
        print(f"Error: {zip_path} not found!")
        return

    print(f"Extracting separate English files from game zip: {zip_path}")
    en_files = ["enUS.csv", "enUS_names.csv", "enUS_donottranslate.csv", "enUS_wip.csv"]
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_name in en_files:
            if file_name in zip_ref.namelist():
                zip_ref.extract(file_name, output_dir)
                print(f"  -> Extracted: {os.path.join(output_dir, file_name)}")
            else:
                # Create empty file if not in zip
                open(os.path.join(output_dir, file_name), 'w', encoding='utf-8').close()
                print(f"  -> Created empty placeholder: {file_name}")

    print(f"\nSuccessfully extracted exact individual English CSV files to: {output_dir}")

if __name__ == "__main__":
    extract_exact_en_files_timberborn()
