:title: Virtual Machine
:description: What is a virtual machine and how to create one?
:year: 2025
:month: 8
:day: 8

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

```
# a = 0
push 0
store 0

# b = 0
push 1
store 1

# i = 0
push 0
store 2

.label
# c = a + b
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
```

Instructions: `push`, `store`, `load`, `add`, `lt`, `jumpif`, `print`
