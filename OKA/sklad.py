class JunkItem:
    def __init__(self, name, quantity, value):
        self.name = name
        self.quantity = quantity
        self.value = value

    def __repr__(self):
        return f"{self.name} (x{self.quantity}, {self.value})"


class JunkStorage:
    @staticmethod
    def serialize(items, filename):
        with open(filename, "w", encoding="utf-8") as f:
            for item in items:
                line = f"{item.name}|{item.quantity}|{str(item.value).replace('.', ',')}\n"
                f.write(line)

    @staticmethod
    def parse(filename):
        items = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) != 3:
                    print(" Пропущено рядок (не 3 поля):", line.strip())
                    continue

                name, qty, val = parts
                try:
                    quantity = int(qty)
                    value = float(val.replace(",", "."))
                except ValueError:
                    print(" Пропущено рядок (не число):", line.strip())
                    continue

                items.append(JunkItem(name, quantity, value))
        return items


items = [
    JunkItem("Бляшанка", 5, 2.5),
    JunkItem("Стара плата", 3, 7.8),
    JunkItem("Купка дротів", 10, 1.2)
]

filename = "junk.csv"

JunkStorage.serialize(items, filename)
print(" Дані записано у файл.")

restored = JunkStorage.parse(filename)
print("\n Відновлені предмети:")
for item in restored:
    print(item)
