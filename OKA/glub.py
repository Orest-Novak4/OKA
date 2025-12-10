from abc import ABC, abstractmethod


class Transport(ABC):
    def __init__(self, name: str, speed: int, capacity: int):
        self.name = name
        self.speed = speed
        self.capacity = capacity

    @abstractmethod
    def move(self, distance: int) -> float:
        """Повертає час у годинах."""
        pass

    @abstractmethod
    def fuel_consumption(self, distance: int) -> float:
        """Повертає витрати пального."""
        pass

    @abstractmethod
    def info(self) -> str:
        """Короткий опис транспорту."""
        pass

    def calculate_cost(self, distance: int, price_per_unit: float) -> float:
        """Повертає вартість витраченого ресурсу (пальне/заряд)."""
        return self.fuel_consumption(distance) * price_per_unit


class Car(Transport):
    def move(self, distance: int) -> float:
        return distance / self.speed

    def fuel_consumption(self, distance: int) -> float:
        return distance * 0.07

    def info(self) -> str:
        return f"Car: {self.name}, speed={self.speed}, capacity={self.capacity}"


class Bus(Transport):
    def __init__(self, name: str, speed: int, capacity: int, passengers: int):
        super().__init__(name, speed, capacity)
        self.passengers = passengers

    def move(self, distance: int) -> float:
        return distance / self.speed

    def fuel_consumption(self, distance: int) -> float:
        if self.passengers > self.capacity:
            print("Перевантажено!")
        return distance * 0.15

    def info(self) -> str:
        return f"Bus: {self.name}, speed={self.speed}, capacity={self.capacity}, passengers={self.passengers}"


class Bicycle(Transport):
    def __init__(self, name: str, capacity: int = 1):
        super().__init__(name, speed=20, capacity=capacity) 

    def move(self, distance: int) -> float:
        return distance / self.speed

    def fuel_consumption(self, distance: int) -> float:
        return 0.0

    def info(self) -> str:
        return f"Bicycle: {self.name}, speed={self.speed}, capacity={self.capacity}"


class ElectricCar(Car):
    def battery_usage(self, distance: int) -> float:
        return distance * 0.2

    def fuel_consumption(self, distance: int) -> float:
        return 0.0  

    def info(self) -> str:
        return f"ElectricCar: {self.name}, speed={self.speed}, capacity={self.capacity}"

vehicles = [
    Car("Toyota", 120, 5),
    Bus("Volvo Bus", 80, 50, passengers=60), 
    Bicycle("CrossBike"),
    ElectricCar("Tesla Model 3", 150, 5)
]

distance = 100  

for v in vehicles:
    print("————————————")
    print(v.info())
    print(f"Час у дорозі на {distance} км: {v.move(distance):.2f} год")
    print(f"Витрати пального/заряду: {v.fuel_consumption(distance)}")
