def shadow(limit=200):
    def decorator(gen_func):
        def wrapper(*args, **kwargs):
            total = 0
            for event in gen_func(*args, **kwargs):

                parts = event.split()
                if len(parts) != 2:
                    print(f"⚠️ Некоректна транзакція: '{event}' — ігнорую")
                    continue

                action, value = parts[0], parts[1]

                if action not in ("payment", "refund", "transfer"):
                    print(f"⚠️ Незнайома операція: '{event}' — ігнорую")
                    continue

                try:
                    amount = float(value)
                except ValueError:
                    print(f"Сума не число: '{event}' — ігнорую")
                    continue

                total += amount
                print(f"Подія: {event}")

                if total > limit:
                    print("Тіньовий ліміт перевищено. Активую схему.")

                yield event

            return total
        return wrapper
    return decorator


@shadow(limit=200)
def transactions():
    yield "payment 120"
    yield "refund 50"
    yield "transfer 300"
    yield "free money!"  
    yield "payment xyz"  
    yield "steal 500"    


gen = transactions()
try:
    while True:
        next(gen)
except StopIteration as e:
    print(f"\nФінальна сума операцій: {e.value}")