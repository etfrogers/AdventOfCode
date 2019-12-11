
def fuel(mass):
    return (mass // 3) - 2


def recursive_fuel(mass):
    fuel_ = fuel(mass)
    if fuel_ <= 0:
        return 0
    else:
        return fuel_ + recursive_fuel(fuel_)


def main():
    with open('input.txt') as f:
        masses = f.readlines()
    masses = [int(m.strip()) for m in masses]
    total_fuel = sum([fuel(mass) for mass in masses])
    print(f'Total fuel: {total_fuel}')

    total_fuel_recursive = sum([recursive_fuel(mass) for mass in masses])
    print(f'Fuel including fuel for fuel: {total_fuel_recursive}')


if __name__ == '__main__':
    main()
