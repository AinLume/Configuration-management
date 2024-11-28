import argparse
import csv

class VirtualMachine:
    def __init__(self, memory_size):
        self.stack = []  # Стек для данных
        self.memory = [0] * memory_size  # Инициализация памяти
        self.memory_size = memory_size

    def load_const(self, value):
        """Загружаем константу на стек"""
        self.stack.append(value)

    def read_mem(self, address):
        """Чтение значения из памяти"""
        value = self.memory[address]
        self.stack.append(value)

    def write_mem(self, address):
        """Запись значения в память"""
        value = self.stack.pop()
        self.memory[address] = value

    def shift_left(self, shift_value):
        """Циклический побитовый сдвиг влево"""
        value = self.stack.pop()
        # Циклический сдвиг влево
        result = ((value << shift_value) & 0xFF) | (value >> (8 - shift_value))
        self.stack.append(result)

    def execute(self, bytecode):
        """Исполнение программы"""
        i = 0
        while i < len(bytecode):
            cmd = bytecode[i]
            if cmd == 0x90:  # Загрузка константы
                B = bytecode[i + 1]
                self.load_const(B)
                i += 3
            elif cmd == 0x02:  # Чтение из памяти
                A = bytecode[i + 2]
                self.read_mem(A)
                i += 3
            elif cmd == 0x63:  # Запись в память
                B = bytecode[i + 1]
                self.write_mem(B)
                i += 3
            elif cmd == 0x37:  # Сдвиг влево
                B = bytecode[i + 1]
                self.shift_left(B)
                i += 3
            else:
                raise ValueError(f"Неизвестная команда: {cmd}")

def main():
    parser = argparse.ArgumentParser(description="Интерпретатор для виртуальной машины")
    parser.add_argument('input_bin', help="Путь к входному бинарному файлу")
    parser.add_argument('memory_range', help="Диапазон памяти для вывода результатов в формате 'start-end'")
    parser.add_argument('output_csv', help="Путь к выходному CSV файлу с результатами")

    args = parser.parse_args()

    # Чтение бинарного файла
    with open(args.input_bin, 'rb') as f:
        bytecode = list(f.read())

    # Разбор диапазона памяти
    start, end = map(int, args.memory_range.split('-'))

    # Проверка диапазона
    if start > end:
        raise ValueError("Неверный диапазон памяти: start должен быть меньше end.")
    
    if start < 0 or end >= 256:  # Память ограничена размером 256
        raise ValueError("Диапазон памяти должен быть от 0 до 255.")

    # Создание виртуальной машины
    vm = VirtualMachine(memory_size=256)  # Инициализируем память размером 256

    # Выполнение программы
    vm.execute(bytecode)

    # Сохранение результатов в CSV
    with open(args.output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(start, end + 1):
            writer.writerow([i, vm.memory[i]])

    print(f"Результаты сохранены в {args.output_csv}")

if __name__ == "__main__":
    main()
