import os
import shutil

def move_svs_files():
    """
    Moves all .svs files from subfolders within 'all_svs_files' to the current working directory.
    """
    current_dir = os.getcwd()
    source_dir = os.path.join(current_dir, 'all_svs_files')
    
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return
    
    subfolders = [f for f in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, f))]
    moved_files = 0
    
    for subfolder in subfolders:
        subfolder_path = os.path.join(source_dir, subfolder)
        files = [f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))]
        svs_files = [f for f in files if f.lower().endswith('.svs')]
        
        for svs_file in svs_files:
            source_path = os.path.join(subfolder_path, svs_file)
            destination_path = os.path.join(current_dir, svs_file)
            
            if os.path.exists(destination_path):
                print(f"File '{svs_file}' already exists in the destination. Skipping.")
                continue
            
            try:
                shutil.move(source_path, destination_path)
                print(f"Moved '{svs_file}' to '{current_dir}'.")
                moved_files += 1
            except Exception as e:
                print(f"Error moving '{svs_file}': {e}")
    
    print(f"Total files moved: {moved_files}")

if __name__ == "__main__":
    move_svs_files()
