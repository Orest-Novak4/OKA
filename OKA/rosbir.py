from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import csv


@dataclass(order=True)
class Item:
    category: str
    value: float

    name: str
    quantity: int
    condition: str
    location: str

    added_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))

    def total_value(self) -> float:
        return self.quantity * self.value

    def __str__(self):
        return f"[{self.category}] {self.name} ({self.quantity} шт.) — {self.value} грн/шт, стан: {self.condition}"


@dataclass
class Inventory:
    items: List[Item] = field(default_factory=list)

    def add_item(self, item: Item):
        self.items.append(item)

    def remove_item(self, name: str):
        self.items = [i for i in self.items if i.name != name]

    def find_by_category(self, category: str) -> List[Item]:
        return [i for i in self.items if i.category == category]

    def total_inventory_value(self) -> float:
        return sum(i.total_value() for i in self.items)


    def save_to_csv(self, filename: str):
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "name", "category", "quantity", "value",
                "condition", "location", "added_at"
            ])
            for item in self.items:
                writer.writerow([
                    item.name, item.category, item.quantity,
                    item.value, item.condition,
                    item.location, item.added_at
                ])

    def load_from_csv(self, filename: str):
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                item = Item(
                    name=row["name"],
                    category=row["category"],
                    quantity=int(row["quantity"]),
                    value=float(row["value"]),
                    condition=row["condition"],
                    location=row["location"],
                )
                item.added_at = row["added_at"]
                self.add_item(item)


    def export_summary(self) -> dict:
        summary = {}
        for item in self.items:
            summary[item.category] = summary.get(item.category, 0) + item.quantity
        return summary


    def filter_items(self, **kwargs) -> List[Item]:
        result = self.items
        for key, value in kwargs.items():
            result = [i for i in result if getattr(i, key) == value]
        return result

    def sort_items(self, key: str, reverse: bool = False) -> List[Item]:
        return sorted(self.items, key=lambda x: getattr(x, key), reverse=reverse)
