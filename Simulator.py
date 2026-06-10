import sys
class Simulator:
    def __init__(self):
        self.opcodes={
            "0110011":"add","0110011":"sub","0110011":"slt",
            "0110011":"srl","0110011":"or","0110011":"and",
            "0000011":"lw","0010011":"addi","1100111":"jalr",
            "0100011":"sw","1100011":"beq","1100011":"bne",
            "1101111":"jal","1110011":"rst","1111111":"halt"
        }
        self.registers = {
            "00000": "zero", "00001": "ra", "00010": "sp", "00011": "gp",
            "00100": "tp", "00101": "t0", "00110": "t1", "00111": "t2",
            "01000": "s0", "01001": "s1", "01010": "a0", "01011": "a1",
            "01100": "a2", "01101": "a3", "01110": "a4", "01111": "a5",
            "10000": "a6", "10001": "a7", "10010": "s2", "10011": "s3",
            "10100": "s4", "10101": "s5", "10110": "s6", "10111": "s7",
            "11000": "s8", "11001": "s9", "11010": "s10", "11011": "s11",
            "11100": "t3", "11101": "t4", "11110": "t5", "11111": "t6"
        }
        self.datamemory = {
            "10000": 0, "10004": 0, "10008": 0, "1000C": 0,
            "10010": 0, "10014": 0, "10018": 0, "1001C": 0,
            "10020": 0, "10024": 0, "10028": 0, "1002C": 0,
            "10030": 0, "10034": 0, "10038": 0, "1003C": 0,
            "10040": 0, "10044": 0, "10048": 0, "1004C": 0,
            "10050": 0, "10054": 0, "10058": 0, "1005C": 0,
            "10060": 0, "10064": 0, "10068": 0, "1006C": 0,
            "10070": 0, "10074": 0, "10078": 0, "1007C": 0
        }
        
        self.reg_value = {
        "zero": 0, "ra": 0, "sp": 380, "gp": 0,
        "tp": 0, "t0": 0, "t1": 0, "t2": 0,
        "s0": 0, "s1": 0, "a0": 0, "a1": 0,
        "a2": 0, "a3": 0, "a4": 0, "a5": 0,
        "a6": 0, "a7": 0, "s2": 0, "s3": 0,
        "s4": 0, "s5": 0, "s6": 0, "s7": 0,
        "s8": 0, "s9": 0, "s10": 0, "s11": 0,
        "t3": 0, "t4": 0, "t5": 0, "t6": 0
        }
        self.funct3 = {
            "000":"add", "000":"sub", "010":"slt", "101":"srl",
            "110":"or", "111":"and", "010":"lw", "000": "addi",
            "000":"jalr",  "010":"sw",  "000":"beq",  "001":"bne"
        } 
        self.funct7={
             "0000000":"add",  "0100000":"sub",  "0000000":"slt",  "0000000":"srl",  "0000000":"or",  "0000000":"and", "0000001":"mul"
        }
        self.Type_Flag = None
        self.PC = 0
        self.instruction_dict = {}

    def Bin_to_dec(self, num, bin_length):
        value = int(num, 2)
        if value >= 2**(bin_length - 1):
            value -= 2**bin_length
        return value
    
    def Dec_to_Bin(self, number, k):
        if (number>=0):
            Binary = bin(number)[2:]
        elif (number<0):
            Binary = bin((1 << k) + number)[2:]
        Binary = Binary.zfill(k)
        if len(Binary) > k:
            Binary = Binary[-k:]
        return Binary

    def decode(self,bin_code):
        opcode = bin_code[::-1][:7][::-1]
        instruction = self.opcodes[opcode]
        if instruction in ["add","sub","slt","srl","or","and","mul"]:
            self.Type_Flag = "R_Type"
            self.R_Type(bin_code)
        elif instruction in ["lw","jalr","addi"]:
            self.Type_Flag = "I_Type"
            self.I_Type(bin_code)
        elif instruction in ["sw"]:
            self.Type_Flag = "S_Type"
            self.S_Type(bin_code)
        elif instruction in ["beq","bne"]:
            self.Type_Flag = "B_Type"
            self.B_Type(bin_code)
        elif instruction in ["jal"]:
            self.Type_Flag = "J_Type"
            self.J_Type(bin_code)
        
    def R_Type(self,bin_code):
        func7 = bin_code[0:7]
        rs2 = bin_code[7:12]
        rs1 = bin_code[12:17]
        func3 = bin_code[17:20]
        rd = bin_code[20:25]
        opcode = bin_code[25:32]

        if(func3=="000" and func7=="0000000"): 
            self.reg_value[self.registers[rd]] = self.reg_value[self.registers[rs1]] + self.reg_value[self.registers[rs2]]
        elif(func3=="000" and func7=="0100000"):
            self.reg_value[self.registers[rd]] = self.reg_value[self.registers[rs1]] - self.reg_value[self.registers[rs2]]
        elif(func3=="010" and func7=="0000000"):
            if self.reg_value[self.registers[rs1]] < self.reg_value[self.registers[rs2]]:
                self.reg_value[self.registers[rd]] = 1
            else:
                self.reg_value[self.registers[rd]] = 0
        elif(func3=="101" and func7=="0000000"):
            bin_value_rs2 = self.Dec_to_Bin((self.reg_value[self.registers[rs2]]),32)
            bin_value_rs2 = bin_value_rs2[27:32]
            x = self.reg_value[self.registers[rs1]] >> self.Bin_to_dec((bin_value_rs2),5)
            self.reg_value[self.registers[rd]] = x
        elif(func3=="110" and func7=="0000000"):
            self.reg_value[self.registers[rd]] = self.reg_value[self.registers[rs1]] | self.reg_value[self.registers[rs2]]
        elif(func3=="111" and func7=="0000000"):
            self.reg_value[self.registers[rd]] = self.reg_value[self.registers[rs1]] & self.reg_value[self.registers[rs2]]
    
    def I_Type(self,bin_code):
        imm = bin_code[0:12]
        rs1 = bin_code[12:17]
        func3 = bin_code[17:20]
        rd = bin_code[20:25]
        opcode = bin_code[25:32]
        if(func3=="010" and opcode=="0000011"):
            address = self.reg_value[self.registers[rs1]] + self.Bin_to_dec(imm,12)
            address1=hex(address)
            mainaddress=address1[2:]
            if mainaddress in self.datamemory:
                self.reg_value[self.registers[rd]] = self.datamemory[mainaddress]       
        elif(func3=="000" and opcode=="0010011"):          
            self.reg_value[self.registers[rd]] =self.reg_value[self.registers[rs1]] + self.Bin_to_dec(imm,12)
        elif(func3=="000" and opcode=="1100111"):
            temp=self.PC
            self.PC = self.reg_value[self.registers[rs1]] + self.Bin_to_dec(imm,12)
            if(self.registers[rd]!="zero"):
                self.reg_value[self.registers[rd]] = temp

    def S_Type(self,bin_code):
        imm = bin_code[0:7]+bin_code[20:25]
        rs2 = bin_code[7:12]
        rs1 = bin_code[12:17]
        func3 = bin_code[17:20]
        opcode = bin_code[25:32]
        address=self.reg_value[self.registers[rs1]] + self.Bin_to_dec(imm,12)
        address1=hex(address)
        mainaddress=address1[2:]
        if(func3=="010" and opcode=="0100011"):
            self.datamemory[mainaddress] = self.reg_value[self.registers[rs2]]
        
    def B_Type(self,bin_code):
        imm = bin_code[0]+bin_code[24]+bin_code[1:7]+bin_code[20:24]
        immv = self.Dec_to_Bin(((self.Bin_to_dec(imm,12))*2),12)
        rs2 = bin_code[7:12]
        rs1 = bin_code[12:17]
        func3 = bin_code[17:20]
        opcode = bin_code[25:32]
        if func3 == "000" and opcode == "1100011": 
            if self.reg_value[self.registers[rs1]] == self.reg_value[self.registers[rs2]]:
                self.PC += self.Bin_to_dec(immv,12) - 4
        elif func3 == "001" and opcode == "1100011":  
            if self.reg_value[self.registers[rs1]] != self.reg_value[self.registers[rs2]]:
                self.PC += self.Bin_to_dec(immv,12) - 4
    
    def J_Type(self,bin_code):
        opcode = bin_code[25:32]
        rd = bin_code[20:25]
        imm = bin_code[0]+bin_code[12:20]+bin_code[11]+bin_code[1:11]
        imm = self.Dec_to_Bin(((self.Bin_to_dec(imm,20))*2),20)
        if opcode == "1101111":
            if(self.registers[rd]!="zero"):
                self.reg_value[self.registers[rd]] = self.PC
            if self.Bin_to_dec(imm,20)%4==0:    
                self.PC += self.Bin_to_dec(imm,20) - 4

    def Read_File(self,input_file):
        count = 4
        with open(input_file, "r") as file1:
            for line in file1:
                self.instruction_dict[count] = line.strip()
                count +=4
    def process_file(self, input_file, output_file):
        HALT="00000000000000000000000001100011"
        last_key = list(self.instruction_dict.keys())[-1]
        with open(output_file, "w") as file2:
            keys_iter = iter(self.instruction_dict)
            keys = next(keys_iter)             
            while(keys!=last_key):
                bin_code = self.instruction_dict[keys]
                if bin_code==HALT:
                    break
                self.PC+=4
                self.decode(bin_code)
                file2.write("0b"+self.Dec_to_Bin(self.PC,32))
                keys = self.PC+4
                for key, value in self.reg_value.items():
                    file2.write(f" 0b{self.Dec_to_Bin(value,32)}")
                file2.write(str("\n"))           
        with open(output_file, "a") as file:     
            file.write("0b"+self.Dec_to_Bin(self.PC,32))
            for key, value in self.reg_value.items():
                    file.write(f" 0b{self.Dec_to_Bin(value,32)}")
            file.write("\n")
            for key, value in self.datamemory.items():
                if "10000" <= key <= "1007C":
                    file.write(f"0x000{key}:0b{self.Dec_to_Bin(value,32)}\n")
                
                
# inputFileName = input("Enter Binary File Name: ")
# outputFileName = "output_" + inputFileName
inputFileName = sys.argv[1]
outputFileName = sys.argv[2]
sim = Simulator()
sim.Read_File(inputFileName)
sim.process_file(inputFileName, outputFileName)