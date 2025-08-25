const Op = {
    PUSH: 0,
    STORE: 1,
    LOAD: 2,
    ADD: 3,
    SUB: 4,
    JUMPIF: 5,
    PRINT: 6,
    HALT: 7,
    JUMP: 8,
    JUMPIFNOT: 9,
    CALL: 10,
    RETURN: 11,
    MOD: 12,
    MUL: 13,
    EQ: 14,
    NEQ: 15
};

class Vm {
    constructor(program, memorySize = 256) {
        this.program = new Uint8Array(program);
        this.stack = [];
        this.callstack = [];
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

    sub() {
        const a = this.stack.pop();
        const b = this.stack.pop();
        this.stack.push(b - a);
    }

    mod() {
        const a = this.stack.pop();
        const b = this.stack.pop();
        this.stack.push(b % a);
    }

    mul() {
        const a = this.stack.pop();
        const b = this.stack.pop();
        this.stack.push(a * b);
    }

    eq() {
        const a = this.stack.pop();
        const b = this.stack.pop();
        this.stack.push(a === b ? 1 : 0);
    }

    neq() {
        const a = this.stack.pop();
        const b = this.stack.pop();
        this.stack.push(a !== b ? 1 : 0);
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
        if (this.stack.pop() <= 0) {
            this.ip = pointer;
        }
    }

    call(pointer) {
        this.callstack.push(this.ip);
        this.ip = pointer;
    }

    returns() {
        this.ip = this.callstack.pop()
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
                case Op.SUB:
                    this.sub();
                    break;
                case Op.MOD:
                    this.mod();
                    break;
                case Op.MUL:
                    this.mul();
                    break;
                case Op.EQ:
                    this.eq();
                    break;
                case Op.NEQ:
                    this.neq();
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
                case Op.CALL:
                    this.call(this._readInt32());
                    break;
                case Op.RETURN:
                    this.returns();
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
            } else if (cmd === 'sub') {
                program.push(Op.SUB);
                pointer += 1;
            } else if (cmd === 'mod') {
                program.push(Op.MOD);
                pointer += 1;
            } else if (cmd === 'mul') {
                program.push(Op.MUL);
                pointer += 1;
            } else if (cmd === 'eq') {
                program.push(Op.EQ);
                pointer += 1;
            } else if (cmd === 'neq') {
                program.push(Op.NEQ);
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
            } else if (cmd === 'call') {
                program.push(Op.CALL);
                if (parts[1].startsWith('.')) {
                    labelCalls.push([parts[1], pointer + 1]);
                    program.push(...this._int32(0));
                } else {
                    program.push(...this._int32(parseInt(parts[1])));
                }
                pointer += 5;
            } else if (cmd === 'return') {
                program.push(Op.RETURN);
                pointer += 1;
            } else if (cmd === 'print') {
                program.push(Op.PRINT);
                pointer += 1;
            } else if (cmd === 'halt') {
                program.push(Op.HALT);
                pointer += 1;
            } else {
                console.error("Instruction not recognized: ", cmd)
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

const hook = (execute, assemble, code, output) => {
    execute.onclick = () => {
        let assembler = new Assembler()
        let bytes = assembler.assemble(code.value)
        let vm = new Vm(bytes);
        vm.run();
        output.innerText = vm.stdout.join('\n')
    };
    assemble.onclick = () => {
        let assembler = new Assembler()
        let bytes = assembler.assemble(code.value)
        output.innerText = `[${bytes.join(', ')}]`
    };
}

const execute1 = document.getElementById("execute1");
const assemble1 = document.getElementById("assemble1");
const assembly1 = document.getElementById("assembly1");
const output1 = document.getElementById("output1");
hook(execute1, assemble1, assembly1, output1);
assembly1.value = `
push 4   # stack=[4]
push 5   # stack=[4, 5]
add      # stack=[9]
print    # stack=[]
`.trim()

const execute2 = document.getElementById("execute2");
const assemble2 = document.getElementById("assemble2");
const assembly2 = document.getElementById("assembly2");
const output2 = document.getElementById("output2");
hook(execute2, assemble2, assembly2, output2);
assembly2.value = `
push 1          # stack=[1]     memory[0]=0
store 0         # stack=[]      memory[0]=1
.label

load 0          # stack=[1]     memory[0]=1
print           # stack=[]      memory[0]=1

load 0          # stack=[1]     memory[0]=1
push 1          # stack=[1,1]   memory[0]=1
add             # stack=[2]     memory[0]=1
store 0         # stack=[]      memory[0]=2

push 10         # stack=[10]    memory[0]=2
load 0          # stack=[10,2]  memory[0]=2
sub             # stack=[8]     memory[0]=2
jumpif .label   # stack=[]      memory[0]=2,    goes to .label if 8>2. will stop at 9.
`.trim()


const execute3 = document.getElementById("execute3");
const assemble3 = document.getElementById("assemble3");
const assembly3 = document.getElementById("assembly3");
const output3 = document.getElementById("output3");
hook(execute3, assemble3, assembly3, output3);
assembly3.value = `
# a = 0
push 0
store 0

# b = 1
push 1
store 1

# i = 0
push 0
store 2

# c = a + b
.label
load 0
load 1
add
store 3

# print(c)
load 3
print

# a = b
load 1
store 0

# b = c
load 3
store 1

# i++
load 2
push 1
add
store 2

# goto .label if i<20
push 20
load 2
sub
jumpif .label
`.trim()


const execute4 = document.getElementById("execute4");
const assemble4 = document.getElementById("assemble4");
const assembly4 = document.getElementById("assembly4");
const output4 = document.getElementById("output4");
hook(execute4, assemble4, assembly4, output4);
assembly4.value = `
push 1
call .fun
print

push 2
call .fun
print

push 3
call .fun
print

halt

.fun
push 10
add
return
`.trim()


const execute5 = document.getElementById("execute5");
const assemble5 = document.getElementById("assemble5");
const assembly5 = document.getElementById("assembly5");
const output5 = document.getElementById("output5");
hook(execute5, assemble5, assembly5, output5);
assembly5.value = `
# print 2
push 2
print

# i = 2
push 3
store 2

.main

# if isPrime(i): print i
load 2
call .isprime
jumpifnot .notaprime

load 2
print

# i += 2
.notaprime
load 2
push 2
add
store 2

# loop if i < 100
push 100
load 2
sub
jumpif .main

halt

# isPrime() function
.isprime

# n = stack[-1]
store 0

# j = 2
push 2
store 1

.loop

# if n%j == 0
load 0
load 1
mod
push 0
eq
jumpifnot .continue

# return false
push 0
return

# j += 1
.continue
push 1
load 1
add
store 1

# if n == j, return true
load 0
load 1
eq

jumpifnot .loop

push 1
return
`.trim()