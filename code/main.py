import vm
import assembly

# program = bytes([
#     0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
#     0, 0, 0, 0, 1, 1, 0, 0, 0, 1,
#     0, 0, 0, 0, 0, 1, 0, 0, 0, 2,
#     2, 0, 0, 0, 0, 2, 0, 0, 0, 1,
#     3, 1, 0, 0, 0, 3,
#     2, 0, 0, 0, 3, 6,
#     2, 0, 0, 0, 1, 1, 0, 0, 0, 0,
#     2, 0, 0, 0, 3, 1, 0, 0, 0, 1,
#     2, 0, 0, 0, 2, 0, 0, 0, 0, 1,
#     3, 1, 0, 0, 0, 2,
#     2, 0, 0, 0, 2, 0, 0, 0, 0, 20,
#     4, 5, 0, 0, 0, 30, 7
# ])


program = """
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

# goto .label if i<30
load 2
push 30
lt
jumpif .label
halt
"""

machine = vm.Vm(program=assembly.assemble(program), stack=[], memory=[0] * 16)
machine.run()
