import os
import shutil
from pathlib import Path
import schedule
import time

# 1/sset the folder you want to organize
TARGET_FOLDER = Path(r"./ToOrganize")  #Change to your desired folder path

# 2/define the types of files and their extensions
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "PDFs": [".pdf"],
    "Documents": [".doc", ".docx", ".txt", ".xls", ".xlsx"],
}


def create_folders():
    """Create folders based on the keys in FILE_TYPES dict."""
    TARGET_FOLDER.mkdir(parents=True, exist_ok=True)
    for folder in FILE_TYPES:
        folder_path = TARGET_FOLDER / folder
        folder_path.mkdir(exist_ok=True)


def organize_files():
    """Move files into their respective folders."""
    for file in TARGET_FOLDER.iterdir():
        if file.is_file():
            moved = False
            for folder_name, extensions in FILE_TYPES.items():
                if file.suffix.lower() in extensions:
                    dest_folder = TARGET_FOLDER / folder_name
                    dest_file = dest_folder / file.name

                    # this for avoid overwriting existing files
                    if dest_file.exists():
                        base, ext = os.path.splitext(file.name)
                        dest_file = dest_folder / f"{base}_copy{ext}"

                    shutil.move(str(file), str(dest_file))
                    print(f"Moved: {file.name} → {folder_name}")
                    moved = True
                    break
            if not moved:
                print(f"Skipped: {file.name} (no matching type)")


def run_organizer():
    print("Organizing files...")
    create_folders()
    organize_files()
    print("Done!")


if __name__ == "__main__":
    run_organizer()

    #enable the scheduler if needed
    schedule.every().monday.at("10:00").do(run_organizer)
    print("🕒 Scheduler started...")

    while True:
        schedule.run_pending()
        time.sleep(60)
