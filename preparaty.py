preparaty = [
    {"name": "Амоксицилін", "quantity": 10, "category": "antibiotic", "temperature": 8.0},
    {"name": "Вітамін C", "quantity": 20, "category": "vitamin", "temperature": 22.5},
    {"name": "Вакцина БЦЖ", "quantity": 5, "category": "vaccine", "temperature": 2.0},
    {"name": "НевідомийПрепарат", "quantity": 15, "category": "herbal", "temperature": 18.0},
    {"name": "Зіпсований", "quantity": 10, "category": "antibiotic", "temperature": 10.0},
    {"name": "Ще один", "quantity": 5, "category": "vitamin", "temperature": 30.0},
    {"name": "ТемпературнаПомилка", "quantity": 5, "category": "vaccine", "temperature": "hot"}
]

for prep in preparaty:
    name = prep.get("name")
    quantity = prep.get("quantity")
    category = prep.get("category")
    temperature = prep.get("temperature")

    if not isinstance(quantity, int) or not isinstance(temperature, (int, float)):
        print(f"{name}: Помилка даних")
       
       

    if temperature < 5:
        temp_status = "Надто холодно"
    elif temperature > 25:
        temp_status = "Надто жарко"
    else:
        temp_status = "Норма"

    match category:
        case "antibiotic":
            category_status = "Рецептурний препарат"
        case "vitamin":
            category_status = "Вільний продаж"
        case "vaccine":
            category_status = "Потребує спецзберігання"
        case _:
            category_status = "Невідома категорія"

    print(f"{name}: {category_status}, {temp_status}")