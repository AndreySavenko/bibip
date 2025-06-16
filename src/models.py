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
        lst.append(self.model)
        lst.append(self.price)
        # Приведем дату в текст с нужным форматированием
        lst.append(datetime.strftime(self.date_start, '%Y-%m-%d'))
        lst.append(self.status)
        return lst

    def return_params_as_json(self) -> json:
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
        lst.append(self.id)
        lst.append(self.name)
        lst.append(self.brand)
        return lst

    def return_params_as_json(self) -> json:
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
