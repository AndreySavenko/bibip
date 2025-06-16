
# import json
# import os
from pathlib import Path
import models as bibip
from datetime import datetime as dt
from decimal import Decimal 
import sys

ROW_LENTS = 150  # длина строки для базы (без учета символа \n)


def read_file(path: str, nam: str):  # -> list:
    """ Читаем файл целиком. Возвращает список строк"""
    # p = Path(path)
    # print('Начинаем read_file:\n')
    with open(f'{path.rstrip('/')}/{nam}',
              'r', encoding='utf-8') as f:
        lines = f.readlines()
        # print(lines)  # , type(lines))
    return lines


def read_row_in_file(path: str, nam: str, num_row: int,
                     row_len: int = ROW_LENTS) -> str:
    """ Читаем конкретную строку в файле
     Должна быть реализована константная длина строк"""
    # Нумерация строк файла начинается с 1 (как id в БД)
    with open(f'{path.rstrip('/')}/{nam}', 'r') as f:
    # with open(f'{path.rstrip('/')}/{nam}', 'r', encoding='utf-8') as f:
        #      'r', encoding='utf-8') as f:
        offset = (num_row - 1) * (row_len + 1)
        f.seek(offset)  # +1 - учет символа \n
        text = f.read(row_len)
        text = text.strip(' \n')  # получаем строку без \n и ' '
        # сначала хотел применить rstrip, но в начале строки откуда-то
        # появляется \n, хотя я вроде правильно читаю (с начала строк)
    return text


def write_row_in_file(path: str, nam: str, text: str, num_row: int,
                      row_len: int = ROW_LENTS, RW: bool = False) -> str:
    """ Пишем конкретную строку в файле
      Должна быть реализована константная длина строк"""
    # Нумерация строк файла начинается с 1 (как id в БД)
    p = Path(path)
    p.mkdir(exist_ok=True)  # создадим папку, если нету
    fullpath = f'{path.rstrip('/')}/{nam}'
    p = Path(fullpath)
    isfile = p.is_file()
    if isfile:
        mode = 'r+'
        offset = (num_row - 1) * (row_len + 1)  # +1 - учет символа \n
    else:
        mode = 'w'

    if len(text) <= row_len:
        text = text.ljust(row_len)
    else:
        raise Exception(f'Длина строки больше ограничения\n{text}')
    # print(len(text), text)
    if not RW:  # если не перезаписываем строку, то добавим каретку переноса
        text = text + '\n'

    # with open(fullpath, mode, encoding='utf-8') as f:  # mode = f(isfile)
    with open(fullpath, mode) as f:  # mode = f(isfile)
        if isfile:
            f.seek(offset)
        f.write(text)


def write_file(path: str, nam: str, text: str, mode: str = 'w+',
               fix_len: bool = True, row_len: int = ROW_LENTS):
    # print('Начинаем write_file:\n')
    p = Path(path)
    p.mkdir(exist_ok=True)  # создадим папку, если нету
    if fix_len:
        if len(text) <= row_len:
            text = text.ljust(row_len)
        else:
            raise Exception(f'Длина строки больше ограничения\n{text}')
    with open(f'{path.rstrip('/')}/{nam}', mode, encoding='utf-8') as f:
    # with open(f'{path.rstrip('/')}/{nam}', mode) as f:
        # print(lines)  # , type(lines))
        f.write(text + '\n')
        # return lines


def init_car(text: str, delimiter: str) -> bibip.Car:
    """ Функция возвращает объект bibip.Car.
    Функция принимает строку с параметрами, разделенными delimiter,
    распаковываем строку в список, приводим параметры к нужным типам.
    """
    param = str.split(text, delimiter)
    dat = dt.strptime(param[3], '%Y-%m-%d')
    # print(dat, type(dat))
    if param[4] == 'available':
        status = bibip.CarStatus.available
    elif param[4] == 'reserve':
        status = bibip.CarStatus.reserve
    elif param[4] == 'delivery':
        status = bibip.CarStatus.delivery
    elif param[4] == 'sold':
        status = bibip.CarStatus.sold
    else:
        raise ValueError
    price = Decimal(str.replace(param[2], ',', '.'))
    car = bibip.Car(vin=param[0], model=int(param[1]), price=price, date_start=dat, status=status)

    return car


def init_model(text: str, delimiter: str) -> bibip.Model:
    """ Функция возвращает объект bibip.Model.
    Функция принимает строку с параметрами, разделенными delimiter,
    распаковываем строку в список, приводим параметры к нужным типам.
    """
    param = str.split(text, delimiter)
    model = bibip.Model(id=int(param[0]), name=param[1], brand=param[2])
    return model


