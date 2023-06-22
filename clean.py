import sys
from pathlib import Path
import uuid
import shutil
import os

import clean_folder.normalize as norm

CATEGORIES = {
    "images": [".jpeg", ".png", ".jpg", ".svg", ".bmp"],
    "videos": [".avi", ".mp4", ".mov", ".mkv"],
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".xls", ".pptx"],
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "archives": [".zip", ".gz", ".tar"],
}

def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        # print(f"Make {target_dir}")
        target_dir.mkdir()
    # print(path.suffix)
    # print(target_dir.joinpath(f"{normalize(path.stem)}{path.suffix}"))
    new_name = target_dir.joinpath(f"{norm.normalize(file.stem)}{file.suffix}")
    if new_name.exists():
        new_name = new_name.with_name(f"{new_name.stem}-{uuid.uuid4()}{file.suffix}")
    file.rename(new_name)


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        print(item)
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)


def unpack_archive(path: Path) -> None:
    archive_folder = "archives"
    for item in path.glob(f"{archive_folder}/*"):
        filename = item.stem
        arh_dir = path.joinpath(path / archive_folder / filename)
        os.mkdir(arh_dir)
        shutil.unpack_archive(item, arh_dir)


def delete_empty_folders(path: Path):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"

    if not path.exists():
        return f"Folder with path {path} doesn`t exists."

    sort_folder(path)
    delete_empty_folders(path)
    unpack_archive(path)

    return "All ok"


if __name__ == "__main__":
    print(main())
