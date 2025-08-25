import vm


def _int32(value: int) -> bytes:
    return value.to_bytes(4)


def _assemble(commands: list[str]) -> bytes:
    program = bytearray()
    label_defs = dict()
    label_calls = list()
    pointer = 0

    for command in commands:
        parts = command.split()
        cmd = parts[0].lower()

        if cmd.startswith('.'):
            label_defs[cmd] = pointer
        elif cmd == 'push':
            program.append(vm.Op.PUSH)
            program.extend(_int32(int(parts[1])))
            pointer += 5
        elif cmd == 'store':
            program.append(vm.Op.STORE)
            program.extend(_int32(int(parts[1])))
            pointer += 5
        elif cmd == 'load':
            program.append(vm.Op.LOAD)
            program.extend(_int32(int(parts[1])))
            pointer += 5
        elif cmd == 'add':
            program.append(vm.Op.ADD)
            pointer += 1
        elif cmd == 'sub':
            program.append(vm.Op.SUB)
            pointer += 1
        elif cmd == 'jumpif':
            program.append(vm.Op.JUMPIF)
            if parts[1].startswith('.'):
                label_calls.append((parts[1], pointer + 1))
                program.extend(_int32(0))
            else:
                program.extend(_int32(int(parts[1])))
            pointer += 5
        elif cmd == 'print':
            program.append(vm.Op.PRINT)
            pointer += 1
        elif cmd == 'halt':
            program.append(vm.Op.HALT)
            pointer += 1

    for label, position in label_calls:
        value = _int32(label_defs[label])
        program[position: position + 4] = value

    return bytes(program)


def assemble(assembly: str) -> bytes:
    lines = []
    for line in assembly.strip().splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            idx = line.find('#')
            if idx > 0:
                line = line[:idx].strip()
            lines.append(line)
    return _assemble(lines)
