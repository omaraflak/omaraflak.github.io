:title: Virtual Machine
:description: What is a virtual machine and how to create one?
:year: 2025
:month: 8
:day: 11

Virtual machines are a truely fascinating piece of software, and suprisingly simple. As you start understanding how they work and write your own, you will feel like you're discovering computers all over again. In this article I will explain what a virtual machine is, we will write some code that runs on a virtual machine, and see how simple constructs build up to create complex logic.

# Preamble

Your computer has a processor, or CPU (central processing unit), which is responsible for executing instructions, performing calculations, moving memory around, etc. It's the central piece of your computer, and yet at its core, you could reduce it to something very simple.

> A CPU is a machine that takes **instructions** as input, and executes **actions** as output.

Those instructions are very basic. You might have an instruction to add two numbers, to multiply two numbers, to read from a memory location, to write to a memory location, etc.

When some piece of code executes on your computer, it can go through convoluted paths involving various optimizations and pre-processing, but evenutally it **must** be transformed into instructions for the CPU to understand and execute.

> A virtual machine, VM, is a simulation of a CPU.

This simulation can be more or less complex, support more or less instructions, but the main idea stays the same.

There are multiple types of VM architectures, mainly: stack-based, register-based, or hybrid. In this article we will be playing around with a *hybrid* model.

# Programming Languages

CPUs come in various kinds, architectures, brands, etc. The instructions a CPU support are not necessarily the same across other CPUs. This already gives you a hint on something important: when you compile code, it has to be compiled *for a given CPU instruction set*.

Language such as C or C++ compile directly into machine code (CPU instructions), which means they run very fast, but it also means you have to write **one compiler per CPU architecture**.

Other languages, like Java, are based on virtual machines. For Java it's the **Java Virtual Machine**, or JVM. This means that code in Java does not compile into CPU instructions, but **VM instructions** (here, the JVM)! It is then the job of the JVM (which is just a piece of software) to execute the code. This means it's slower to execute since we've introduced a sort of middle-man between the code and the CPU, which is the VM. In other words, the code runs on the JVM, which runs on the CPU.

In return, the advantages of this approach are multiple:

