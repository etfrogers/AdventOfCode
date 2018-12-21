import math

INITIAL_RECIPES = (3, 7)


class Recipes:
    def __init__(self):
        self.recipes = list(INITIAL_RECIPES)
        self.elf1 = 0
        self.elf2 = 1

    def __getitem__(self, item):
        while max([item.start, item.stop]) > len(self.recipes):
            self.extend_recipes()
        return self.recipes[item]

    def extend_recipes(self):
        new_score = self.recipes[self.elf1] + self.recipes[self.elf2]
        self.recipes.extend(get_digits(new_score))
        self.elf1 = (self.elf1 + self.recipes[self.elf1] + 1) % len(self.recipes)
        self.elf2 = (self.elf2 + self.recipes[self.elf2] + 1) % len(self.recipes)

    def ten_after(self, index):
        return ''.join([str(v) for v in self[index:index+10]])


def get_digits(num):
    digits = []
    remainder = num
    while ''.join([str(d) for d in digits]) != str(num):
        digits.insert(0, remainder % 10)
        remainder = math.floor(remainder / 10)
    return digits


if __name__ == '__main__':
    recipes = Recipes()
    print(recipes.ten_after(77201))
