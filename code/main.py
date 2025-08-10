import vm
import assembly

fibonacci = """
# a = 0
push 0
store 0

# b = 0
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
load 2
push 20
lt
jumpif .label
halt
"""

loop = """
push 0
store 0

.label

load 0
push 10
lt
jumpifnot .end

load 0
push 1
add
store 0

load 0
print

jump .label

.end
halt
"""

machine = vm.Vm(
    program=assembly.assemble(loop),
    stack=[0] * 16,
    memory=[0] * 16
)
machine.run()
