import time
from datetime import datetime

def polish_notation():
    print('Введите оператор и числа в формате + 1 1:')
    notation = input()
    notation_split = notation.split(' ')
    assert (len(notation_split) == 3), 'Проверьте количество чисел или количество пробелов!'
    assert (notation_split[0] in ['+', '-', '*', '/']), 'Проверьте значение оператора!'
    try:
        int1 = int(notation_split[1])
        int2 = int(notation_split[2])
    except ValueError:
        print('Неверно указаны числа')
        return
    if notation_split[0] == "+":
        print('Результат сложения:', int1 + int2)
    elif notation_split[0] == "-":
        print('Результат вычитания:', int1 - int2)
    elif notation_split[0] == "*":
        print('Результат умножения:', int1 * int2)
    elif notation_split[0] == "/":
        try:
            print('Результат деления:', round((int1 / int2), 1))
        except ZeroDivisionError:
            print('Делить на ноль нельзя!')


start_time = time.time()

print('Время начала выполнения функции:', datetime.now(tz=None))

polish_notation()
end_time = time.time()

print('Выполнение функции заняло %s секунд' % (end_time - start_time))
print('Время окончания выполнения функции:', datetime.now(tz=None))