- Any system that has the VM can run your code (so you don't have to write a compiler for each system)
- Anyone can create a new progamming language syntax and compile their code to your VM's instruction set (e.g. Scala, Kotlin, etc run on the JVM)
- Easier to maintain, extend, and debug

# Virtual Machine

Our virtual machine will have those components:

- A **stack** which holds temporary values for calculations, e.g. when computing `x=1+2`.
- A **memory** which holds persistent values in a given scope.
- A **program** which it has to run (a set of instructions).
- An **instruction pointer** which points to the current instruction in the *program* that is being executed.

We will support those instructions to start with:

- **`push <value>`** pushes a value to the stack.
- **`store <address>`** pops a value from the stack and stores it at the given address in the memory.
- **`load <address>`** reads a value at the given address from the memory and pushes it onto the stack.
- **`add`** pops two elements from the stack, computes the sum, and pushes the result onto the stack.
- **`sub`** pops two elements from the stack, computes the difference between the second and the first, and pushes the result onto the stack.
- **`jumpif <address>`** pops an element stack, and moves the instruction pointer to the given address if the value is greater than zero.
- **`print`** pops an element from the stack and prints it to stdout.
- **`halt`** stops the virtual machine.

`value` and `address` will be **int32** (4 bytes).

Here's a starter Python code:

```python
import dataclasses

class Op:
    PUSH = 0
    STORE = 1
    LOAD = 2
    ADD = 3
    SUB = 4
    JUMPIF = 5
    PRINT = 6
    HALT = 7

@dataclasses.dataclass
class Vm:
    program: bytes
    stack: list[int]
    memory: list[int]
    ip: int = 0

    def run(self):
        while self.ip < len(self.program):
            instruction = self.program[self.ip]
            # TODO: process instruction

program = [] # instructions to execute
vm = Vm(program=program, stack=[], memory=[0] * 32)
vm.run()
```

**Challenge!** Can you complete writing the code of the virtual machine on your own? (Remeber that *values* and *addresses* in the program are written over 4 bytes).

When you do, you can feed in the following program to get a surprise:

```python
program = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2, 0, 0, 0, 1, 3, 1, 0, 0, 0, 3, 2, 0, 0, 0, 3, 6, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 0, 3, 1, 0, 0, 0, 1, 2, 0, 0, 0, 2, 0, 0, 0, 0, 1, 3, 1, 0, 0, 0, 2, 0, 0, 0, 0, 20, 2, 0, 0, 0, 2, 4, 5, 0, 0, 0, 30, 7]
```

## Code

Here's the full code:

```python
import dataclasses

class Op:
    PUSH = 0
    STORE = 1
    LOAD = 2
    ADD = 3
    SUB = 4
    JUMPIF = 5
    PRINT = 6
    HALT = 7

@dataclasses.dataclass
class Vm:
    program: bytes
    stack: list[int]
    memory: list[int]
    ip: int = 0

    def push(self, value: int):
        self.stack.append(value)

    def store(self, index: int):
        self.memory[index] = self.stack.pop()

    def load(self, index: int):
        self.stack.append(self.memory[index])

    def add(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(a + b)

    def sub(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b - a)

    def jumpif(self, pointer: int):
        if self.stack.pop() > 0:
            self.ip = pointer

    def print(self):
        print(self.stack.pop())

    def run(self):
        while self.ip < len(self.program):
            instruction = self.program[self.ip]
            self.ip += 1

            if instruction == Op.PUSH:
                self.push(self._read_int32())
            elif instruction == Op.STORE:
                self.store(self._read_int32())
            elif instruction == Op.LOAD:
                self.load(self._read_int32())
            elif instruction == Op.ADD:
                self.add()
            elif instruction == Op.SUB:
                self.sub()
            elif instruction == Op.JUMPIF:
                self.jumpif(self._read_int32())
            elif instruction == Op.PRINT:
                self.print()
            elif instruction == Op.HALT:
                break
            else:
                raise ValueError(f"Instruction not supported: {instruction}")

    def _read_int32(self) -> int:
        return self._read_int(4)

    def _read_int(self, size: int) -> int:
        data = self.program[self.ip: self.ip + size]
        self.ip += size
        return int.from_bytes(bytes(data))
```

And if you run the previous program you will see... the **fibonacci** sequence! How?!

Let's understand how this works by examples. I wrote a small assembler program which allows us to write the instructions not in bytecode, but using their shorthands.

## Example 1

<textarea style="width: 100%; height: 200px; resize: vertical;" id="assembly1"></textarea>
<input id="execute1" type="button" value="Execute">
<div class="article-code-output" id="output1"></div>

## Example 2

I have also introduced a label mechanism in the assembler program so we don't have to pass the actual index of the instruction to `jumpif`. To define a label to a certain point in the program, write down a dot `.` followed by the name of the label, e.g. `.mylabel`. Then use it as `jumpif .mylabel`.

<textarea style="width: 100%; height: 200px; resize: vertical;" id="assembly2"></textarea>
<input id="execute2" type="button" value="Execute">
<div class="article-code-output" id="output2"></div>

## Fibonacci

So you see, all I did earlier was to translate the following logic into bytecode for our VM:

```python
a = 0
b = 1
n = 20

for i in range(n):
    c = a + b
    print(c)
    a = b
    b = c
```

<textarea style="width: 100%; height: 200px; resize: vertical;" id="assembly3"></textarea>
<input id="execute3" type="button" value="Execute">
<div class="article-code-output" id="output3"></div>

# Programming Constructs

## If Condition
## While Loops
## Functions


<script src="/assets/virtual-machine/vm.js"></script>