from modelmed.py import Antibiotic, Vitamin, Vaccine


def print_medicine_info(medicines):
    """Поліморфна функція — ЖОДНИХ if-ів."""
    for m in medicines:
        print(m.info())


def main():
    meds = [
        Antibiotic("Амоксицилін", 20, 45.5),
        Vitamin("Вітамін C", 50, 5.0),
        Vaccine("Коронавак", 10, 250.0),
        Vitamin("D3", 30, 12.0),
        Antibiotic("Азитроміцин", 15, 60.0),
        Vaccine("Інфлувак", 5, 300.0),
    ]

    print_medicine_info(meds)


if __name__ == "__main__":
    main()
