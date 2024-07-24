# file_operations.py

import os
import shutil

def create_file(filepath, content=''):
    """Létrehoz egy új fájlt a megadott tartalommal."""
    with open(filepath, 'w') as file:
        file.write(content)

def delete_file(filepath):
    """Törli a megadott fájlt."""
    if os.path.isfile(filepath):
        os.remove(filepath)
    else:
        raise FileNotFoundError(f"{filepath} nem található")

def rename_file(old_filepath, new_filepath):
    """Átnevezi a megadott fájlt."""
    if os.path.isfile(old_filepath):
        os.rename(old_filepath, new_filepath)
    else:
        raise FileNotFoundError(f"{old_filepath} nem található")

def list_files(directory):
    """Visszaadja a megadott könyvtárban található fájlokat és könyvtárakat."""
    if os.path.isdir(directory):
        return os.listdir(directory)
    else:
        raise FileNotFoundError(f"{directory} nem található")

def copy_file(source, destination):
    """Másolja a fájlt a megadott célba."""
    if os.path.isfile(source):
        shutil.copy(source, destination)
    else:
        raise FileNotFoundError(f"{source} nem található")

def create_directory(directory_path):
    """Létrehoz egy új könyvtárat."""
    os.makedirs(directory_path, exist_ok=True)

def delete_directory(directory_path):
    """Törli a megadott könyvtárat és annak tartalmát."""
    if os.path.isdir(directory_path):
        shutil.rmtree(directory_path)
    else:
        raise FileNotFoundError(f"{directory_path} nem található")
    
def list_files_and_dirs(directory):
    """Visszaadja a megadott könyvtárban található fájlokat és könyvtárakat."""
    if os.path.isdir(directory):
        return os.listdir(directory)
    else:
        raise FileNotFoundError(f"{directory} nem található")