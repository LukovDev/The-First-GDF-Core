#
# camera.py - Создаёт класс камеры.
#


# Импортируем:
import glm
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


# Переменные:
up_down_angle = 0
old_mouse_pos = [0, 0]


# Класс камеры:
class Camera3D:
    def __init__(self,
                 width: int,
                 height: int,
                 position=glm.vec3(0),
                 rotation=glm.vec3(0),
                 fov=60,
                 far=1000.0,
                 near=0.1) -> None:
        self.position = position             # Позиция камеры.
        self.rotation = rotation             # Вращение камеры.
        self.width = width                   # Высота камеры.
        self.height = height                 # Ширина камеры.
        self.fov = fov                       # Угол обзора.
        self.far = far                       # Дальнее отсечение.
        self.near = near                     # Ближнее отсечение.
        self.view_matrix = [[], [], [], []]  # Матрица вида.

        self.rotation = self.CheckRotateVector(self.rotation)
        if self.fov > 179:
            self.fov = 179
        if self.fov < 1:
            self.fov = 1
        if self.far < 1:
            self.far = 1
        if self.near < 0.0001:
            self.near = 0.0001
        glEnable(GL_DEPTH_TEST)  # Включаем глубину для 3D.
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, width, height)
        gluPerspective(fov, float(width) / height, near, far)
        self.view_matrix = [[], [], [], []]

    # Обновление камеры:
    def Update(self) -> None:
        self.rotation = self.CheckRotateVector(self.rotation)

        if self.fov > 179:
            self.fov = 179
        if self.fov < 1:
            self.fov = 1
        if self.far < 1:
            self.far = 1
        if self.near < 0.0001:
            self.near = 0.0001

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, self.width, self.height)
        gluPerspective(self.fov, float(self.width) / self.height, self.near, self.far)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()  # Сбрасываем матрицу.
        glRotatef(self.rotation.x, 1, 0, 0)  # Вращаем камеру по X-оси.
        glRotatef(self.rotation.y, 0, 1, 0)  # Вращаем камеру по Y-оси.
        glRotatef(self.rotation.z, 0, 0, 1)  # Вращаем камеру по Z-оси.
        glTranslatef(-self.position.x, -self.position.y, -self.position.z)

    # Изменение размера камеры при изменении размера окна:
    def ReSize(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, self.width, self.height)
        gluPerspective(self.fov, float(self.width) / self.height, self.near, self.far)

    # Предотвращает переполнение угла в векторе вращения:
    def CheckRotateVector(self, rotate_vec3: glm.vec3) -> glm.vec3:
        # Ограничение размера поворота (по умолчанию, оси могут выходить за 360/-360 градусов):
        if rotate_vec3.x > 360:
            rotate_vec3.x = rotate_vec3.x - 360
        if rotate_vec3.x < 0:
            rotate_vec3.x = 360 + rotate_vec3.x
        if rotate_vec3.y > 360:
            rotate_vec3.y = rotate_vec3.y - 360
        if rotate_vec3.y < 0:
            rotate_vec3.y = 360 + rotate_vec3.y
        if rotate_vec3.z > 360:
            rotate_vec3.z = rotate_vec3.z - 360
        if rotate_vec3.z < 0:
            rotate_vec3.z = 360 + rotate_vec3.z
        return rotate_vec3


# Функция, которая заставляет камеру редактора свободно вращаться:
def FreeCameraEditor(camera3d: Camera3D, delta_time: float, win_size: tuple[int, int] | list[int, int],
                     speed: float, speed_shift: float, mouse_sensitivity: float) -> None:
    global up_down_angle, old_mouse_pos

    camera3d.position.xyz = (0, 0, 0)
    camera3d.rotation.xyz = (0, 0, 0)

    mouse_move = [pygame.mouse.get_pos()[0] - old_mouse_pos[0],
                  pygame.mouse.get_pos()[1] - old_mouse_pos[1]]
    old_mouse_pos = pygame.mouse.get_pos()

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # При нажатии пкм:
    if pygame.mouse.get_pressed()[2]:
        # Вращение вверх и вниз:
        up_down_angle += mouse_move[1] * mouse_sensitivity
    glRotatef(up_down_angle, 1.0, 0.0, 0.0)
    glPushMatrix()
    glLoadIdentity()

    # При нажатии пкм:
    if pygame.mouse.get_pressed()[2]:
        # Шифт = доп.скорость:
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            speed = speed_shift

        # Вперёд назад:
        if pygame.key.get_pressed()[pygame.K_w]:
            glTranslatef(0, 0, speed * (delta_time * 60))
        if pygame.key.get_pressed()[pygame.K_s]:
            glTranslatef(0, 0, -speed * (delta_time * 60))

        # Влево вправо:
        if pygame.key.get_pressed()[pygame.K_a]:
            glTranslatef(speed * (delta_time * 60), 0, 0)
        if pygame.key.get_pressed()[pygame.K_d]:
            glTranslatef(-speed * (delta_time * 60), 0, 0)

        # Вверх-вниз:
        if pygame.key.get_pressed()[pygame.K_q]:
            glTranslatef(0, speed * (delta_time * 60), 0)
        if pygame.key.get_pressed()[pygame.K_e]:
            glTranslatef(0, -speed * (delta_time * 60), 0)

        # Вращение влево и вправо:
        glRotatef(mouse_move[0] * mouse_sensitivity, 0.0, 1.0, 0.0)

        # Если курсор приближается к краю окна, передвинуть его в другую часть окна:
        x_pos_detect = 92
        y_pos_detect = 92
        if pygame.mouse.get_pos()[0] < x_pos_detect:
            pygame.mouse.set_pos((win_size[0] - x_pos_detect, pygame.mouse.get_pos()[1]))
        if pygame.mouse.get_pos()[0] > win_size[0] - x_pos_detect:
            pygame.mouse.set_pos((x_pos_detect, pygame.mouse.get_pos()[1]))
        if pygame.mouse.get_pos()[1] < y_pos_detect:
            pygame.mouse.set_pos((pygame.mouse.get_pos()[0], win_size[1] - y_pos_detect))
        if pygame.mouse.get_pos()[1] > win_size[1] - y_pos_detect:
            pygame.mouse.set_pos((pygame.mouse.get_pos()[0], y_pos_detect))

        old_mouse_pos = pygame.mouse.get_pos()
    glMultMatrixf(camera3d.view_matrix)
    camera3d.view_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    glPopMatrix()
    glMultMatrixf(camera3d.view_matrix)
