"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.fl = 0
        # self.SP = 0

    #provided
    def load(self, program):
        """Load a program into memory."""
        # if len(sys.argv) != 2:
        #     print("usage: comp.py filename")
        #     sys.exit(1)
        # print('middle of load')
        address = 0
        # with open(program) as f:
        for line in program:
            # print(line)
            # line = line.strip()
            # print('')
            # print(line)
            split_line = line.split("#")[0]
            if split_line == '':
                continue
            final_val = int(split_line, 2)
            self.ram[address] = final_val
            address += 1
        
    #provided
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]

        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        
        elif op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            op_a = self.reg[reg_a]
            op_b = self.reg[reg_b]
            # self.alu('CMP', operand_a, operand_b)
            if op_a == op_b:
                self.fl = 0b00000001
            elif op_a > op_b:
                self.fl = 0b00000010
            elif op_a < op_b:
                self.fl = 0b00000100
        else:
            raise Exception("Unsupported ALU operation")

    #provided
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
    
    def run(self):
        """Run the CPU."""

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        CMP = 0b10100111
        JMP = 0b01010100
        JNE = 0b01010110
        JEQ = 0b01010101
        PRA = 0b01001000
        AND = 0b10101000
        XOR = 0b10101011

        SP = 255
        room_target = ''
        running = True
        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print('IR', IR)
            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
                
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            
            elif IR == PRA:
                room_target += chr(self.reg[operand_a])
                print(chr(self.reg[operand_a]))
                self.pc += 2

            elif IR == HLT:
                running = False
                self.pc += 1
                # sys.exit(0)

            elif IR == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            
            elif IR == ADD:
                self.alu('ADD', operand_a, operand_b)
                self.pc += 3

            #ALU
            elif IR == AND:
                self.alu('AND', operand_a, operand_b)
                self.pc += 3

            #ALU
            elif IR == XOR:
                self.alu('XOR', operand_a, operand_b)
                self.pc += 3

            elif IR == PUSH:
                reg = operand_a
                val = self.reg[reg]
                SP -= 1
                self.ram_write(SP, val)
                self.pc += 2

            elif IR == POP:
                val = self.ram[SP]
                self.reg[operand_a] = val
                SP += 1
                self.pc += 2

            elif IR == CALL:
                val = self.pc + 2 
                SP -= 1
                self.ram[SP] = val

                reg = self.ram[operand_a]
                subroutine_address = self.reg[reg]
                self.pc = subroutine_address

            elif IR == RET:
                return_address = self.ram[SP]
                self.pc = return_address
                SP += 1

            elif IR == CMP:
                self.alu('CMP', operand_a, operand_b) 
                self.pc += 3

            elif IR == JMP:
                reg = self.reg[operand_a]
                self.pc = reg
            
            elif IR == JNE:
                if self.fl == 0b00000000 or self.fl == 0b00000010 or self.fl == 0b00000100:
                    reg = self.reg[operand_a]
                    self.pc = reg
                else:
                    self.pc += 2
            
            elif IR == JEQ:
                if self.fl == 0b00000001:
                    reg = self.reg[operand_a]
                    self.pc = reg
                else:
                    self.pc += 2

        final_target = room_target[-3:]
        print('target', final_target)
        return final_target