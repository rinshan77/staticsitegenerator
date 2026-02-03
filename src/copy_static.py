import os
import shutil


def copy_directory(source_dir: str, dest_dir: str) -> None:
    """
    Recursively copies everything from source_dir to dest_dir.
    First deletes dest_dir to ensure a clean copy.
    Logs each file copied.
    """
    # 1) Delete destination if it exists (clean copy)
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    # 2) Recreate destination root
    os.mkdir(dest_dir)

    # 3) Walk source and copy items
    for name in os.listdir(source_dir):
        src_path = os.path.join(source_dir, name)
        dst_path = os.path.join(dest_dir, name)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            # It's a directory
            print(f"Creating dir: {dst_path}")
            os.mkdir(dst_path)
            copy_directory(src_path, dst_path)
