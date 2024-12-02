import sys
import csv

class SimpleVM:
    def __init__(self):
        self.stack = []
        self.memory = [0] * 1000  # Память размером 256 байт

    def load_program(self, program):
        self.program = program

    def run(self):
        pc = 0
        print("Len prog - " + str(len(self.program)))
        while pc < len(self.program):
            instruction = self.program[pc]
            print("Instruction - " + str(instruction) + "\niter - " + str(pc))
            opcode = instruction[0]

            if opcode == 0x90:  # LOAD_CONST
                constant_value = instruction[1] | (instruction[2] << 8)
                print("Const - " + str(constant_value))
                self.stack.append(constant_value)
                print("Stack - " + str(self.stack))

            elif opcode == 0x02:  # READ
                print("stack - " + str(self.stack))
                if len(self.stack) == 0:
                    raise IndexError("Pop from empty stack for READ instruction")
                address = self.stack.pop()
                if 0 <= address < len(self.memory):
                    self.stack.append(self.memory[address])
                else:
                    raise IndexError("Memory read out of range")

            elif opcode == 0x63:  # WRITE
                if len(self.stack) == 0:
                    raise IndexError("Pop from empty stack for WRITE instruction")
                value = self.stack.pop()
                address = instruction[1] | (instruction[2] << 8)
                if 0 <= address < len(self.memory):
                    self.memory[address] = value
                    self.stack.append(address)
                else:
                    raise IndexError("Memory write out of range")

            elif opcode == 0x37:  # CIRCULAR_SHIFT_LEFT
                if len(self.stack) == 0:
                    raise IndexError("Pop from empty stack for CIRCULAR_SHIFT_LEFT instruction")
                shift = instruction[1] | (instruction[2] << 8)
                value = self.stack.pop()

                if value < 0 or value >= len(self.memory):
                    raise IndexError("Value out of memory range for shifting")

                address = (value + shift) % len(self.memory)  # Prevent overflow
                self.memory[address] = ((self.memory[address] << 1) | (self.memory[address] >> 7)) & 0xFF  # Bitwise rotate left

            pc += 1

def main(binary_file, output_csv):
    with open(binary_file, 'rb') as f:
        program = []
        while byte := f.read(3):  # Чтение по 3 байта
            program.append(byte)

    vm = SimpleVM()
    vm.load_program(program)
    vm.run()

    # Сохранение памяти в CSV
    with open(output_csv, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Address', 'Value'])
        for address, value in enumerate(vm.memory):
            writer.writerow([address, value])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python interpreter.py program.bin output.csv")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])