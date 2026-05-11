import os
import shutil

def organize_folder(target_path):
    # Define categories and their extensions
    extensions = {
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
        "Videos": [".mp4", ".mkv", ".mov"],
        "Archives": [".zip", ".tar", ".rar"]
    }

    for filename in os.listdir(target_path):
        file_path = os.path.join(target_path, filename)
        
        # Skip directories, only process files
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1].lower()
            
            for category, exts in extensions.items():
                if file_ext in exts:
                    dest_dir = os.path.join(target_path, category)
                    os.makedirs(dest_dir, exist_ok=True)
                    shutil.move(file_path, os.path.join(dest_dir, filename))
                    print(f"Moved: {filename} -> {category}")

# Example usage (be careful with the path!)
# organize_folder("/Users/YourName/Downloads")
