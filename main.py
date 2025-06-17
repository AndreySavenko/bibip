
# import json
# import os
from pathlib import Path
import models
import bibip_car_service
from models import write_row_in_file, read_row_in_file, write_file
from datetime import datetime as dt
from decimal import Decimal


# ROW_LENTS = 150  # длина строки для базы (без учета символа \n)


def read_file(path: str, nam: str):  # -> list:
    """ Читаем файл целиком. Возвращает список строк"""
    # p = Path(path)
    # print('Начинаем read_file:\n')
#    fullpath = f'{path.rstrip('/')}/{nam}'
#    p = Path(fullpath)
#    isfile = p.is_file()
#    if isfile:
#        mode = 'r'
#    else:
#        mode = 'w'   
    with open(f'{path.rstrip('/')}/{nam}',
              'r', encoding='utf-8') as f:
        lines = f.readlines()
        # print(lines)  # , type(lines))
    return lines


def init_car(text: str, delimiter: str) -> models.Car:
    """ Функция возвращает объект models.Car.
    Функция принимает строку с параметрами, разделенными delimiter,
    распаковываем строку в список, приводим параметры к нужным типам.
    """
    param = str.split(text, delimiter)
    dat = dt.strptime(param[3], '%Y-%m-%d')
    # print(dat, type(dat))
    if param[4] == 'available':
        status = models.CarStatus.available
    elif param[4] == 'reserve':
        status = models.CarStatus.reserve
    elif param[4] == 'delivery':
        status = models.CarStatus.delivery
    elif param[4] == 'sold':
        status = models.CarStatus.sold
    else:
        raise ValueError
    price = Decimal(str.replace(param[2], ',', '.'))
    car = models.Car(vin=param[0], model=int(param[1]), price=price, date_start=dat, status=status)

    return car


def init_model(text: str, delimiter: str) -> models.Model:
    """ Функция возвращает объект models.Model.
    Функция принимает строку с параметрами, разделенными delimiter,
    распаковываем строку в список, приводим параметры к нужным типам.
    """
    param = str.split(text, delimiter)
    model = models.Model(id=int(param[0]), name=param[1], brand=param[2])
    return model


def init_raw_files():
    path = 'src'
    # инициализируем класс CarService
    bibip = bibip_car_service.CarService(path)

    # Читаем сырой файл с машинами
    nam = 'raw_cars.txt'   
    f = read_file(path, nam)
    ln = len(f)
    for i in range(ln-1):
        car = init_car(f[i+1].strip('\n'), '\t')
        bibip.add_car(car)

    # Читаем сырой файл с моделями
    nam = 'raw_models.txt'
    fm = read_file(path, nam)
    ln = len(fm)
    for i in range(ln-1):
        # пример инициализации модели из сырого файла
        model = init_model(fm[i+1].strip('\n'), '\t')
        bibip.add_model(model)
    
    print("\nСырые файлы обработаны")


if __name__ == '__main__':
    # path = 'src'  # папка для сохранения файлов

    # Читаем сырые файлы
    init_raw_files()