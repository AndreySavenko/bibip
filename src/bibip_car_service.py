from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from models import write_row_in_file, write_file, read_row_in_file, init_car, init_model, init_sale
from pathlib import Path
from datetime import datetime as dt
from decimal import Decimal


DELIMITER: str = ';'
CARS_FNAME: str = 'cars.txt'
CARS_INDEX_FNAME: str = 'cars_index.txt'
MODELS_FNAME: str = 'models.txt'
MODELS_INDEX_FNAME: str = 'models_index.txt'
SALES_FNAME: str = 'sales.txt'
SALES_INDEX_FNAME: str = 'sales_index.txt'
DELETED_STATUS: str = 'is_deleted'

class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        path = self.root_directory_path.rstrip('/')
        # читаем файл Индекс, определяем число записей
        index_lst = read_index_file(path, MODELS_INDEX_FNAME)
        cnt = len(index_lst)  # число записей. Будет 0, если файла нет.
        # добавляем в индекс новые строки
        # index_lst.append(model.brand + ' ' + model.name + DELIMITER + str(cnt + 1))
        index_lst.append(str(cnt + 1) + DELIMITER + str(cnt + 1))
        # пишем в файл базы, как строку с разделителями
        lst = model.return_params_as_list()  # возвращаем параметры списком
        write_row_in_file(path, MODELS_FNAME, str.join(DELIMITER, map(str, lst)), cnt + 1)

        # пишем в файл базы, как строку json (или словарь) - отказался от этого варианта
        # json_string = model.return_params_as_json()
        # write_row_in_file(path, 'models_json.txt', json_string, cnt+1)

        # сортируем обновленный Индекс
        list.sort(index_lst)  # не имеет смысл сортировать реальный индекс для моделей
        # перезаписываем файл Индекс
        text = str.join('\n', index_lst)  # делаем многострочный текст из списка
        write_file(path, MODELS_INDEX_FNAME, text, fix_len=False)
        # raise NotImplementedError
        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        path = self.root_directory_path.rstrip('/')
        # читаем файл Индекс, определяем число записей
        index_lst = read_index_file(path, CARS_INDEX_FNAME)
        cnt = len(index_lst)  # число записей. Будет 0, если файла нет.        
        # добавляем в индекс новые строки
        index_lst.append(car.vin + DELIMITER + str(cnt + 1))
        # пишем в файл базы, как строку с разделителями
        lst = car.return_params_as_list()
        write_row_in_file(path, CARS_FNAME, str.join(DELIMITER, map(str, lst)),
                          cnt+1)  # i+1 - чтобы нуме-я строк была с 1

        # пишем в файл базы, как строку json (или словарь)
        # json_string = car.return_params_as_json()
        # write_row_in_file(path, 'cars_json.txt', json_string, cnt+1)

        # сортируем обновленный Индекс
        list.sort(index_lst)
        # перезаписываем файл Индекс
        text = str.join('\n', index_lst)  # делаем многострочный текст из списка
        write_file(path, CARS_INDEX_FNAME, text, fix_len=False)
        # raise NotImplementedError
        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        path = self.root_directory_path.rstrip('/')
        # читаем файл Индекс, определяем число записей
        index_lst = read_index_file(path, SALES_INDEX_FNAME)
        cnt = len(index_lst)  # число записей. Будет 0, если файла нет.
        # добавляем в индекс новые строки
        index_lst.append(sale.sales_number + DELIMITER + str(cnt + 1))  # + DELIMITER + 'OK')
        # пишем в файл базы, как строку с разделителями
        lst = sale.return_params_as_list()
        write_row_in_file(path, SALES_FNAME, str.join(DELIMITER, map(str, lst)), cnt+1)

        # сортируем обновленный Индекс
        list.sort(index_lst)
        # перезаписываем файл Индекс
        text = str.join('\n', index_lst)  # делаем многострочный текст из списка
        write_file(path, SALES_INDEX_FNAME, text, fix_len=False)

        # Теперь обновляем данные по авто.
        # Поиск авто по Vin
        # читаем файл Индекс для авто, определяем число записей
        index_lst = read_index_file(path, CARS_INDEX_FNAME)
        cnt = len(index_lst)  # число записей. Будет 0, если файла нет.
        if cnt == 0:
            raise Exception("Нельзя продать машину, если вообще нет машин")
        for i in range(len(index_lst)):
            fnd = str(index_lst[i]).find(sale.car_vin)
            if str(index_lst[i]).find(sale.car_vin) >= 0: #is not None:
                # парсим подстроку, определяем номер записи в базе
                car_number = int(index_lst[i].split(DELIMITER)[1])
                break

        # Формируем объект car
        text = read_row_in_file(path, CARS_FNAME, car_number) # читаем строку из базы
        car = init_car(text, DELIMITER)
        car.status = CarStatus.sold  # Обновляем статус авто в модели
        lst = car.return_params_as_list()  # получаем параметры списком
        # пишем обновленную строку в базу (перезаписываем)
        write_row_in_file(path, CARS_FNAME, str.join(DELIMITER, map(str, lst)),
                          car_number, RW=True)  # i+1 - чтобы нуме-я строк была с 1
        return car  # возвращем объект car (так было в шаблоне, пока не понял зачем...)

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        path = self.root_directory_path.rstrip('/')
        # нужно перебрать базу машин.
        # т.к. зачитать целиком файл базы по условию задачи не можем, то
        # читаем сначала файл индексов, определяем число строк
        index_lst = read_index_file(path, CARS_INDEX_FNAME)
        cnt = len(index_lst)
        cars_lst = list()
        # далее построчно читаем основной файл базы, Отбирая нужные записи
        for i in range(cnt):
            text = read_row_in_file(path, CARS_FNAME, i+1)  # читаем строку из базы
            car = init_car(text, DELIMITER)  # получаем объект Car из строки
            if car.status == CarStatus.available:
                cars_lst.append(car)  # сохраняем в выборку, если нужный статус
        # raise NotImplementedError
        return cars_lst

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        path = self.root_directory_path.rstrip('/')        
        # читаем сначала файл индекс авто, определяем число строк
        index_cars = read_index_file(path, CARS_INDEX_FNAME)
        cnt_cars = len(index_cars)
        break_out_flag = False  # флаг выхода из верхнего цикла
        not_find = True
        # for num_car in range(cnt_cars):
        for car_index_item in index_cars:
            car_index, car_num = car_index_item.split(DELIMITER)
            if vin == car_index:
                text = read_row_in_file(path, CARS_FNAME, int(car_num))
                car = init_car(text, DELIMITER)  # получаем объект Car
                # читаем модели
                index_models = read_index_file(path, MODELS_INDEX_FNAME)
                for model_index_item in index_models:  # range(cnt_models):
                    model_index, model_num = model_index_item.split(DELIMITER)
                    if car.model == int(model_index):
                        text = read_row_in_file(path, MODELS_FNAME, int(model_num))
                        model = init_model(text, DELIMITER)  # получаем Model
                        break_out_flag = True  # для выхода из внешенего цикла
                        break
                if break_out_flag:
                    not_find = False
                    break  # exit из верхнего цикла, когда нашли Car и Model

        if not_find:
            return None
        #    raise Exception(f'Не нашли машину с VIN {vin}')
        # читаем продажи, если машина числится проданной
        # присвоим стартовые значения. Обновим, если есть продажа
        sales_date = None
        sales_cost = None
        if car.status == CarStatus.sold:
            index_sales = read_index_file(path, SALES_INDEX_FNAME)
            cnt_sales = len(index_sales)  # получили число продаж
            for sale_num in range(cnt_sales):  # построчно читаем продажи
                # тут нужно именно итерировать саму базу, а не искать индекс
                text = read_row_in_file(path, SALES_FNAME, int(sale_num)+1)
                sale = init_sale(text, DELIMITER)  # получаем объект Sale
                if car.vin == sale.car_vin:
                    if sale.status != DELETED_STATUS:
                        sales_date = sale.sales_date
                        sales_cost = sale.cost
                    break  # в любом случае выходим из цикла,
