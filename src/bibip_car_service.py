from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
import os


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        # Translate into string
        model_string = f"{model.id};{model.brand};{model.name}"
                
        # Add \n and spaces till 501 char
        model_string = model_string.ljust(500)
        model_string = model_string + '\n'
        
        # Calculate lines number
        with open(file_path, "r", encoding="utf-8") as f:
            line_number = sum(1 for _ in f)
        
        with open(file_path, "r+", encoding="utf-8") as f: # r+ нужен для того, чтобы была возможность писать в тот же файл, что читаем.
            f.seek(line_number * (501)) # длина строки 501, т.к. добавили символ перехода строки — он тоже считается.
            f.write(model_string)
        
        return model
    
     # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        raise NotImplementedError

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        raise NotImplementedError

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
