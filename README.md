# RISC-V Assembler and Simulator

A custom implementation of a subset of the RV32I RISC-V Instruction Set Architecture developed as part of a Computer Organization course project.

## Overview

This project implements:

1. A RISC-V Assembler that translates assembly instructions into machine code.
2. A RISC-V Simulator that executes machine code and generates execution traces.
3. An Automated Testing Framework for validation and grading.

The project demonstrates concepts such as instruction encoding, program execution, memory management, register operations, branching, and system-level architecture design.

---

## Features

### Assembler

- Converts RISC-V assembly code into 32-bit machine code.
- Supports instruction parsing and encoding.
- Handles labels and branch targets.
- Validates instruction formats.
- Detects syntax and semantic errors.
- Supports virtual halt checking.

### Simulator

- Executes generated machine code.
- Simulates:
  - Program Counter (PC)
  - Register File
  - Data Memory
- Supports arithmetic, logical, memory, branch, and jump instructions.
- Generates execution traces for debugging and verification.

### Automated Testing

- Automated validation of assembler outputs.
- Automated validation of simulator outputs.
- Test case execution and grading support.

---

## Supported Instruction Types

### R-Type

- add
- sub
- slt
- srl
- or
- and

### I-Type

- addi
- lw
- jalr

### S-Type

- sw

### B-Type

- beq
- bne

### J-Type

- jal

### Bonus Instructions

- mul
- rst
- halt

---

## Project Structure

```text
Risc-V-Assembler-Simulator
│
├── Assembler.py
├── Simulator.py
│
├── automatedTesting/
│   ├── src/
│   └── tests/
│
├── docs/
│   ├── CO_Project_Guidelines.pdf
│   └── CO_Project_Instructions.txt
│
├── README.md
└── .gitignore
```

---

## Running the Assembler

Generate machine code from an assembly file:

```bash
python Assembler.py input.txt output.txt
```

Example:

```bash
python Assembler.py sample.asm machine_code.txt
```

---

## Running the Simulator

Execute machine code and generate traces:

```bash
python Simulator.py machine_code.txt trace.txt
```

Example:

```bash
python Simulator.py machine_code.txt execution_trace.txt
```

---

## Concepts Demonstrated

- Computer Organization
- Instruction Set Architecture (ISA)
- RISC-V RV32I
- Instruction Encoding
- Machine Code Generation
- Program Execution
- Register File Simulation
- Memory Simulation
- Branching and Control Flow
- Automated Testing

---

## Technologies Used

- Python
- RISC-V RV32I ISA
- Git
- GitHub

---

## Learning Outcomes

Through this project, the following concepts were implemented and explored:

- Assembly language translation
- Instruction decoding and execution
- CPU state management
- Register and memory modeling
- Control flow handling
- Systems programming fundamentals

---

## Contributors:

- Sourabh
- Mohit Gupta
- Mrityunjai
- Anushka


