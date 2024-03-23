import os
import time
import random

def test():
    print("Helper test")

def generate_filename(path):
    ext = get_file_extension(path)
    timestamp = str(time.time())
    timestamp = timestamp.replace(".", "_")
    return f"{timestamp}.{ext}"


def get_file_extension(file_path):
    # Извлечь расширение файла из пути
    _, file_extension = os.path.splitext(file_path)
    
    # Удалить точку из расширения (если она присутствует)
    file_extension = file_extension[1:] if file_extension.startswith('.') else file_extension
    
    return file_extension


def get_file_name(file_path):
    # Извлечь имя файла из полного пути
    file_name = os.path.basename(file_path)
    name, _ = os.path.splitext(file_name)
    #r = file_name.rsplit(".")
    return name


def get_file_directory(file_path):
    # Извлечь директорию из полного пути к файлу
    directory = os.path.dirname(file_path)
    
    return directory


def delete_file(file_path):
    # Удалить файл
    try:
        os.remove(file_path)
        print("Файл удален успешно.")
    except OSError as e:
        print(f"Ошибка при удалении файла: {e}")


# Поучить случайный параметр из диапазона
def get_random_parametr(param):
    if param == "" or param == None:
        return None
    
    if isinstance(param, list):
        random.shuffle(param)
        return param[0]
    
    if isinstance(param, int) == True:
        return param
    
    p = param.split("-")
    if len(p) == 1:
        return param
    
    if p[0].isdigit() != True or p[1].isdigit() != True:
        return None
    return random.randint(int(p[0]), int(p[1]))