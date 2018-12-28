registers = [0] + [0] * 5

registers[2] += 2  # addi 2 2 2  # 17
registers[2] *= registers[2]  # mulr 2 2 2  # 18
registers[2] = registers[2] * 19  # mulr 3 2 2  # 19
registers[2] *= 11 # muli 2 11 2 # 20
registers[5] = registers[5] + 4  # addi 5 4 5  # 21
registers[5] = registers[5] * 22  # mulr 5 3 5  # 22
registers[5] += 16  # addi 5 16 5 # 23
registers[2] += registers[5]  # addr 2 5 2  # 24
if not registers[0]:  ### goto 26+register[0]  # addr 3 0 3  # 25
    ### goto 1  # seti 0 8 3  # 26
    registers[5] = 27  # setr 3 2 5  # 27
    registers[5] *= 28  # mulr 5 3 5  # 28
    registers[5] += 29  # addr 3 5 5  # 29
    registers[5] *= 30  # mulr 3 5 5  # 30
    registers[5] *= 14  # muli 5 14 5 # 31
    registers[5] *= 32  # mulr 5 3 5  # 32
    registers[2] = registers[2] * registers[5]  # addr 2 5 2  # 33
    registers[0] = 0  # seti 0 0 0  # 34
### goto 1 seti 0 0 3  # 35
### goto 17 addi 3 16 3 # 0

registers[4] = 1  # seti 1 0 4  # 1
while True:
    print(registers)
    registers[1] = 1  # seti 1 0 1  # 2
    registers[5] = registers[4] * registers[1]  # mulr 4 1 5  # 3
    registers[5] = registers[5] == registers[2]  # eqrr 5 2 5  # 4
    if registers[5]:  # addr 5 3 3  # 5
        # addi 3 1 3  # 6
        registers[0] += registers[4]  # addr 4 0 0  # 7
    registers[1] += 1  # addi 1 1 1  # 8
    registers[5] = registers[1] > registers[2]  # gtrr 1 2 5  # 9
    if not registers[5]:#addr 3 5 3  # 10
        continue
        ### goto 2 seti 2 9 3  # 11
    registers[4] +=1  # addi 4 1 4  # 12
    registers[5] = registers[4] > registers[2]  # gtrr 4 2 5  # 13

    if registers[5]: # addr 5 3 3  # 14
        ### goto 2 seti 1 2 3  # 15
        break
### halt # mulr 3 3 3  # 16
# registers[2] += 2  # addi 2 2 2  # 17
# registers[2] *= registers[2]  # mulr 2 2 2  # 18
# registers[2] = registers[2] * 19  # mulr 3 2 2  # 19
# registers[2] *= 11 # muli 2 11 2 # 20
# registers[5] = registers[5] + 4  # addi 5 4 5  # 21
# registers[5] = registers[5] * 22  # mulr 5 3 5  # 22
# registers[5] += 16  # addi 5 16 5 # 23
# registers[2] += registers[5]  # addr 2 5 2  # 24
# ### goto 26+register[0]  # addr 3 0 3  # 25
# ### goto 1  # seti 0 8 3  # 26
# registers[5] = 27  # setr 3 2 5  # 27
# registers[5] *= 28  # mulr 5 3 5  # 28
# registers[5] += 29  # addr 3 5 5  # 29
# registers[5] *= 30  # mulr 3 5 5  # 30
# registers[5] *= 14  # muli 5 14 5 # 31
# registers[5] *= 32  # mulr 5 3 5  # 32
# registers[2] = registers[2] * registers[5]  # addr 2 5 2  # 33
# registers[0] = 0  # seti 0 0 0  # 34
# ### goto 1 seti 0 0 3  # 35

print(registers)