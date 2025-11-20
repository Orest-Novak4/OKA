from abc import ABC, abstractmethod


class Medicine(ABC):
    def __init__(self, name: str, quantity: int, price: float):
        if not isinstance(name, str):
            raise TypeError("name must be str")
        if not isinstance(quantity, int) or quantity < 0:
            raise TypeError("quantity must be a non-negative int")
        if not (isinstance(price, int) or isinstance(price, float)) or price < 0:
            raise TypeError("price must be a non-negative number")

        self.name = name
        self.quantity = quantity
        self.price = price

    @abstractmethod
    def requires_prescription(self) -> bool:
        pass

    @abstractmethod
    def storage_requirements(self) -> str:
        pass

    def total_price(self) -> float:
        """Базова реалізація — можна перевизначати."""
        return self.quantity * self.price

    @abstractmethod
    def info(self) -> str:
        """Повертає інформацію про препарат."""
        pass


class Antibiotic(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "8–15°C, темне місце"

    def info(self) -> str:
        return (
            f"[Antibiotic] {self.name}: {self.quantity} шт, ціна {self.total_price()} грн, "
            f"рецепт: {self.requires_prescription()}, зберігання: {self.storage_requirements()}"
        )


class Vitamin(Medicine):
    def requires_prescription(self) -> bool:
        return False

    def storage_requirements(self) -> str:
        return "15–25°C, сухо"

    def info(self) -> str:
        return (
            f"[Vitamin] {self.name}: {self.quantity} шт, ціна {self.total_price()} грн, "
            f"рецепт: {self.requires_prescription()}, зберігання: {self.storage_requirements()}"
        )


class Vaccine(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "2–8°C, холодильник"

    def total_price(self) -> float:
        """10% націнки."""
        return round((self.quantity * self.price) * 1.10, 2)

    def info(self) -> str:
        return (
            f"[Vaccine] {self.name}: {self.quantity} шт, ціна {self.total_price()} грн (з націнкою), "
            f"рецепт: {self.requires_prescription()}, зберігання: {self.storage_requirements()}"
        )
