const Op = {
    PUSH: 0,
    STORE: 1,
    LOAD: 2,
    ADD: 3,
    LT: 4,
    JUMP: 5,
    JUMPIF: 6,
    JUMPIFNOT: 7,
    PRINT: 8,
    HALT: 9,
};

class Vm {
    constructor(program, memorySize = 256) {
        this.program = new Uint8Array(program);
        this.stack = [];
        this.memory = new Array(memorySize).fill(0);
        this.ip = 0;
        this.stdout = [];
    }

    push(value) {
        this.stack.push(value);
    }

    store(index) {
        this.memory[index] = this.stack.pop();
    }

    load(index) {
        this.stack.push(this.memory[index]);
    }

    add() {
        const a = this.stack.pop();
        const b = this.stack.pop();
        this.stack.push(a + b);
    }

    lt() {
        const a = this.stack.pop();
        const b = this.stack.pop();
        this.stack.push(b < a ? 1 : 0);
    }

    jump(pointer) {
        this.ip = pointer;
    }

    jumpif(pointer) {
        if (this.stack.pop() > 0) {
            this.ip = pointer;
        }
    }

    jumpifnot(pointer) {
        if (this.stack.pop() === 0) {
            this.ip = pointer;
        }
    }

    print() {
        this.stdout.push(this.stack.pop());
    }

    run() {
        while (this.ip < this.program.length) {
            const instruction = this.program[this.ip];
            this.ip++;

            switch (instruction) {
                case Op.PUSH:
                    this.push(this._readInt32());
                    break;
                case Op.STORE:
                    this.store(this._readInt32());
                    break;
                case Op.LOAD:
                    this.load(this._readInt32());
                    break;
                case Op.ADD:
                    this.add();
                    break;
                case Op.LT:
                    this.lt();
                    break;
                case Op.JUMP:
                    this.jump(this._readInt32());
                    break;
                case Op.JUMPIF:
                    this.jumpif(this._readInt32());
                    break;
                case Op.JUMPIFNOT:
                    this.jumpifnot(this._readInt32());
                    break;
                case Op.PRINT:
                    this.print();
                    break;
                case Op.HALT:
                    return;
            }
        }
    }

    _readInt32() {
        return this._readInt(4);
    }

    _readInt(size) {
        const view = new DataView(this.program.buffer, this.ip, size);
        this.ip += size;
        return view.getInt32(0, false);
    }
}

class Assembler {
    _int32(value) {
        const buffer = new ArrayBuffer(4);
        const view = new DataView(buffer);
        view.setInt32(0, value, false);
        return new Uint8Array(buffer);
    }

    _assemble(commands) {
        let program = [];
        const labelDefs = {};
        const labelCalls = [];
        let pointer = 0;

        for (const command of commands) {
            const parts = command.split(/\s+/);
            const cmd = parts[0].toLowerCase();

            if (cmd.startsWith('.')) {
                labelDefs[cmd] = pointer;
            } else if (cmd === 'push') {
                program.push(Op.PUSH);
                program.push(...this._int32(parseInt(parts[1])));
                pointer += 5;
            } else if (cmd === 'store') {
                program.push(Op.STORE);
                program.push(...this._int32(parseInt(parts[1])));
                pointer += 5;
            } else if (cmd === 'load') {
                program.push(Op.LOAD);
                program.push(...this._int32(parseInt(parts[1])));
                pointer += 5;
            } else if (cmd === 'add') {
                program.push(Op.ADD);
                pointer += 1;
            } else if (cmd === 'lt') {
                program.push(Op.LT);
                pointer += 1;
            } else if (cmd === 'jump') {
                program.push(Op.JUMP);
                if (parts[1].startsWith('.')) {
                    labelCalls.push([parts[1], pointer + 1]);
                    program.push(...this._int32(0));
                } else {
                    program.push(...this._int32(parseInt(parts[1])));
                }
                pointer += 5;
            } else if (cmd === 'jumpif') {
                program.push(Op.JUMPIF);
                if (parts[1].startsWith('.')) {
                    labelCalls.push([parts[1], pointer + 1]);
                    program.push(...this._int32(0));
                } else {
                    program.push(...this._int32(parseInt(parts[1])));
                }
                pointer += 5;
            } else if (cmd === 'jumpifnot') {
                program.push(Op.JUMPIFNOT);
                if (parts[1].startsWith('.')) {
                    labelCalls.push([parts[1], pointer + 1]);
                    program.push(...this._int32(0));
                } else {
                    program.push(...this._int32(parseInt(parts[1])));
                }
                pointer += 5;
            } else if (cmd === 'print') {
                program.push(Op.PRINT);
                pointer += 1;
            } else if (cmd === 'halt') {
                program.push(Op.HALT);
                pointer += 1;
            }
        }

        program = new Uint8Array(program);

        for (const [label, position] of labelCalls) {
            const value = this._int32(labelDefs[label]);
            program.set(value, position);
        }

        return program;
    }

    assemble(assembly) {
        const lines = [];
        const assemblyLines = assembly.trim().split('\n');
        for (let line of assemblyLines) {
            line = line.trim();
            if (line && !line.startsWith('#')) {
                const idx = line.indexOf('#');
                if (idx > 0) {
                    line = line.substring(0, idx).trim();
                }
                lines.push(line);
            }
        }
        return this._assemble(lines);
    }
}


const assembleButton = document.getElementById("assemble");
const assembly = document.getElementById("assembly");
const output = document.getElementById("output")

assembleButton.onclick = () => {
    let assembler = new Assembler()
    let bytes = assembler.assemble(assembly.value)
    let vm = new Vm(bytes);
    vm.run();
    output.innerText = vm.stdout.join('\n')
};