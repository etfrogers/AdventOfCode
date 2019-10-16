def look_and_say(string: str):
    output = [1, string[0]]
    counter = 0
    for ii in range(1, len(string)):
        if string[ii] == output[counter + 1]:
            output[counter] = output[counter] + 1
        else:
            output.append(1)
            output.append(string[ii])
            counter = counter + 2
    return ''.join([str(v) for v in output])


def main():
    string = '1321131112'
    for _ in range(40):
        string = look_and_say(string)

    print(f'Part 1: length of iterated string is {len(string)}')


if __name__ == '__main__':
    main()
