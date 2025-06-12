from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
import os

from decimal import Decimal
from datetime import datetime

class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение моделей
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

        # Creating file IF NOT EXIST
        if not os.path.exists(file_path_index):
            with open(file_path_index, "w", encoding="utf-8"):
                pass

        # Reading index
        index_list = []
        with open(file_path_index, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) == 2:
                    index_list.append((int(parts[0]), int(parts[1])))

        # Adding new entry (ID , model.id)
        new_id = len(index_list)
        index_list.append((new_id, model.id))

        # Writing to index
        with open(file_path_index, "w", encoding="utf-8") as f:
            for row in index_list:
                f.write(f"{row[0]};{row[1]}\n")

        return model
    
    # Задание 1. Сохранение автомобилей
    def add_car(self, car: Car) -> Car:
        # Формируем строку
        car_string = (
            f"{car.vin};"
            f"{car.model};"
            f"{car.price};"
            f"{car.date_start:%Y-%m-%d};"
            f"{car.status.value}"
        ).ljust(500) + "\n"

        # Path to cars.txt
        file_path_cars = os.path.join(self.root_directory_path, "cars.txt")

        if not os.path.exists(file_path_cars):
            with open(file_path_cars, "w", encoding="utf-8"):
                pass

        with open(file_path_cars, "r", encoding="utf-8") as f:
            line_number = sum(1 for _ in f)

        # Writing into cars.txt
        with open(file_path_cars, "r+", encoding="utf-8") as f:
            f.seek(line_number * 501)
            f.write(car_string)

        # Path to  cars_index.txt
        file_path_index = os.path.join(self.root_directory_path, "cars_index.txt")
        if not os.path.exists(file_path_index):
            with open(file_path_index, "w", encoding="utf-8"):
                pass

        index_list = []
        with open(file_path_index, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) == 2:
                    index_list.append((int(parts[0]), parts[1]))

        new_id = len(index_list)
        index_list.append((new_id, car.vin))

        # Re-writing index file
        with open(file_path_index, "w", encoding="utf-8") as f:
            for idx, vin in index_list:
                f.write(f"{idx};{vin}\n")

        return car
    

    def sell_car(self, sale: Sale) -> Sale:
        # 1) Adding to sales.txt
        sales_path = os.path.join(self.root_directory_path, "sales.txt")
        if not os.path.exists(sales_path):
            open(sales_path, "w", encoding="utf-8").close()
        sale_line = f"{sale.sales_number};{sale.car_vin};{sale.cost};{sale.sales_date:%Y-%m-%d}\n"
        with open(sales_path, "a", encoding="utf-8") as f:
            f.write(sale_line)

        # 2) Change fro sold in cars.txt
        idx_path = os.path.join(self.root_directory_path, "cars_index.txt")
        car_line = None
        with open(idx_path, "r", encoding="utf-8") as f:
            for rec in f:
                idx_str, vin = rec.strip().split(";")
                if vin == sale.car_vin:
                    car_line = int(idx_str)
                    break
        if car_line is None:
            raise ValueError(f"VIN {sale.car_vin} not in cars_index")

        cars_path = os.path.join(self.root_directory_path, "cars.txt")
        with open(cars_path, "r+", encoding="utf-8") as f:
            f.seek(car_line * 501)
            raw_block = f.read(501)
            raw = raw_block.rstrip("\n")
            parts = [p.strip() for p in raw.split(";")]
            if len(parts) < 5:
                raise RuntimeError("Unexpected cars.txt format")
            
            # updateing status
            parts[4] = CarStatus.sold.value
            # заново формируем ровно 500 символов + "\n"
            new_line = ";".join(parts).ljust(500) + "\n"
            
            # re-writing
            f.seek(car_line * 501)
            f.write(new_line)

        return sale

        

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
    
        path = os.path.join(self.root_directory_path, "cars.txt")
        cars = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                parts = [p.strip() for p in line.strip().split(";")]
                if len(parts) != 5:
                    continue
                vin, model, price, date_str, st = parts
                if CarStatus(st) != status:
                    continue
                cars.append(Car(
                    vin=vin,
                    model=int(model),
                    price=Decimal(price),
                    date_start=datetime.strptime(date_str, "%Y-%m-%d"),
                    status=CarStatus(st)
                ))
        return cars


    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        # Looking for a string
        cars_index_path = os.path.join(self.root_directory_path, "cars_index.txt")
        car_line = None
        with open(cars_index_path, "r", encoding="utf-8") as f:
            for line in f:
                idx, vin_i = line.strip().split(";")
                if vin_i == vin:
                    car_line = int(idx)
                    break
        if car_line is None:
            return None

        # Reading from cars.txt
        cars_path = os.path.join(self.root_directory_path, "cars.txt")
        with open(cars_path, "r", encoding="utf-8") as f:
            f.seek(car_line * 501)
            raw = f.readline().rstrip("\n")
        car_fields = [field.strip() for field in raw.split(";")]
        car_vin, model_id_str, price_str, date_str, status_str = car_fields[:5]

        model_id   = int(model_id_str)
        price      = Decimal(price_str)
        date_start = datetime.strptime(date_str, "%Y-%m-%d")
        status     = CarStatus(status_str)

        # Finding model by model_id
        models_index_path = os.path.join(self.root_directory_path, "models_index.txt")
        model_line = None
        with open(models_index_path, "r", encoding="utf-8") as f:
            for line in f:
                idx_str, model_id_str_i = line.strip().split(";")
                if int(model_id_str_i) == model_id:
                    model_line = int(idx_str)
                    break
        if model_line is None:
            raise ValueError("Model not found")

        models_path = os.path.join(self.root_directory_path, "models.txt")
        with open(models_path, "r", encoding="utf-8") as f:
            f.seek(model_line * 501)
            raw = f.readline().rstrip("\n")
        model_fields = [field.strip() for field in raw.split(";")]
        _, brand, name = model_fields[:3]
        model_name = name
        model_brand = brand

        sales_date = None
        sales_cost = None
        if status == CarStatus.sold:
            sales_path = os.path.join(self.root_directory_path, "sales.txt")
            with open(sales_path, "r", encoding="utf-8") as f:
                for line in f:
                    fields = [field.strip() for field in line.strip().split(";")]
                    if len(fields) != 4:
                        continue
                    _, vin_i, cost_str, date_str = fields
                    if vin_i == vin:
                        sales_cost = Decimal(cost_str)
                        sales_date = datetime.strptime(date_str, "%Y-%m-%d")
                        break

        return CarFullInfo(
            vin=car_vin,
            car_model_name=model_name,
            car_model_brand=model_brand,
            price=price,
            date_start=date_start,
            status=status,
            sales_date=sales_date,
            sales_cost=sales_cost
        )




    # Задание 5. Обновление VIN
    def update_vin(self, vin: str, new_vin: str) -> Car | None:
        idx_path = os.path.join(self.root_directory_path, "cars_index.txt")
        entries = []
        target = None
        
        # Looking for an index
        with open(idx_path, "r", encoding="utf-8") as f:
            for rec in f:
                idx, vin_i = rec.strip().split(";")
                i = int(idx)
                entries.append((i, vin_i))
                if vin_i == vin:
                    target = i
        if target is None:
            return None

        cars_path = os.path.join(self.root_directory_path, "cars.txt")
        
        # Updating VIn in cars.txt
        with open(cars_path, "r+", encoding="utf-8") as f:
            f.seek(target * 501)
            raw = f.readline().rstrip("\n")
            parts = [p.strip() for p in raw.split(";")]
            parts[0] = new_vin
            new_line = ";".join(parts).ljust(500) + "\n"
            f.seek(target * 501)
            f.write(new_line)

        # Updating cars_index.txt
        entries = [(i, new_vin if i == target else v) for i, v in entries]
        with open(idx_path, "w", encoding="utf-8") as f:
            for i, v in entries:
                f.write(f"{i};{v}\n")

        
        return Car(
            vin=new_vin,
            model=int(parts[1]),
            price=Decimal(parts[2]),
            date_start=datetime.strptime(parts[3], "%Y-%m-%d"),
            status=CarStatus(parts[4])
        )



    # Задание 6. Откат продажи
    def revert_sale(self, sales_number: str) -> Car:
        sales_txt = os.path.join(self.root_directory_path, "sales.txt")
        kept = []
        restored_vin = None
        
        # Looking for a necessarz string
        with open(sales_txt, "r", encoding="utf-8") as f:
            for line in f:
                sn, vin, cost, date_str = line.strip().split(";")
                if sn == sales_number:
                    restored_vin = vin
                else:
                    kept.append(line)
        if restored_vin is None:
            raise ValueError(f"Sale {sales_number} not found")

        # Re-writing sales.txt
        with open(sales_txt, "w", encoding="utf-8") as f:
            f.writelines(kept)

        
        cars_idx = os.path.join(self.root_directory_path, "cars_index.txt")
        car_line = None
        with open(cars_idx, "r", encoding="utf-8") as f:
            for line in f:
                idx, vin = line.strip().split(";")
                if vin == restored_vin:
                    car_line = int(idx)
                    break

        cars_txt = os.path.join(self.root_directory_path, "cars.txt")
        with open(cars_txt, "r+", encoding="utf-8") as f:
            f.seek(car_line * 501)
            raw = f.readline().rstrip("\n")
            parts = raw.split(";")
            parts[4] = CarStatus.available.value
            new_line = ";".join(parts).ljust(500) + "\n"
            f.seek(car_line * 501)
            f.write(new_line)

        return Car(
            vin=restored_vin,
            model=int(parts[1]),
            price=Decimal(parts[2]),
            date_start=datetime.strptime(parts[3], "%Y-%m-%d"),
            status=CarStatus.available,
        )


    def top_models_by_sales(self) -> list[ModelSaleStats]:
        
        cars_idx = {}
        idx_path = os.path.join(self.root_directory_path, "cars_index.txt")
        with open(idx_path, "r", encoding="utf-8") as f:
            for rec in f:
                idx, vin = rec.strip().split(";")
                cars_idx[vin] = int(idx)

        # 2) counting by model_id
        counts: dict[int,int] = {}
        sales_path = os.path.join(self.root_directory_path, "sales.txt")
        with open(sales_path, "r", encoding="utf-8") as f:
            for rec in f:
                _, vin, _, _ = rec.strip().split(";")
                if vin not in cars_idx:
                    continue
                car_pos = cars_idx[vin]

                
                cars_path = os.path.join(self.root_directory_path, "cars.txt")
                with open(cars_path, "r", encoding="utf-8") as cf:
                    cf.seek(car_pos * 501)
                    raw_block = cf.read(501)           # 500 chars + "\n"
                raw = raw_block.rstrip("\n")
                car_fields = [p.strip() for p in raw.split(";")]
                # теперь гарантированно car_fields[1] существует
                mid = int(car_fields[1])
                counts[mid] = counts.get(mid, 0) + 1

        # Preparing a dictionary
        model_pos = {}
        midx_path = os.path.join(self.root_directory_path, "models_index.txt")
        with open(midx_path, "r", encoding="utf-8") as f:
            for rec in f:
                idx, mid = rec.strip().split(";")
                model_pos[int(mid)] = int(idx)

        
        stats: list[ModelSaleStats] = []
        models_path = os.path.join(self.root_directory_path, "models.txt")
        for mid, cnt in counts.items():
            pos = model_pos[mid]
            with open(models_path, "r", encoding="utf-8") as mf:
                mf.seek(pos * 501)
                raw_block = mf.read(501)
            raw = raw_block.rstrip("\n")
            mf_fields = [p.strip() for p in raw.split(";")]
            brand = mf_fields[1]
            name  = mf_fields[2]
            stats.append(ModelSaleStats(
                car_model_name=name,
                brand=brand,
                sales_number=cnt
            ))

        # sorting
        stats.sort(key=lambda s: s.sales_number, reverse=True)
        return stats[:3]