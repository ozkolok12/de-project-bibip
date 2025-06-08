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
        
        # Calculate lines number in models.txt
        file_path_models = os.path.join(self.root_directory_path, "models.txt")

        if not os.path.exists(file_path_models):
            with open(file_path_models, "w", encoding="utf-8") as f:
                pass 
        
        with open(file_path_models, "r", encoding="utf-8") as f:
            line_number = sum(1 for _ in f)
        
        # Writing to file models.txt
        with open(file_path_models, "r+", encoding="utf-8") as f:
            f.seek(line_number * (501))
            f.write(model_string)

        # Writing to models_index.txt
        file_path_index = os.path.join(self.root_directory_path, "models_index.txt")

        if not os.path.exists(file_path_index):
            with open(file_path_index, "w", encoding="utf-8") as f:
                pass 

        index_list = []
        with open(file_path_index, "r+", encoding="utf-8") as f:
            for line in f:
                parts = tuple(map(int, line.strip().split(";")))
                index_list.append(parts)
             
        index_line_number = len(index_list)
        index_list.append((index_line_number, line_number))

        index_list.sort(key=lambda x: int(x[0]))

        with open(file_path_index, "w", encoding="utf-8") as f:
            for row in index_list:
                f.write(";".join(map(str, row)) + "\n")
       
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

"""
with open("C:\\Users\\Hoz\\Documents\\Python projects\\de-project-bibip\\src\\test_index.txt", "r+") as f:
    my_list = f.readlines()
    index_list = []
    
    for line in my_list:
        parts = list(map(int, line.strip().split(";")))
        index_list.append(parts)

index_list """
