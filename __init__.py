#
# __init__.py - Играет роль основного кода от лица папки.
#


# Скрипты:
from . import camera
from . import files
from . import window


# Получить версию ядра:
def GetVersion() -> str:
    return "v0.1-a"
