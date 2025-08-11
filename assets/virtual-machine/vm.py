import dataclasses


class Op:
    PUSH = 0
    STORE = 1
    LOAD = 2
    ADD = 3
    LT = 4
    JUMP = 5
    JUMPIF = 6
    JUMPIFNOT = 7
    PRINT = 8
    HALT = 9


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

    def lt(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(int(b < a))

    def jump(self, pointer: int):
        self.ip = pointer

    def jumpif(self, pointer: int):
        if self.stack.pop() > 0:
            self.ip = pointer

    def jumpifnot(self, pointer: int):
        if self.stack.pop() == 0:
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
            elif instruction == Op.LT:
                self.lt()
            elif instruction == Op.JUMP:
                self.jump(self._read_int32())
            elif instruction == Op.JUMPIF:
                self.jumpif(self._read_int32())
            elif instruction == Op.JUMPIFNOT:
                self.jumpifnot(self._read_int32())
            elif instruction == Op.PRINT:
                self.print()
            elif instruction == Op.HALT:
                break

    def _read_int32(self) -> int:
        return self._read_int(4)

    def _read_int(self, size: int) -> int:
        data = self.program[self.ip: self.ip + size]
        self.ip += size
        return int.from_bytes(bytes(data))
