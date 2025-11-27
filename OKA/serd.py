def calculate(expression: str) -> float:
    expression = expression.replace(" ", "")  
    
    def parse_number(i):
        num = 0
        while i < len(expression) and expression[i].isdigit():
            num = num * 10 + int(expression[i])
            i += 1
        return num, i
    
    def parse_atom(i):
        if expression[i].isdigit():
            return parse_number(i)
        
        if expression[i] == '(':
            val, i = parse_expression(i + 1)
            if i >= len(expression) or expression[i] != ')':
                raise ValueError("Немає закриваючої дужки")
            return val, i + 1
        
        if expression[i] == '-':
            val, i = parse_atom(i + 1)
            return -val, i
        
        raise ValueError(f"Невідомий символ: {expression[i]}")
    
    def parse_power(i):
        val, i = parse_atom(i)
        
        while i < len(expression) and expression[i] == '^':
            op = expression[i]
            right, i = parse_atom(i + 1)
            if op == '^':
                val = val ** right
        return val, i
    
    def parse_term(i):
        val, i = parse_power(i)
        
        while i < len(expression) and expression[i] in '*/':
            op = expression[i]
            right, i = parse_power(i + 1)
            if op == '*':
                val *= right
            else: 
                if right == 0:
                    raise ZeroDivisionError("Ділення на нуль!")
                val /= right
        return val, i
    
    def parse_expression(i):
        val, i = parse_term(i)
        
        while i < len(expression) and expression[i] in '+-':
            op = expression[i]
            right, i = parse_term(i + 1)
            if op == '+':
                val += right
            else:
                val -= right
        return val, i
    
    try:
        result, pos = parse_expression(0)
        if pos != len(expression):
            raise ValueError(f"Зайві символи в кінці: {expression[pos:]}")
        return result
    except Exception as e:
        return f"ПОМИЛКА: {str(e)}"

tests = [
    "2 + 3 * 4 - 1",
    "(2 + 3) * 4",
    "2 * (3 + 4 * (5 - 2))",
    "10 / 2 / 5",
    "2^3^2",
    "2^(3^2)",
    "(2+3)*--4",
    "-3^2",
    "(-3)^2",
    "2*-3 + 5",
    "100 - 5 * 2 + 3 * 4",
    "((((10))))",
    "2 + 2",
    "0.5 * 4",
    "5 / 0",
    "2 + abc"
]

print("🚀 Калькулятор запущено!\n")
for t in tests:
    print(f"{t:25} → {calculate(t)}")