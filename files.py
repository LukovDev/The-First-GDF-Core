#
# files.py - Создаёт возможность работать с файлами.
#


# Импортируем:
import json
import pygame


# ------------------------------------------------ PyGame IMAGE: -------------------------------------------------------
# Загружаем pygame изображение:
def LoadPyGameImage(file_path: str) -> pygame.Surface | bool:
    try:
        image = pygame.image.load(file_path)
    except Exception as error:
        return False
    return image


# Сохраняем pygame изображение:
def SavePyGameImage(file_path: str, pygame_surface: pygame.Surface) -> bool:
    try:
        pygame.image.save(pygame_surface, file_path)
    except Exception as error:
        return False
    return True
# ----------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------- FILE: ------------------------------------------------------------
# Загружаем файл:
def LoadFile(file_path: str, mode="r+") -> str | bool:
    try:
        with open(file_path, mode, encoding="utf-8") as f:
            file = str(f.read())
    except Exception as error:
        return False
    return file


# Сохраняем файл:
def SaveFile(file_path: str, data: str, mode="w+") -> bool:
    try:
        with open(file_path, mode, encoding="utf-8") as f:
            f.write(data)
    except Exception as error:
        return False
    return True
# ----------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------ JSON: ---------------------------------------------------------
# Загружаем json файл:
def LoadJsonFile(file_path: str, mode="r+") -> dict | bool:
    try:
        with open(file_path, mode, encoding="utf-8") as f:
            file = dict(json.load(f))
    except Exception as error:
        return False
    return file


# Сохраняем json файл:
def SaveJsonFile(file_path: str, data: dict, mode="w+") -> bool:
    try:
        with open(file_path, mode, encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as error:
        return False
    return True
# ----------------------------------------------------------------------------------------------------------------------
