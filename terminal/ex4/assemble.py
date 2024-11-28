import argparse
import csv

# Определение команд
COMMANDS = {
    'load_const': 0x90,  # Загрузка константы
    'read_mem': 0x02,    # Чтение значения из памяти
    'write_mem': 0x63,   # Запись значения в память
    'shift_left': 0x37   # Побитовый циклический сдвиг влево
}

# Функция для ассемблирования команд
def assemble(commands):
    bytecode = []
    log = []
    for command in commands:
        parts = command.split()
        cmd = parts[0]
        if cmd == 'load_const':
            B = int(parts[1], 16)
            bytecode.extend([COMMANDS['load_const'], B, 0x00])
            log.append(f"load_const={B:#04x}")
        elif cmd == 'read_mem':
            A = int(parts[1], 16)
            bytecode.extend([COMMANDS['read_mem'], 0x00, A])
            log.append(f"read_mem={A:#04x}")
        elif cmd == 'write_mem':
            A = int(parts[1], 16)
            B = int(parts[2], 16)
            bytecode.extend([COMMANDS['write_mem'], B, 0x00])
            log.append(f"write_mem={B:#04x}")
        elif cmd == 'shift_left':
            A = int(parts[1], 16)
            B = int(parts[2], 16)
            bytecode.extend([COMMANDS['shift_left'], 0x00, 0x00])
            log.append(f"shift_left={B:#04x}")
        else:
            raise ValueError(f"Неизвестная команда: {cmd}")
    return bytecode, log

# Сохранение бинарного файла
def save_binary(bytecode, binary_file):
    with open(binary_file, 'wb') as f:
        f.write(bytearray(bytecode))

# Сохранение лога в CSV
def save_log(log, log_file):
    with open(log_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for entry in log:
            writer.writerow([entry])

def assemble_shift_program(A, B):
    bytecode = []

    # Загрузим вектор A
    for i in range(len(A)):
        bytecode.append(0x90)  # Команда загрузки константы
        bytecode.append(A[i])  # Значение из A
        bytecode.append(0x00)  # Заглушка

    # Загрузим вектор B (сдвиговые значения)
    for i in range(len(B)):
        bytecode.append(0x90)  # Команда загрузки константы
        bytecode.append(B[i])  # Значение из B (сдвиг)
        bytecode.append(0x00)  # Заглушка

    # Выполним сдвиг для каждого элемента
    for i in range(len(A)):
        bytecode.append(0x37)  # Команда сдвига влево
        bytecode.append(B[i])  # Смещение из B
        bytecode.append(0x00)  # Заглушка

        bytecode.append(0x63)  # Запись в память
        bytecode.append(i)     # Адрес в памяти
        bytecode.append(0x00)  # Заглушка

    return bytecode

# Основная функция
def main():
    # parser = argparse.ArgumentParser(description="Ассемблер для учебной виртуальной машины")
    # parser.add_argument('input', help="Путь к входному файлу с исходным кодом")
    # parser.add_argument('output_bin', help="Путь к выходному бинарному файлу")
    # parser.add_argument('log_file', help="Путь к файлу лога")
    
    # args = parser.parse_args()

    # # Чтение входного файла
    # with open(args.input, 'r') as f:
    #     commands = f.read().strip().split('\n')

    # # Ассемблирование
    # bytecode, log = assemble(commands)

    # # Сохранение бинарного файла и лога
    # save_binary(bytecode, args.output_bin)
    # save_log(log, args.log_file)

    # print(f"Бинарный файл сохранен по пути {args.output_bin}")
    # print(f"Лог сохранен по пути {args.log_file}")
    
    parser = argparse.ArgumentParser(description="Ассемблер для виртуальной машины")
    parser.add_argument('output_file', help="Путь к выходному бинарному файлу")
    args = parser.parse_args()

    # Пример векторов A и B
    A = [1, 2, 3, 4, 5]
    B = [1, 2, 3, 4, 5]

    # Генерируем программу
    bytecode = assemble_shift_program(A, B)

    # Записываем в бинарный файл
    with open(args.output_file, 'wb') as f:
        f.write(bytearray(bytecode))

    print(f"Бинарный файл с программой записан в {args.output_file}")

if __name__ == "__main__":
    main()
