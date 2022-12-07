import shutil
import sys
import os
from datetime import datetime
from threading import Thread, Lock
from concurrent import futures

map = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
    'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
    'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
    'э': 'e', 'ю': 'yu', 'я': 'ya', 'і': 'i', 'є': 'e', 'ї': 'i',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
    'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
    'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
    'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', 'І': 'I', 'Є': 'E', 'Ї': 'I'
}

types = {
    'images': ['jpeg', 'png', 'jpg', 'svg', 'webp'],
    'video': ['avi', 'mp4', 'mov', 'mkv'],
    'documents': ['doc', 'docx', 'txt', 'pdf', 'xls', 'xlsx', 'pptx'],
    'audio': ['mp3', 'ogg', 'mov', 'amr'],
    'archives': ['zip', 'gz', 'tar']
}

name_folder = ''
lock = Lock()

pool = futures.ThreadPoolExecutor(200)

def get_dir_name():
    work_dir = ''
    args = sys.argv
    if len(args) == 1:
        work_dir = input('Enter path to directory: ')   
    else:
        work_dir = args[1]
    while True:
        if not os.path.exists(work_dir):
            if work_dir:
                print(f'{work_dir} is not exist')
            work_dir = input('Enter path to directory: ')
        else:
            if os.path.isdir(work_dir):
                break
            else:
                print(f'{work_dir} is not a directory')
                work_dir = ''
    return work_dir

def read_dir(namedir):
    return os.listdir(namedir)

def check_file_type(file):
    file_name_arr = file.split('.')
    file_ext = ''
    if len(file_name_arr) > 1:
        file_ext = file_name_arr[-1]
    if not file_ext:
        return None
    else:
        for key, val in types.items():
            if file_ext.lower() in val:
                return key
        return None

def rename_file(folder_to, folder_from, file):
    global name_folder
    path_to = os.path.join(name_folder, folder_to)
    if not os.path.exists(path_to):
        os.makedirs(path_to)
    if folder_to != 'archives':
        try:
            os.rename(os.path.join(folder_from, file), os.path.join(path_to, normalize(file)))
        except FileExistsError:
            print(f'File {file} is already exist')
            while True:
                is_rewrite = input(f'Do you want to rewrite file {file} (y/n)').lower()
                if is_rewrite == 'y':
                    os.replace(os.path.join(folder_from, file), os.path.join(path_to, normalize(file)))
                    break
                elif is_rewrite == 'n':
                    os.rename(os.path.join(folder_from, file), os.path.join(path_to, normalize(file, True)))
                    break

    else:
        f = normalize(file).split('.')
        try:
            shutil.unpack_archive(os.path.join(folder_from, file), os.path.join(path_to, f[0]), f[1])
        except shutil.ReadError:
            print(f"Archive {os.path.join(folder_from, file)} can't be unpack")
        else:
            os.remove(os.path.join(folder_from, file))
    
def normalize(file, is_copy = False):
    lists = file.split('.')
    name_file = '.'.join(lists[0:-1])
    new_name = ''
    for el in name_file:
        if el in map:
            new_name += map[el]
        elif el.isalnum():
            new_name += el
        else:
            new_name += '_'
    if is_copy:
        new_name += f'_(copy_{datetime.now().microsecond})'
    return new_name + '.' + lists[-1]

def sorting_folder(namedir):
    lists = read_dir(namedir)
    for el in lists:
        path_file = os.path.join(namedir, el)
        if os.path.isdir(path_file):
            pool.submit(sorting_folder, path_file)
        else:
            folder = check_file_type(el)
            if folder:
                pool.submit(rename_file, folder, namedir, el)

def check_clear_folder(namedir):
    is_remove = False
    lists = os.listdir(namedir)
    if not lists:
        os.rmdir(namedir)
        return True
    else:
        for el in lists:
            path_el = os.path.join(namedir, el)
            if os.path.isdir(path_el):
                if check_clear_folder(path_el):
                    is_remove = True
        if is_remove:
            check_clear_folder(namedir)
            return True

def main():
    global name_folder
    name_folder = get_dir_name()
    sorting_folder(name_folder)
    pool.shutdown(wait=True)
    check_clear_folder(name_folder)
 
if __name__ == '__main__':
    main()
    
