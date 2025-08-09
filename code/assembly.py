import vm


def _int32(value: int) -> bytes:
    return value.to_bytes(4)


def _assemble(commands: list[str]) -> bytes:
    program = bytearray()
    labels = dict()
    pointer = 0

    for command in commands:
        parts = command.split()
        cmd = parts[0].lower()
        if cmd.startswith('.'):
            labels[cmd] = pointer
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
        elif cmd == 'lt':
            program.append(vm.Op.LT)
            pointer += 1
        elif cmd == 'jumpif':
            program.append(vm.Op.JUMPIF)
            if parts[1].startswith('.'):
                program.extend(_int32(labels[parts[1]]))
            else:
                program.extend(_int32(int(parts[1])))
            pointer += 5
        elif cmd == 'print':
            program.append(vm.Op.PRINT)
            pointer += 1
        elif cmd == 'halt':
            program.append(vm.Op.HALT)
            pointer += 1

    return program


def assemble(assembly: str) -> bytes:
    lines = [
        line.strip()
        for line in assembly.strip().splitlines()
        if line.strip() and not line.strip().startswith('#')
    ]
    return _assemble(lines)
