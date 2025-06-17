from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale, write_row_in_file, write_file
from pathlib import Path
from datetime import datetime as dt
from decimal import Decimal

DELIMITER: str = ';'

class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        path = self.root_directory_path.rstrip('/')
        # читаем файл Индекс, определяем число авто
        f_index_nam = 'models_index.txt'
        fullpath = f'{path}/{f_index_nam}'
        p = Path(fullpath)
        isfile = p.is_file()
        if isfile:
            with open(fullpath, 'r') as f:
                index_lst = f.read().rstrip('\n').split('\n')
        else:
            index_lst = list()

        # определяем текущее число машин
        cnt = len(index_lst)  # при первом проходе (отсутствии файла)= 0
        # добавляем в индекс новые строки
        index_lst.append(model.brand + ' ' + model.name + DELIMITER + str(cnt + 1))
        # пишем в файл базы, как строку с разделителями
        lst = model.return_params_as_list()
        write_row_in_file(path, 'models.txt', str.join('; ', map(str, lst)), cnt+1)

        # пишем в файл базы, как строку json (или словарь)
        # json_string = model.return_params_as_json()
        # write_row_in_file(path, 'models_json.txt', json_string, cnt+1)

        # сортируем обновленный Индекс
        list.sort(index_lst)
        # перезаписываем файл Индекс
        text = str.join('\n', index_lst)  # делаем многострочный текст из списка
        write_file(path, 'models_index.txt', text, fix_len=False)
        # raise NotImplementedError
        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        path = self.root_directory_path.rstrip('/')
        # читаем файл Индекс, определяем число авто
        f_index_nam = 'cars_index.txt'
        fullpath = f'{path}/{f_index_nam}'
        p = Path(fullpath)
        isfile = p.is_file()
        if isfile:
            with open(fullpath, 'r') as f:
                # index_lst = f.readlines()
                index_lst = f.read().rstrip('\n').split('\n')
        else:
            index_lst = list()

        # определяем текущее число машин
        cnt = len(index_lst)  # при первом проходе (отсутствии файла)= 0
        # добавляем в индекс новые строки
        index_lst.append(car.vin + DELIMITER + str(cnt + 1))
        # пишем в файл базы, как строку с разделителями
        lst = car.return_params_as_list()
        write_row_in_file(path, 'cars_list.txt', str.join('; ', map(str, lst)),
                          cnt+1)  # i+1 - чтобы нуме-я строк была с 1

        # пишем в файл базы, как строку json (или словарь)
        # json_string = car.return_params_as_json()
        # write_row_in_file(path, 'cars_json.txt', json_string, cnt+1)
    
        # сортируем обновленный Индекс
        list.sort(index_lst)
        # перезаписываем файл Индекс
        text = str.join('\n', index_lst)  # делаем многострочный текст из списка
        write_file(path, 'cars_index.txt', text, fix_len=False)
        # raise NotImplementedError
        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        path = self.root_directory_path.rstrip('/')
        # читаем файл Индекс, определяем число авто
        f_index_nam = 'sales_index.txt'
        fullpath = f'{path}/{f_index_nam}'
        p = Path(fullpath)
        isfile = p.is_file()
        if isfile:
            with open(fullpath, 'r') as f:
                index_lst = f.read().rstrip('\n').split('\n')
        else:
            index_lst = list()

        # определяем текущее число машин
        cnt = len(index_lst)  # при первом проходе (отсутствии файла)= 0
        # добавляем в индекс новые строки
        index_lst.append(sale.sales_number + DELIMITER + str(cnt + 1))
        # пишем в файл базы, как строку с разделителями
        lst = sale.return_params_as_list()
        write_row_in_file(path, 'sales.txt', str.join('; ', map(str, lst)), cnt+1)

        # пишем в файл базы, как строку json (или словарь)
        # json_string = model.return_params_as_json()
        # write_row_in_file(path, 'sales_json.txt', json_string, cnt+1)

        # сортируем обновленный Индекс
        list.sort(index_lst)
        # перезаписываем файл Индекс
        text = str.join('\n', index_lst)  # делаем многострочный текст из списка
        write_file(path, 'sales_index.txt', text, fix_len=False)
        
        # Теперь обновляем данные по авто.
        # Поиск авто по Vin
        f_index_nam = 'cars_index.txt'
        fullpath = f'{path}/{f_index_nam}'
        p = Path(fullpath)
        isfile = p.is_file()
        if isfile:
            with open(fullpath, 'r') as f:
                index_lst = f.read().rstrip('\n').split('\n')
        else:
            raise Exception("Нельзя продать машину, если вообще нет машин")        
        for i in range(len(index_lst)):
            if str(index_lst[i]).find(sale.car_vin) is not None:
                # парсим подстроку, определяем номер записи в базе
                car_number = index_lst[i].split(DELIMITER)[1]
        
        # Формируем объект car

        # Теперь обновляем файл базы по авто.

        # raise NotImplementedError
        return car     
        #raise NotImplementedError

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        raise NotImplementedError

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        raise NotImplementedError

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        raise NotImplementedError

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        raise NotImplementedError

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        raise NotImplementedError
