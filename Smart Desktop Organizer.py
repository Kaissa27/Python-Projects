import os 
import shutil
from pathlib import Path

def organize_folder(target_dir):
    # Define your directory categories
    TRACKED_EXTENSIONS = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
        "Archives": [".zip", ".tar", ".rar", ".gz"],
        "Installers": [".exe", ".dmg", ".msi"]
    }

    target_path = Path(target_dir)
    
    for item in target_path.iterdir():
        if item.is_file():
            file_ext = item.suffix.lower()
            moved = False
            
            # Find the correct category folder
            for category, extensions in TRACKED_EXTENSIONS.items():
                if file_ext in extensions:
                    dest_folder = target_path / category
                    dest_folder.mkdir(exist_ok=True) # Create folder if missing
                    
                    shutil.move(str(item), str(dest_folder / item.name))
                    print(f"Moved: {item.name} -> {category}/")
                    moved = True
                    break
            
            # Optional: Move unknown files to a "Misc" folder
            if not moved:
                misc_folder = target_path / "Misc"
                misc_folder.mkdir(exist_ok=True)
                shutil.move(str(item), str(misc_folder / item.name))

# Example usage:
# organize_folder("/Users/yourname/Downloads")
