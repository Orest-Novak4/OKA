a = float(input("Введи перше число: "))
b = float(input("Введи друге число: "))
op = input("Введи операцію (+, -, *, /): ")

if op == "+":
    result = a + b
elif op == "-":
    result = a - b
elif op == "*":
    result = a * b
elif op == "/":
    if b == 0:
        result = "Помилка: ділення на нуль!"
    else:
        result = a / b
else:
    result = "Невідома операція!"

print("Результат:", result)