#                            даже если статус продажи не подтвердился
        # теперь есть все параметры, чтобы получить объект CarFullInfo
        return CarFullInfo(vin=car.vin, car_model_name=model.name,
                           car_model_brand=model.brand, price=car.price,
                           date_start=car.date_start, status=car.status,
                           sales_date=sales_date, sales_cost=sales_cost)
        # raise NotImplementedError


    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        path = self.root_directory_path.rstrip('/')
        # читаем сначала файл индекс авто, определяем число строк
        index_cars = read_index_file(path, CARS_INDEX_FNAME)
        cnt_cars = len(index_cars)
        for num_car in range(cnt_cars):
            index = index_cars[num_car].split(DELIMITER)
            if vin == index[0]:
                num_row = int(index[1])
                break  # сделали дело, выходим из цикла
        text = read_row_in_file(path, CARS_FNAME, num_row)  # читаем базу
        car = init_car(text, DELIMITER)  # получаем объект Car из строки
        car.vin = new_vin
        # обновляем строку в базе
        lst = car.return_params_as_list()
        write_row_in_file(path, CARS_FNAME, str.join(DELIMITER, map(str, lst)), num_row, RW = True)
        # обновляем вин в индексе
        index_cars[num_car] = car.vin + DELIMITER + str(num_row)
        list.sort(index_cars)  # сортируем индекс в памяти
        # перезаписываем файл Индекс полностью
        text = str.join('\n', index_cars)  # делаем многострочный текст из списка
        write_file(path, CARS_INDEX_FNAME, text, fix_len=False)
        # raise NotImplementedError
        return car

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        path = self.root_directory_path.rstrip('/')  
        # читаем сначала файл индекс, определяем число строк
        index_sales = read_index_file(path, SALES_INDEX_FNAME)
        cnt_sales = len(index_sales)
        for num in range(cnt_sales):
            sale_index, sale_row = index_sales[num].split(DELIMITER)
            if sales_number == sale_index:
                # index_sales[num] = sale_index + DELIMITER + sale_row  # + DELIMITER + DELETED_STATUS
                break
        # list.sort(index_sales) # сортировать индекс не нужно, ключи не обновились
        # т.к. именно в индексе я не выдерживал равное число символов в строке, 
        # то перезапишу весь файл, а не конкретную строку
        #text = str.join('\n', index_sales)  # делаем многострочный текст из списка
        # write_file(path, SALES_INDEX_FNAME, text, fix_len=False)
        
        # инициализируем продажу, чтобы знать vin авто
        text = read_row_in_file(path, SALES_FNAME, int(sale_row))  # читаем базу
        sale = init_sale(text, DELIMITER)
        sale.status = DELETED_STATUS
        lst = sale.return_params_as_list()
        write_row_in_file(path, SALES_FNAME, str.join(DELIMITER, map(str, lst)), int(sale_row), RW = True)

        # теперь найдем авто, обновим статус
        index_cars = read_index_file(path, CARS_INDEX_FNAME)
        # cnt_cars = len(index_cars)
        for car_index_item in index_cars:
            car_index, car_num = car_index_item.split(DELIMITER)
            if sale.car_vin == car_index:
                break  # сделали дело, выходим из цикла

        text = read_row_in_file(path, CARS_FNAME, int(car_num))  # читаем базу авто
        car = init_car(text, DELIMITER)  # получаем объект Car из строки
        if car.status != CarStatus.sold:
            raise Exception("Эта машина должна была быть помечена, как удаленная")
        car.status = CarStatus.available  # ставим правильный статус
        # обновляем строку в базе
        lst = car.return_params_as_list()  # получаем параметры объекта списком
        # перезаписываем строку в базе.
        write_row_in_file(path, CARS_FNAME, str.join(DELIMITER, map(str, lst)), int(car_num), RW = True)
        return car


    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        # пытаюсь реализовать шаги из подсказки
        path = self.root_directory_path.rstrip('/')  
        # читаю все действительные (неудаленные) продажи
        id_cnt_dct: dict[int, int] = dict()  # dict для пары model_id:count
        id_cost_dct: dict[int, Decimal] = dict()  # dict для пары mode_id:cost
        # второй словарь, чтобы цену запомнить
        # храню в разных словарях, чтобы потом сортировать словарь по значению

        # читаю индексы продаж, определяю число продаж
        index_sales = read_index_file(path, SALES_INDEX_FNAME)
        cnt_sales = len(index_sales)
        for sale_index in range(cnt_sales):
            id, sale_num = index_sales[sale_index].split(DELIMITER)
            
            # тут надо переделать!!!!!! статус теперь не тут!
            
            if status != DELETED_STATUS:
                # читаю продажи
                text = read_row_in_file(path, SALES_FNAME, int(sale_num))
                sale = init_sale(text, DELIMITER)                     
                # vin = sale.car_vin  # фиксирую vin
                # ищу по vin номер авто
                index_cars = read_index_file(path, CARS_INDEX_FNAME)
                cnt_cars = len(index_cars)
                for car_index in range(cnt_cars):
                    vin, car_num = index_sales[car_index].split(DELIMITER)
                    if sale.car_vin == vin:
                        break
                text = read_row_in_file(path, CARS_FNAME, int(car_num))
                car = init_car(text, DELIMITER)  # получаем объект Car
                #  model_id = car.model  # запомнили id модели
                #  price = car.price  # запомнили цену авто
                #  пишем в словари
                if car.model in id_cnt_dct:  # другой словарь можно не чекать
                    id_cnt_dct[car.model] = int(id_cnt_dct[car.model] + 1)
                    if car.price > id_cost_dct[car.model]:
                        #  у авто одинаковых моделей может быть разная цена.
                        #  запомним самый дорогой
                        # (хотя может быть, лучше было самый дешевый..)
                        id_cost_dct[car.model] = car.price
                else:  # добавляем новый id в словарь
                    id_cnt_dct[car.model] = 1
                    id_cost_dct[car.model] = car.price
        
        #  сортируем словарь (подсказка).
        #  Только сейчас узнал, что такое возможно в python...
        #  мы такое не проходили ) нас таким странным вещам не учили) ну ладно.
        top_three = sorted(id_cnt_dct.items(), key=lambda item: item[1],
                           reverse=True)[:3]
        # Эту строку выдал DeepSeek. Без него я чуть не сдался.
        # Восхищен этим однострочником. Как красив и многогранен Python...

        # Итак, окончание. Итерируем полученный список, превращаем в объекты
        result: list[ModelSaleStats] = list()
        index_models = read_index_file(path, MODELS_INDEX_FNAME)
        cnt_models = len(index_models)
        for item in top_three:
            for num_model in range(cnt_models):
                model_id, model_num = index_models[num_model].split(DELIMITER)
                if item[0] == int(model_id):
                    text = read_row_in_file(path, MODELS_FNAME, int(model_num))
                    model = init_model(text, DELIMITER)  # генерим объект Model
                    price = Decimal(id_cost_dct[model.id])
                    sale_stat_obj = ModelSaleStats(car_model_name=model.name,
                                                   brand=model.brand,
                                                   sales_number=int(item[1]),
                                                   price=price)
                    result.append(sale_stat_obj)
                    break
        # raise NotImplementedError
        return result

def read_index_file(path: str, nam: str) -> list[str]:
    fullpath = f'{path}/{nam}'
    p = Path(fullpath)
    isfile = p.is_file()
    if isfile:
        with open(fullpath, 'r') as f:
            index_lst = f.read().rstrip('\n').split('\n')
    else:
        index_lst = list()
    return index_lst



