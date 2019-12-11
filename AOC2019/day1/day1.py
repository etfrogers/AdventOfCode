
def fuel(mass):
    return (mass // 3) - 2


def main():
    with open('input.txt') as f:
        masses = f.readlines()
    masses = [int(m.strip()) for m in masses]
    total_fuel = sum([fuel(mass) for mass in masses])
    print(f'Total fuel: {total_fuel}')


if __name__ == '__main__':
    main()
