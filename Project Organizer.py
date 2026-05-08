import os

def bulk_rename(folder_path, base_name):
    # 1. Change to the target directory
    try:
        os.chdir(folder_path)
    except FileNotFoundError:
        print("Error: Folder not found.")
        return

    # 2. Get a list of files and sort them (to keep order)
    files = [f for f in os.listdir() if os.path.isfile(f)]
    files.sort()

    print(f"Renaming {len(files)} files...")

    # 3. Loop with a counter
    for index, filename in enumerate(files, start=1):
        # Split the name and the extension (e.g., 'photo', '.jpg')
        extension = os.path.splitext(filename)[1]
        
        # Create the new name with padding (01, 02 instead of 1, 2)
        # :02d means "integer, 2 digits wide, fill with zero"
        new_name = f"{base_name}_{index:02d}{extension}"
        
        # 4. Rename the file
        os.rename(filename, new_name)
        print(f"Renamed: {filename} -> {new_name}")

# Example Usage:
# bulk_rename("C:/Photos/Italy2024", "Italy_Vacation")