def init_raw_files():
    path = 'src'
    nam = 'raw_cars.txt'
    f = read_file(path, nam)

    # print(f)

    # Это просто тестирование
    """   
    path2 = 'src2'  # папка для сохранения файлов
    nam2 = 'raw_cars2.txt'
    text = str.join('', lines)
    write_file(path2, nam2, text)
    lines2 = read_file(path2, nam2)
    if lines == lines2:
        print('The same')
    else:
        print('Different')
    """
    # пример инициализации авто из сырого файла
    ln = len(f)
    cars: list[bibip.Car] = list()  # создаем список типа bibip.Car

    for i in range(ln-1):
        # if i == 11:
        #    i = i
        car = init_car(f[i+1].strip('\n'), '\t')
        cars.append(car)  # добавляем в список очередной элемент
#        lst: list[str] = list() # создаем список
        lst = car.return_params_as_list()
        write_file(path, 'cars_list2.txt', str.join('; ', map(str, lst)), 'a', True, ROW_LENTS)
        write_row_in_file(path, 'cars_list.txt', str.join('; ', map(str, lst)),
                          i+1, ROW_LENTS)  # i+1 - чтобы нуме-я строк была с 1
#        print(str.join('; ', map(str, lst)))
        json_string = car.return_params_as_json()
#       print(json_string)  # , type(json_string))
        write_file(path, 'cars_json.txt', json_string, 'a')

    # Читаем весь сырой файл с машинами
    nam = 'raw_models.txt'
    fm = read_file(path, nam)
    ln = len(fm)
    models: list[bibip.Model] = list()  # создаем список типа bibip.Model

    for i in range(ln-1):
        # пример инициализации модели из сырого файла
        model = init_model(fm[i+1].strip('\n'), '\t')
        models.append(model)
        lst2 = model.return_params_as_list()
        # print(str.join('; ', map(str, lst2)))
        write_file(path, 'models_list2.txt', str.join('; ', map(str, lst2)), 'a', True, ROW_LENTS)
        write_row_in_file(path, 'models_list.txt', str.join('; ', map(str, lst2)), i+1, ROW_LENTS)
        json_string = model.return_params_as_json()
        # text: str = str(json_string)
        # print(json_string)
        # print(text, type(text))
        write_file(path, 'models_json.txt', json_string, 'a')
    
    print("\nСырые файлы обработаны")


if __name__ == '__main__':
    print(sys.path)
    # sys.path.append(r"D:\Dev\de-project-bibip\src")
    # sys.path.append('D:\Dev\bibip\src')    
    path = 'src'  # папка для сохранения файлов

    # Читаем сырые файлы
    init_raw_files()

    """
    f = read_file(path, 'models_list.txt')
    print(f'Число строк models_list: {len(f)}')
    print(f'Длина строки models_list: {len(f[1])}')


    f = read_file(path, 'models_json.txt')
    print(f'Число строк models_json: {len(f)}')
    print(f'Длина строки models_json: {len(f[1])}')

    f = read_file(path, 'cars_list.txt')
    print(f'Число строк cars_list: {len(f)}')
    print(f'Длина строки cars_list: {len(f[1])}')


    f = read_file(path, 'cars_json.txt')
    print(f'Число строк cars_json: {len(f)}')
    print(f'Длина строки cars_json: {len(f[1])}')
    
    
    f = read_file(path, 'cars_list.txt')
    print('\n')
    print(f)
    """
    
    text = read_row_in_file(path, 'cars_list.txt', 3, ROW_LENTS)
    print(text)

    text = 'НОВАЯ СТРОКА__________ух'
    # text = text.ljust(ROW_LENTS)
    write_row_in_file(path, 'cars_list.txt', text, 3, ROW_LENTS, True)

    text = read_row_in_file(path, 'cars_list.txt', 3, ROW_LENTS)
    print(text)

    text = read_row_in_file(path, 'cars_list.txt', 4, ROW_LENTS)
    print(text)

    text = read_row_in_file(path, 'cars_list.txt', 5, ROW_LENTS)
    print(text)


    text = read_row_in_file(path, 'models_list.txt', 3, ROW_LENTS)
    print(text)

    text = 'НОВАЯ СТРОКА в моделях ееее'
    # text = text.ljust(ROW_LENTS)
    write_row_in_file(path, 'models_list.txt', text, 3, ROW_LENTS, True)

    text = read_row_in_file(path, 'models_list.txt', 3, ROW_LENTS)
    print(text)

    text = read_row_in_file(path, 'models_list.txt', 4, ROW_LENTS)
    print(text)

    text = read_row_in_file(path, 'models_list.txt', 5, ROW_LENTS)
    print(text)