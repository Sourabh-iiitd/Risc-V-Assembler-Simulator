import sys;
class RISCV:
    def __init__(self):
        self.opcodes={
            "add":0b0110011,"sub":0b0110011,"slt":0b0110011,
            "srl":0b0110011,"or":0b0110011,"and":0b0110011,
            "lw":0b0000011,"addi":0b0010011,"jalr":0b1100111,
            "sw":0b0100011,"beq":0b1100011,"bne":0b1100011,
            "jal":0b1101111,"rst":0b1110011, "halt":0b1111111
        }
        self.registers= {
        "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011",
        "tp": "00100", "t0": "00101", "t1": "00110", "t2": "00111",
        "s0": "01000", "s1": "01001", "a0": "01010", "a1": "01011",
        "a2": "01100", "a3": "01101", "a4": "01110", "a5": "01111",
        "a6": "10000", "a7": "10001", "s2": "10010", "s3": "10011",
        "s4": "10100", "s5": "10101", "s6": "10110", "s7": "10111",
        "s8": "11000", "s9": "11001", "s10": "11010", "s11": "11011",
        "t3": "11100", "t4": "11101", "t5": "11110", "t6": "11111"
        }
        self.funct3 = {
            "add": "000", "sub": "000", "slt": "010", "srl": "101",
            "or": "110", "and": "111", "lw": "010", "addi": "000",
            "jalr": "000", "sw": "010", "beq": "000", "bne": "001"
        } 
        self.funct7={
            "add": "0000000", "sub": "0100000", "slt": "0000000", "srl": "0000000", "or": "0000000", "and": "0000000", "mul": "0000001"
        }
        self.labels={}
        self.labels_position={}
        self.current=0
    
    def Dec_to_Bin(self, number, k):
        if (number>=0):
            Binary = bin(number)[2:]
        elif (number<0):
            Binary = bin((1 << k) + number)[2:]
        Binary = Binary.zfill(k)
        
        if len(Binary) > k:
            Binary = Binary[-k:]
        return Binary

    def R_Type(self, ins_name, ins_args):
        #ins_name, ins_args = instruction.split()
        rd, rs1, rs2 = ins_args.split(",")
        func7 = self.funct7[ins_name]
        func3 = self.funct3[ins_name]
        return f"{func7}{self.registers[rs2]}{self.registers[rs1]}{func3}{self.registers[rd]}{bin(self.opcodes[ins_name])[2:].zfill(7)}"

    def I_Type(self, ins_name, ins_eq):
        #ins_name,ins_eq = instruction.split()
        if ins_name in ["lw"]:
            a1,a2 = ins_eq.split(",")
            op2=a2.split("(")
            op2[1]=op2[1][0:2]
            a2 = op2[1]
            a3 = op2[0]
        else:
            a1,a2,a3 = ins_eq.split(",")
        opcode = format(self.opcodes[ins_name], '07b')
        funct3 = self.funct3[ins_name]
        imm1 = self.Dec_to_Bin(int(a3), 12)
        return f"{imm1}{self.registers[a2]}{funct3}{self.registers[a1]}{opcode}"
    
    def S_Type(self, ins_name, ins_op):
        #ins_name,ins_op = instruction.split()
        a1,a2 = ins_op.split(",")
        opcode = format(self.opcodes[ins_name], '07b')
        funct3 = self.funct3[ins_name]
        offset, base = a2.split("(")
        base = base[0:2]
        imm = self.Dec_to_Bin(int(offset), 12)
        imm1 = imm[:7]
        imm2 = imm[7:] 
        return f"{imm1}{self.registers[a1]}{self.registers[base]}{funct3}{imm2}{opcode}"
    
    def B_Type(self,ins_name,ins_eq,index):
        #ins_name,ins_eq = instruction.split()
        a1,a2,a3 = ins_eq.split(",")
        if a3 in self.labels_position:
            imm = (((self.labels_position[a3]-(index)))*2)
            imm = self.Dec_to_Bin(int(imm),12)
        else:
            imm = int(a3)/2
            imm = self.Dec_to_Bin(int(imm),12)
        imm12 = imm[0] 
        imm10_5 = imm[2:8] 
        imm4_1 = imm[8:12] 
        imm11 = imm[1]
        return f"{imm12}{imm10_5}{self.registers[a2]}{self.registers[a1]}{self.funct3[ins_name]}{imm4_1}{imm11}{bin(self.opcodes[ins_name])[2:]}"
    
    def J_Type(self,ins_name,ins_op,index):
        #ins_name,ins_op = instruction.split()
        a1,a2 = ins_op.split(",")
        if a2 in self.labels_position:
            imm = ((((self.labels_position[a2])-(index)))*2)
            imm = self.Dec_to_Bin(int(imm),20)
        else:
            imm = int(a2)/2
            imm = self.Dec_to_Bin(int(imm),20)
        imm20 = imm[0] 
        imm19_12 = imm[1:9] 
        imm11= imm[9] 
        imm10_1 = imm[10:20]
        return f"{imm20}{imm10_1}{imm11}{imm19_12}{self.registers[a1]}{bin(self.opcodes[ins_name])[2:]}"

    def encode_vhalt(self,instruction,rd, rs1, imm):
        opcode1=format(self.opcodes[instruction], '07b')
        funct3 = self.funct3[instruction]
        imm = format(imm& 0x1FFF, '013b')
        imm12 = imm[0] 
        imm10_5 = imm[1:7] 
        imm4_1 = imm[7:11] 
        imm11 = imm[11] 
        return f"{imm12}{imm10_5}{self.registers[rd]}{self.registers[rs1]}{funct3}{imm4_1}{imm11}{opcode1}"
        #return f"0000000{self.registers['zero']}{self.registers['zero']}00000000{opcode1}"

    def encode_r_type(self,instruction, rd, rs1, rs2):
        #opcode1=format(self.opcodes[instruction], '07b')
        opcode1=format(self.opcodes["rst"], '07b')
        #print(f"{funct7_map[instruction]}{self.registers[rs2]}{self.registers[rs1]}{funct3_map[instruction]}{self.registers[rd]}{opcode1}")
        return f"{self.funct7[instruction]}{self.registers[rs2]}{self.registers[rs1]}{self.funct3[instruction]}{self.registers[rd]}{opcode1}"

        
    def encode_halt(self,instruction):
        opcode1=format(self.opcodes[instruction], '07b')
        return f"0000000{self.registers['zero']}{self.registers['zero']}00000000{opcode1}"
    
    def encode_rst(self):
        rst_instructions = []
        for reg in self.registers.keys():  
            rst_instructions.append(self.encode_r_type("add", reg, "zero", "zero"))
        #print("\n".join(rst_instructions))
        return "\n".join(rst_instructions)

    def encode_no_oper(self,instr,rd, rs1, imm):
        opcode = format(self.opcodes[instr], '07b')
        funct3 = self.funct3[instr]
        imm1 = format(int(imm), '012b')
        return f"{imm1}{self.registers[rs1]}{funct3}{self.registers[rd]}{opcode}"
    
    def process_line(self,line, line_num):
        instruction=""
        inst_value=""
        label_n=""
        if ":" in line:
            assembly_instruct_l = line.split(":")
            label_n = assembly_instruct_l[0]
            assembly_instruct= assembly_instruct_l[1].split()
            instruction = assembly_instruct[0]  
            instruction = instruction.strip()
            if len(assembly_instruct) > 1:
                inst_arg = assembly_instruct[1]
                inst_arg_val = inst_arg.split(",")
        else:
            assembly_instruct = line.split()
            instruction = assembly_instruct[0]
            if len(assembly_instruct) > 1:
                inst_arg = assembly_instruct[1]
                inst_arg_val = inst_arg.split(",")
        index = line_num -1
        
        #label_check = assembly_instruct[0]
        try:
            if instruction in ["add","sub","slt","srl","or","and","mul"]:
                return self.R_Type(instruction,inst_arg)
            elif instruction in ["addi", "lw", "jalr"]: 
                if instruction == "addi" and inst_arg_val[0] =="zero" and inst_arg_val[1] =="zero" and inst_arg_val[2] =="0":
                    return self.encode_no_oper(instruction,inst_arg_val[0],inst_arg_val[1],inst_arg_val[2])
                else:
                    return self.I_Type(instruction,inst_arg)
            elif instruction in ["sw"]:
                return self.S_Type(instruction,inst_arg)
            elif instruction in ["beq", "bne"]:
                if inst_arg_val[2]=="0x00000000":
                    valH=int(inst_arg_val[2],16)
                    if instruction == "beq" and inst_arg_val[0] =="zero" and inst_arg_val[1] =="zero" and valH == 0:
                        return self.encode_vhalt(instruction,inst_arg_val[0],inst_arg_val[1],valH)
                return self.B_Type(instruction,inst_arg,index)
            elif instruction == "jal":
                return self.J_Type(instruction,inst_arg,index)
            elif instruction == "rst":
                return self.encode_rst()
            elif instruction == "halt":
                return self.encode_halt(instruction)
            else:
                return f"Error on line {line_num}: Unknown instruction '{instruction}'"
        except Exception as e:
            return f"Error on line {line_num}: {str(e)}"
    
    def read_file(self,input_file):
        with open(input_file, 'r') as inputfile:
            num=1
            for line in inputfile:
                if len(line.strip()):
                    if ":" in line :
                        assembly_instruct = line.split(":")
                        label_n=""
                        label_check = assembly_instruct[0]
                        #if((label_check[-1]==":") and 
                        index = num -1
                        if(label_check[0].isalpha()):
                            label_n = assembly_instruct[0]
                            label_n = label_n.strip()
                            self.labels_position[label_n]=index
                    num=num+1

    def process_file(self,input_file, output_file):
        with open(output_file, 'w') as outputfile:
            with open(input_file, 'r') as inputfile:
                errorfile = open("stdout.txt", "w")
                num =1
                for line in inputfile:
                    #print("line",line)
                    if len(line.strip()):
                        binary_code = self.process_line(line.strip(), num)
                        #print("binary_code",binary_code)
                        if None == binary_code:
                            print(binary_code)
                            errorfile.write(binary_code + '\n')
                            errorfile.close()
                            return
                        if "Error" in binary_code:
                            print(binary_code)
                            errorfile.write(binary_code + '\n')
                            errorfile.close()
                            return
                        if binary_code:
                            outputfile.write(binary_code + '\n')
                    num=num+1
        print("Successfully assembled to ", output_file)


# #inputFileName = input("Enter Assembler File Name with extension (e.g. filename.txt):")
# inputFileName=""
# fileName=["Ex_test_0","Ex_test_1","Ex_test_2","Ex_test_4","Ex_test_5","Ex_test_6",
#           "Ex_test_7","Ex_test_8",
#           "Ex_test_9","Ex_test_10","bonus_test"]
# #fileName1=["Ex_test_6"]
# outPutFileName ="bin_"+inputFileName
# riscv = RISCV()
# for i in fileName:
#     riscv.read_file(i+".txt")
#     outPutFileName ="bin_"+i+".txt"
#     riscv.process_file(i+".txt", outPutFileName)
input_file_name = sys.argv[1]
output_file_name = sys.argv[2]
# inputFileName = input("Enter Assembler File Name with extension (e.g. filename.txt):")
# outPutFileName ="bin_"+inputFileName
riscv = RISCV()
riscv.read_file(input_file_name)
riscv.process_file(input_file_name , output_file_name)