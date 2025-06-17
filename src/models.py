from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel

from pathlib import Path
import json

ROW_LENTS = 150  # длина строки для базы (без учета символа \n)


class CarStatus(StrEnum):
    available = "available"
    reserve = "reserve"
    sold = "sold"
    delivery = "delivery"


class Car(BaseModel):
    vin: str
    model: int
    price: Decimal
    date_start: datetime
    status: CarStatus

    def index(self) -> str:
        return self.vin

    def return_params_as_list(self) -> list[str]:
        """ Мое. Возвращает все параметры списком """
        lst: list[str] = list()
        lst.append(self.vin)
        lst.append(str(self.model))
        lst.append(str(self.price))
        # Приведем дату в текст с нужным форматированием
        lst.append(datetime.strftime(self.date_start, '%Y-%m-%d'))
        lst.append(self.status)
        return lst

    def return_params_as_json(self):
        dct = {
            'vin': str(self.vin),
            'model': self.model,
            'price': str(self.price),
            'date_start': datetime.strftime(self.date_start, '%Y-%m-%d'),
            'status': str(self.status)
        }
        return json.dumps(dct)


class Model(BaseModel):
    id: int
    name: str
    brand: str

    def index(self) -> str:
        return str(self.id)

    def return_params_as_list(self) -> list[str]:
        """ Мое. Возвращает все параметры списком """
        lst: list[str] = list()
        lst.append(str(self.id))
        lst.append(self.name)
        lst.append(self.brand)
        return lst

    def return_params_as_json(self):
        dct = {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
        }
        return json.dumps(dct)


class Sale(BaseModel):
    sales_number: str
    car_vin: str
    sales_date: datetime
    cost: Decimal

    def index(self) -> str:
        return self.car_vin

    def return_params_as_list(self) -> list[str]:
        """ Мое. Возвращает все параметры списком """
        lst: list[str] = list()
        lst.append(str(self.sales_number))
        lst.append(self.car_vin)
        lst.append(datetime.strftime(self.sales_date, '%Y-%m-%d'))
        lst.append(str(self.cost))
        return lst

    def return_params_as_json(self):
        dct = {
            'sales_number': self.sales_number,
            'car_vin': self.car_vin,
            'sales_date': datetime.strftime(self.sales_date, '%Y-%m-%d'),
            'cost': str(self.cost)
        }
        return json.dumps(dct)

class CarFullInfo(BaseModel):
    vin: str
    car_model_name: str
    car_model_brand: str
    price: Decimal
    date_start: datetime
    status: CarStatus
    sales_date: datetime | None
    sales_cost: Decimal | None


class ModelSaleStats(BaseModel):
    car_model_name: str
    brand: str
    sales_number: int


""" ------------------- Мое ----------------------------------------------- """


def write_row_in_file(path: str, nam: str, text: str, num_row: int,
                      row_len: int = ROW_LENTS, RW: bool = False):
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
    return None


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
