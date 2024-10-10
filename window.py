#
# window.py - Создаёт класс окна.
#


# Импортируем:
import glm
import sys
import pygame
from datetime import datetime
from OpenGL.GL import *


# Переменные:
__time_in_start__ = datetime.now()


# Класс окна:
class Window:
    def __init__(self,
                 next_class: any,
                 title="Window",
                 icon=None,
                 size=(960, 540),
                 vsync=False,
                 fps=60
                 ) -> None:
        self.WinWidth = size[0]              # Высота окна.
        self.WinHeight = size[1]             # Ширина окна.
        self.WinTitle = title                # Заголовок окна.
        self.WinIcon = icon                  # Иконка окна.
        self.WinVSync = vsync                # Вертикальная синхронизация.
        self.NextClass = next_class          # Наследующий класс этого класса (передайте сюда self).
        self.WinClock = pygame.time.Clock()  # Класс часов окна.
        self.WinFPS = fps                    # FPS окна.
        self.SettledFPS = fps                # Установленный FPS.
        self.__old_window_size = (0, 0)      # Старый размер окна. То-бишь размер окна в прошлой итерации цикла.

    # Открыть окно:
    def RunWindow(self) -> None:
        global __time_in_start__
        __time_in_start__ = datetime.now()
        
        pygame.display.set_caption(self.WinTitle)
        if self.WinIcon is not None:
            pygame.display.set_icon(self.WinIcon)
        v = 0
        if self.WinVSync:
            v = 1
        pygame.display.set_mode((self.WinWidth, self.WinHeight),
                                pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE, vsync=v)

        self.NextClass.Start()
        self.MainLoop()  # Запускаем цикл.

    # Цикл окна. Без него, окно не будет работать,
    # как и всё остальное что требует постоянного обновления, по типу игровой физики, отрисовки и тд:
    def MainLoop(self) -> None:
        global __time_in_start__
        while True:
            # Цикл, собирающий события:
            events = []
            for event in pygame.event.get():
                events.append(event)

                # Если программу хотят закрыть:
                if event.type == pygame.QUIT:
                    self.Exit()

            # Проверка на то, изменился ли размер окна или нет:
            if self.__old_window_size != pygame.display.get_window_size():
                self.__old_window_size = pygame.display.get_window_size()
                self.NextClass.ReSize(width=self.GetWinSize()[0], height=self.GetWinSize()[1])

            self.NextClass.Update(events)

    # Вызовите, когда хотите закрыть окно:
    def Exit(self) -> None:
        t = str(datetime.now() - __time_in_start__)[:-7]
        if len(t[0:1]) == 1:
            t = f"0{t}"
        self.NextClass.Destroy()
        
        pygame.quit()
        sys.exit()

    # ------------------------------------- Основные функции наследуемого класса: --------------------------------------
    # Вызывается один раз после создания окна и перед циклом:
    def Start(self) -> None:
        pass

    # Цикл окна:
    def Update(self, events: list) -> None:
        pass

    # Вызывается при изменении размера окна:
    def ReSize(self, width: int, height: int) -> None:
        pass

    # Вызывается при закрытии окна:
    def Destroy(self) -> None:
        pass
    # ------------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------- Функции окна: -----------------------------------------------------
    # Установить размер окна:
    def SetWinSize(self, width: int, height: int) -> None:
        self.WinWidth = width
        self.WinHeight = height
        v = 0
        if self.WinVSync:
            v = 1
        pygame.display.set_mode((self.WinWidth, self.WinHeight),
                                pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE, vsync=v)

    # Получить размер окна:
    def GetWinSize(self) -> tuple:
        return pygame.display.get_window_size()

    # Установить заголовок окна:
    def SetWinTitle(self, title: str) -> None:
        self.WinTitle = title
        pygame.display.set_caption(title)

    # Получить заголовок окна:
    def GetWinTitle(self) -> str:
        return self.WinTitle

    # Установить иконку окну:
    def SetWinIcon(self, icon: pygame.image) -> None:
        self.WinIcon = icon
        pygame.display.set_icon(icon)

    # Получить иконку окна:
    def GetWinIcon(self) -> pygame.image:
        return self.WinIcon

    # Установить VSync:
    def SetWinVSync(self, is_vsync: bool) -> None:
        v = 0
        if is_vsync:
            v = 1
        self.WinVSync = is_vsync
        pygame.display.set_mode(self.GetWinSize(), pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE, vsync=v)

    # Получить VSync:
    def GetWinVSync(self) -> bool:
        return self.WinVSync

    # Получить дельту времени:
    def GetDeltaTime(self) -> float:
        fps = self.GetWinFPS()
        if fps > 0:
            return 1 / self.GetWinFPS()
        else:
            return 0

    # Установить FPS:
    def SetWinFPS(self, fps: int) -> None:
        self.SettledFPS = fps

    # Получить FPS окна:
    def GetWinFPS(self) -> float:
        return self.WinClock.get_fps()

    # Установить позицию мыши:
    def SetMousePos(self, pos: tuple | list | glm.vec2) -> None:
        if type(pos) == glm.vec2:
            pygame.mouse.set_pos(pos.x, pos.y)
        else:
            pygame.mouse.set_pos(pos[0], pos[1])

    # Установить позицию мыши:
    def GetMousePos(self) -> tuple | list:
        return pygame.mouse.get_pos()

    # Получить время:
    def GetTime(self) -> float:
        return pygame.time.get_ticks() / 1000

    # Очистка окна:
    def Clear(self, red=0, green=0, blue=0) -> None:
        glClearColor(red/255, green/255, blue/255, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Отрисовка окна:
    def Render(self) -> None:
        pygame.display.flip()
        if self.WinVSync:
            self.WinClock.tick(60)
        elif self.SettledFPS <= 0:
            self.WinClock.tick(8192)
        else:
            self.WinClock.tick(self.SettledFPS)
    # ------------------------------------------------------------------------------------------------------------------
