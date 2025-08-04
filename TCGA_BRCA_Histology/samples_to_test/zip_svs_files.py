import os
import zipfile

def zip_svs_files(root_dir):
    single_zip_path = os.path.join(root_dir, 'all_svs_files.zip')
    files_to_zip = []
    
    for subdir in os.listdir(root_dir):
        subdir_path = os.path.join(root_dir, subdir)
        if os.path.isdir(subdir_path):
            for file in os.listdir(subdir_path):
                file_path = os.path.join(subdir_path, file)
                if os.path.isfile(file_path) and file.endswith('.svs'):
                    # Delete the corresponding zip file if it exists
                    zip_file_name = file + '.zip'
                    zip_file_path = os.path.join(subdir_path, zip_file_name)
                    if os.path.exists(zip_file_path):
                        os.remove(zip_file_path)
                        print(f"Deleted {zip_file_path}")
                    # Collect the file to be zipped
                    relative_path = os.path.relpath(file_path, root_dir)
                    files_to_zip.append((file_path, relative_path))
    
    if not files_to_zip:
        print("No .svs files found.")
    else:
        with zipfile.ZipFile(single_zip_path, 'w', compression=zipfile.ZIP_STORED) as zipf:
            for full_path, rel_path in files_to_zip:
                zipf.write(full_path, arcname=rel_path)
                print(f"Added {rel_path} to {single_zip_path}")
        print(f"Single zip file created: {single_zip_path}")

if __name__ == "__main__":
    root_directory = '.'
    zip_svs_files(root_directory)
