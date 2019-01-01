# ip 2


def assembly(r0, log_length=0):
    r1 = r2 =r3 = r4 = r5 = 0
    r3 = 123  # seti 123 0 3          # 0
    while True:
        r3 &= 456  # bani 3 456 3          # 1
        if r3 == 72:  # eqri 3 72 3           # 2
            # addr 3 2 2            # 3
            # goto 1 # seti 0 0 2            # 4
            break
    r3 = 0  # seti 0 0 3            # 5
    lst = []
    while True:
        # print((r0, r1, r2, r3, r4, r5))
        lst.append(r3)
        r4 = r3 | 65536  # bori 3 65536 4        # 6
        r3 = 10649702  # seti 10649702 3 3     # 7
        while True:
            r5 = r4 & 255  # bani 4 255 5          # 8
            r3 += r5  # addr 3 5 3            # 9
            r3 &= 16777215  # bani 3 16777215 3     # 10
            r3 *= 65899  # muli 3 65899 3        # 11
            r3 &= 16777215  # bani 3 16777215 3     # 12
            r5 = 256 > r4  # gtir 256 4 5          # 13
            if not r5:  # addr 5 2 2            # 14
                # addi 2 1 2            # 15
                # goto 28  # seti 27 7 2           # 16
                r5 = 0  # seti 0 6 5            # 17
                while True:
                    r1 = r5 + 1  # addi 5 1 1            # 18
                    r1 *= 256  # muli 1 256 1          # 19
                    r1 = r1 > r4  # gtrr 1 4 1            # 20
                    if not r1:  # addr 1 2 2            # 21
                        # addi 2 1 2            # 22
                        # goto 26  # seti 25 9 2           # 23
                        r5 += 1  # addi 5 1 5            # 24
                    else:
                        break  # goto 18  # seti 17 9 2           # 25
                r4 = r5  # setr 5 7 4            # 26
                # goto 8 # seti 7 1 2            # 27
            else:
                break
        r5 = r3 == r0  # eqrr 3 0 5            # 28
        if r5 or (log_length and len(lst) >= log_length):
            break  # addr 5 2 2            # 29
    # goto 6 seti 5 4 2            # 30
    return lst


# def assembly_refactor(r0, log_length=0):
#     r1 = r2 =r3 = r4 = r5 = 0
#     r3 = 123  # seti 123 0 3          # 0
#     while True:
#         r3 &= 456  # bani 3 456 3          # 1
#         if r3 == 72:  # eqri 3 72 3           # 2
#             # addr 3 2 2            # 3
#             # goto 1 # seti 0 0 2            # 4
#             break
#     r3 = 0  # seti 0 0 3            # 5
#     lst = []
#     while r3 not in lst[:-2]:
#         print((r0, r1, r2, r3, r4, r5))
#         lst.append(r3)
#         r4 = r3 | 65536  # bori 3 65536 4        # 6
#         r3 = 10649702  # seti 10649702 3 3     # 7
#         while True:
#             # r5 = r4 % 256  # bani 4 255 5          # 8
#             r3 += r4 % 256  # addr 3 5 3            # 9
#             r3 &= 16777215  # bani 3 16777215 3     # 10
#             r3 *= 65899  # muli 3 65899 3        # 11
#             r3 &= 16777215  # bani 3 16777215 3     # 12
#             # r5 = 256 > r4  # gtir 256 4 5          # 13
#             if 256 < r4:  # addr 5 2 2            # 14
#                 # addi 2 1 2            # 15
#                 # goto 28  # seti 27 7 2           # 16
#                 # r5 = 0  # seti 0 6 5            # 17
#                 # r5 = int(r4 / 256)
#                 # while True:
#                 #     # r1 = (r5 + 1) * 256  # addi 5 1 1            # 18
#                 #     # r1 *= 256  # muli 1 256 1          # 19
#                 #     # r1 = r1 > r4  # gtrr 1 4 1            # 20
#                 #     if (r5 + 1) * 256 < r4:  # addr 1 2 2            # 21
#                 #         # addi 2 1 2            # 22
#                 #         # goto 26  # seti 25 9 2           # 23
#                 #         r5 += 1  # addi 5 1 5            # 24
#                 #     else:
#                 #         break  # goto 18  # seti 17 9 2           # 25
#                 r4 = int(r4 / 256)+1  # setr 5 7 4            # 26
#                 # goto 8 # seti 7 1 2            # 27
#             else:
#                 break
#         # r5 = r3 == r0  # eqrr 3 0 5            # 28
#         if r3 == r0 or (log_length and len(lst) >= log_length):
#             break  # addr 5 2 2            # 29
#     # goto 6 seti 5 4 2            # 30
#     return lst

def assembly_refactor(r0, log_length=0):
    r3 = 123  # seti 123 0 3          # 0
    done = False
    while not done:
        r3 &= 456  # bani 3 456 3          # 1
        done = r3 == 72  # eqri 3 72 3           # 2
    r3 = 0  # seti 0 0 3            # 5
    lst = []
    r4lst = []
    while r3 not in lst[:-2]:
        # print((r0, r1, r2, r3, r4, r5))
        lst.append(r3)
        r4 = r3 | 65536  # bori 3 65536 4        # 6
        r3 = 10649702  # seti 10649702 3 3     # 7
        while True:
            r5 = r4 % 256  # bani 4 255 5          # 8
            r3 += r5  # addr 3 5 3            # 9
            r3 %= 16777216  # bani 3 16777215 3     # 10
            r3 *= 65899  # muli 3 65899 3        # 11
            r3 %= 16777216  # bani 3 16777215 3     # 12
            if r4 >= 256:  # addr 5 2 2            # 14
                r4 //= 256  # seti 0 6 5            # 17
            else:
                r4lst.append(r4)
                break
        # r5 = r3 == r0  # eqrr 3 0 5            # 28
        if r3 == r0 or (log_length and len(lst) >= log_length):
            break  # addr 5 2 2            # 29
    # goto 6 seti 5 4 2            # 30
    return lst
