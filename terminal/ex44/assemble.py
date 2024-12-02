import sys
import struct
import csv

def assemble_line(line):
    parts = line.strip().split()
    command = parts[0]

    if command == 'LOAD_CONST':
        constant = int(parts[1])
        return struct.pack('BBB', 0x90, constant & 0xFF, (constant >> 8) & 0xFF)

    elif command == 'READ':
        return struct.pack('BBB', 0x02, 0x00, 0x00)

    elif command == 'WRITE':
        address = int(parts[1])
        return struct.pack('BBB', 0x63, address & 0xFF, (address >> 8) & 0xFF)

    elif command == 'CIRCULAR_SHIFT_LEFT':
        shift = int(parts[1])
        return struct.pack('BBB', 0x37, shift & 0xFF, (shift >> 8) & 0xFF)

    return b''

def main(input_file, output_file, log_file):
    instructions = []
    
    with open(input_file, 'r') as infile:
        for line in infile:
            if not line.strip():
                continue
            instruction = assemble_line(line)
            instructions.append(instruction)

    with open(output_file, 'wb') as outfile:
        for instruction in instructions:
            outfile.write(instruction)

    # Log in CSV format
    with open(log_file, 'w', newline='') as logfile:
        log_writer = csv.writer(logfile)
        log_writer.writerow(['Instruction', 'Hex Representation'])
        for line, instruction in zip(open(input_file), instructions):
            log_writer.writerow([line.strip(), instruction.hex()])

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python assembler.py input.asm output.bin log.csv")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
