import os
import zipfile
import shutil as sh 
from typing import List

def extract_filtered_files(
    files_path: str,
    extract_path: str,
    pattern: str
) -> List[str]:
    
    final_path = extract_path + "_final"
    os.makedirs(extract_path, exist_ok=True)

    if os.path.exists(extract_path) and os.path.isdir(extract_path):
        sh.rmtree(extract_path)

    
    if os.path.exists(final_path) and os.path.isdir(final_path):
        sh.rmtree(final_path)

    for zip_file in os.listdir(files_path):
        if zip_file.endswith(".zip"):
            file = zip_file.removesuffix(".zip")
            extract_to = os.path.join(extract_path, file)
            os.makedirs(extract_to, exist_ok=True)
            with zipfile.ZipFile(os.path.join(files_path, zip_file), 'r') as zip_ref:
                zip_ref.extractall(extract_to)

    for dir in os.listdir(extract_path):
        full_name = os.path.join(extract_path, dir)
        if os.path.isdir(full_name) and os.listdir(full_name).count(dir) == 0:
            os.makedirs(final_path, exist_ok=True)
            sh.move(full_name, os.path.join(final_path, dir))

    for dir in os.listdir(extract_path):
        full_name = os.path.join(extract_path, dir)
        if os.path.isdir(full_name) and os.listdir(full_name).count(dir) > 0:
            os.makedirs(final_path, exist_ok=True)
            sh.move(os.path.join(full_name, dir), final_path)

    filterFiles_paths = []
    for root, dirs, files in os.walk(final_path):
        for file in files:
            if pattern in file:
                filterFiles_path = os.path.join(root, file)
                filterFiles_paths.append(filterFiles_path)

    return filterFiles_paths

def standard_hour(hour):
    hour = str(hour).replace("UTC", "").strip()

    if ':' in hour:
        hour = hour.replace(":", "")
    
    return hour