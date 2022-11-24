import pygame as pg
from solar_vis import *
from solar_model import *
from solar_input import *
from solar_objects import *
import thorpy
import time
import numpy as np

timer = None

alive = True

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

model_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

time_scale = 1000.0
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""


def execution(delta):
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global model_time
    global displayed_time
    recalculate_space_objects_positions([dr.obj for dr in space_objects], delta)
    model_time += delta


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True


def pause_execution():
    global perform_execution
    perform_execution = False


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global alive
    alive = False


def open_file():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global browser
    global model_time

    model_time = 0.0
    in_filename = "solar_system.txt"
    space_objects = read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.obj.x), abs(obj.obj.y)) for obj in space_objects])
    calculate_scale_factor(max_distance)


def handle_events(events, menu):
    global alive
    for event in events:
        menu.react(event)
        if event.type == pg.QUIT:
            alive = False


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """

    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button
    global perform_execution
    global timer

    print('Modelling started!')
    physical_time = 0

    pg.init()

    width = 1000
    height = 900
    screen = pg.display.set_mode((width, height))
    last_time = time.perf_counter()
    drawer = Drawer(screen)
    menu, box, timer = init_ui(screen)
    perform_execution = True

    while alive:
        handle_events(pg.event.get(), menu)
        cur_time = time.perf_counter()
        if perform_execution:
            execution((cur_time - last_time) * time_scale)
            text = "%d seconds passed" % (int(model_time))
            timer.set_text(text)

        last_time = cur_time
        drawer.update(space_objects, box)
        time.sleep(1.0 / 60)

    print('Modelling finished!')


if __name__ == "__main__":
    main()