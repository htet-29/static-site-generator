import os
import shutil


def copy_static_files(src_dir_path, dest_dir_path):
    if os.path.exists(dest_dir_path):
        shutil.rmtree(dest_dir_path)
    copy_files_recursive(src_dir_path, dest_dir_path)


def copy_files_recursive(src_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    if not os.path.exists(src_dir_path):
        raise ValueError("there is no source directory")
    files = os.listdir(src_dir_path)
    for filename in files:
        from_path = os.path.join(src_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)
