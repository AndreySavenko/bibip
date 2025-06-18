from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel
import json


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
    status: str | None = None  # добавил поле для пометки удаленных продаж

    def index(self) -> str:
        return self.car_vin

    def return_params_as_list(self) -> list[str]:
        """ Мое. Возвращает все параметры списком """
        lst: list[str] = list()
        lst.append(str(self.sales_number))
        lst.append(self.car_vin)
        lst.append(datetime.strftime(self.sales_date, '%Y-%m-%d'))
        lst.append(str(self.cost))
        lst.append(str(self.status))
        return lst

    def return_params_as_json(self):
        dct = {
            'sales_number': self.sales_number,
            'car_vin': self.car_vin,
            'sales_date': datetime.strftime(self.sales_date, '%Y-%m-%d'),
            'cost': str(self.cost),
            'status': str(self.status)
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
    # price: Decimal | None = None  # не было в шаблоне. Добавил


""" ------------------- Мое ----------------------------------------------- """


def init_car(text: str, delimiter: str) -> Car:
    """ Функция возвращает объект models.Car.
    Функция принимает строку с параметрами, разделенными delimiter,
    распаковываем строку в список, приводим параметры к нужным типам.
    """
    param = str.split(text, delimiter)
    dat = datetime.strptime(param[3], '%Y-%m-%d')
    # print(dat, type(dat))
    if param[4] == 'available':
        status = CarStatus.available
    elif param[4] == 'reserve':
        status = CarStatus.reserve
    elif param[4] == 'delivery':
        status = CarStatus.delivery
    elif param[4] == 'sold':
        status = CarStatus.sold
    else:
        raise ValueError
    price = Decimal(str.replace(param[2], ',', '.'))
    car = Car(vin=param[0], model=int(param[1]), price=price, date_start=dat,
              status=status)

    return car


def init_model(text: str, delimiter: str) -> Model:
    """ Функция возвращает объект models.Model.
    Функция принимает строку с параметрами, разделенными delimiter,
    распаковываем строку в список, приводим параметры к нужным типам.
    """
    param = str.split(text, delimiter)
    model = Model(id=int(param[0]), name=param[1], brand=param[2])
    return model


def init_sale(text: str, delimiter: str) -> Sale:
    """ Функция возвращает объект models.Sale.
    Функция принимает строку с параметрами, разделенными delimiter,
    распаковываем строку в список, приводим параметры к нужным типам.
    """
    param = str.split(text, delimiter)
    dat = datetime.strptime(param[2], '%Y-%m-%d')
    cost = Decimal(str.replace(param[3], ',', '.'))
    sale = Sale(sales_number=param[0], car_vin=param[1], sales_date=dat,
                cost=cost)
    return sale
