RType = {
    "ADD"  : ["0", "5"], 
    "SUB"  : ["0", "9"],  
    "CMP"  : ["0", "B"],
    "AND"  : ["0", "1"],   
    "OR"   : ["0", "2"],   
    "XOR"  : ["0", "3"], 
    "MOV"  : ["0", "D"],  
    "LSH"  : ["8", "4"], 
    "LOAD" : ["4", "0"], 
    "STOR" : ["4", "4"],
    "JAL" : ["4","8"]
}

ITypeZero = {
    "ANDI" : "1",
    "ORI" : "2",
    "XORI" : "3",
    "MOVI" : "D",
    "LUI" : "F"
}

ITypeSign = {
    "ADDI" : "5",
    "SUBI" : "9",
    "CMPI" : "B",
}

Conditions = {
    "EQ" : "0",
    "NE" : "1",
    "GE" : "D",
    "CS" : "2",
    "CC" : "3",
    "HI" : "4",
    "LS" : "5",
    "LO" : "A",
    "HS" : "B",
    "GT" : "6",
    "LE" : "7",
    "FS" : "8",
    "FC" : "0",
    "LT" : "C",
    "UC" : "E"
}

def convert_register_to_hex(value):
    number = int(value.strip('$'), 10)
    return hex(number)[2:].upper()

def convert_immediate_to_hex(number_str):
    number = int(number_str)
    if number < -128 or number > 127:
        raise ValueError("Input must be within the range -128 to 127 for 8-bit signed values.")
    if number < 0:
        number = (1 << 8) + number
    return format(number, '02X')

def convert_immediate_to_zero_extend_hex(number_str):
    number = int(number_str)

    # Ensure the number is within the unsigned 8-bit range
    if number < 0 or number > 255:
        raise ValueError("Input must be within the range 0 to 255 for 8-bit unsigned values.")

    # Format the number as a 2-character hexadecimal string
    return format(number, '02X')

def convert_immediate_to_hex_lsh_rsh(number_str):
    number = int(number_str)
    
    # Ensure the input is within the range -7 to 7
    if number < -7 or number > 7:
        raise ValueError("Input must be within the range -7 to 7.")
    
    # If the number is negative, calculate its two's complement in 4-bit format
    if number < 0:
        number = (1 << 4) + number  # Convert to two's complement (4-bit)

    # Return the hex value (will be a single digit)
    return format(number, 'X')

def parse_jal_instruction(line):
    opCode, opExt = RType[line[0]]
    r_target = convert_register_to_hex(line[1])
    return opCode + "0" + opExt + r_target

def parse_store_instruction(line):
    opCode, opExt = RType[line[0]]
    r_src = convert_register_to_hex(line[1])
    r_dest = convert_register_to_hex(line[2])
    return opCode + r_src + opExt + r_dest

def parse_r_type_instruction(line):
    opCode, opExt = RType[line[0]]
    r_src = convert_register_to_hex(line[1])
    r_dest = convert_register_to_hex(line[2])
    return opCode + r_dest + opExt + r_src

def parse_i_type_sign_instruction(line):
    opCode = ITypeSign[line[0]]
    r_dest = convert_register_to_hex(line[2])
    immediate = convert_immediate_to_hex(line[1])
    return opCode + r_dest + immediate

def parse_i_type_zero_extended(line):
    opCode = ITypeZero[line[0]]
    r_dest = convert_register_to_hex(line[2])
    immediate = convert_immediate_to_zero_extend_hex(line[1])
    return opCode + r_dest + immediate

def parse_lsh_rsh_i_type(line):
    opCode = "8"
    if line[0] == "LSHI":
        opExt = "0"
    else:
        opExt = "7"
    r_dest = convert_register_to_hex(line[2])
    immediate = convert_immediate_to_hex_lsh_rsh(line[1])
    return opCode + r_dest + opExt + immediate


def parse_conditional_instruction(line):
    if line[0][0] == "J":
        opCode, opExt = "4", "C"
        condition = Conditions[line[0][1:]]
        r_target = convert_register_to_hex(line[1])
        return opCode + condition + opExt + r_target
    elif line[0][0] == "B":
        opCode = "C"
        condition = Conditions[line[0][1:]]
        disp = convert_immediate_to_hex(line[1])
        return opCode + condition + disp

def convert_instructions_to_hex(file_path):
    converted_instructions = []
    counter = 0
    with open(file_path, 'r') as file:

        # Read the file line by line
        for instruction in file:
            instruction = instruction.strip()
            if not instruction:
                continue

            for i in range(len(instruction)):
                if i == "#":
                    instruction = instruction[:i]

            elements = instruction.split()
            if len(elements) < 2:
                continue

            
            if elements[0] == "STOR":
                parsed_instruction = parse_store_instruction(elements)
                converted_instructions.append(parsed_instruction)
            elif elements[0] == "LSHI" or elements[0] == "RSHI":
                parsed_instruction = parse_lsh_rsh_i_type(elements)
                converted_instructions.append(parsed_instruction)
            elif elements[0] == "JAL": # If its an JAL instruction
                parsed_instruction = parse_jal_instruction(elements)
                converted_instructions.append(parsed_instruction)
            elif elements[0] in RType: # If its an Rtype instruction
                parsed_instruction = parse_r_type_instruction(elements)
                converted_instructions.append(parsed_instruction)
            elif elements[0] in ITypeSign: # If its an IType instruction
                parsed_instruction = parse_i_type_sign_instruction(elements)
                converted_instructions.append(parsed_instruction)
            elif elements[0] in ITypeZero:
                parsed_instruction = parse_i_type_zero_extended(elements)
                converted_instructions.append(parsed_instruction)
            else: # If its an conditional instruction
                parsed_instruction = parse_conditional_instruction(elements)
                converted_instructions.append(parsed_instruction)

            if converted_instructions[-1] == None:
                converted_instructions = converted_instructions[:-1]
        return converted_instructions

if __name__ == "__main__":
    file_path = 'test_instructions.txt'
    converted_instructions = convert_instructions_to_hex(file_path)
    memory = ["0000" for _ in range(2 ** 16)]
    address = 0x0000
    for instr in converted_instructions:
        print(instr)
        memory[address] = instr
        address += 1

    output_file_path = 'memory_output.txt'
    with open(output_file_path, 'w') as output_file:
        for mem in memory:
            output_file.write(mem + '\n')
