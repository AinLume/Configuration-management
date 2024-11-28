import argparse
import xml.etree.ElementTree as ET

# Функция для обработки массива
def process_array(values):
    return '#(' + ', '.join(values) + ')'

# Функция для обработки словаря
def process_dict(dictionary):
    return '{\n' + '\n'.join([f'  {key} = {value}' for key, value in dictionary.items()]) + '\n}'

# Функция для обработки объявления константы
def process_constant(name, value):
    return f'{name} := {value}'

# Функция для обработки вычисления константы
def process_computation(name):
    return f'![{name}]'

# Функция для преобразования XML в конфигурационный язык
def process_xml(xml_string):
    root = ET.fromstring(xml_string)
    output = []

    for elem in root:
        if elem.tag == 'array':
            # Обрабатываем массивы
            array_values = [child.text for child in elem]
            output.append(process_array(array_values))
        elif elem.tag == 'dict':
            # Обрабатываем словари
            dictionary = {child.attrib['name']: child.text for child in elem}
            output.append(process_dict(dictionary))
        elif elem.tag == 'constant_declaration':
            # Обрабатываем объявление констант
            name = elem.attrib['name']
            value = elem.text
            output.append(process_constant(name, value))
        elif elem.tag == 'constant_computation':
            # Обрабатываем вычисление константы
            name = elem.attrib['name']
            output.append(process_computation(name))
        else:
            raise ValueError(f"Неизвестный элемент: {elem.tag}")
    
    return '\n'.join(output)

# Функция для чтения XML из файла
def read_input_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Функция для записи в выходной файл
def write_output_file(file_path, output):
    with open(file_path, 'w') as file:
        file.write(output)

# Основная функция для обработки командной строки
def main():
    parser = argparse.ArgumentParser(description="Преобразование XML в конфигурационный язык.")
    parser.add_argument('input', help="Путь к входному XML файлу.")
    parser.add_argument('output', help="Путь к выходному файлу для конфигурационного языка.")
    
    args = parser.parse_args()

    try:
        # Чтение входных данных
        xml_string = read_input_file(args.input)

        # Преобразование в конфигурационный язык
        result = process_xml(xml_string)

        # Запись результата в выходной файл
        write_output_file(args.output, result)
        print(f"Преобразование завершено. Результат записан в {args.output}")
    
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
