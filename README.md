# RISC-V Assembler and Simulator

A custom implementation of a subset of the RV32I RISC-V Instruction Set Architecture developed as part of a Computer Organization course project.

## Features

### Assembler
- Converts RISC-V assembly instructions to 32-bit machine code
- Supports:
  - R-Type Instructions
    - add
    - sub
    - slt
    - srl
    - or
    - and

  - I-Type Instructions
    - lw
    - addi
    - jalr

  - S-Type Instructions
    - sw

  - B-Type Instructions
    - beq
    - bne

  - J-Type Instructions
    - jal

- Label resolution support
- Virtual halt support
- Error detection

### Simulator

- Executes generated machine code
- Maintains:
  - Program Counter
  - Register File
  - Data Memory

- Generates execution traces
- Supports memory operations
- Supports branching and jumping instructions

### Bonus Features

- rst instruction
- halt instruction
- mul instruction support

## Project Structure

```text
Assembler.py
Simulator.py
automatedTesting/
docs/
