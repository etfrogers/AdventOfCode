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

    def find_pattern(self, pattern):
        pattern_list = [int(v) for v in pattern]
        pattern_len = len(pattern_list)
        while not all([v1 == v2 for v1, v2 in zip(pattern_list, self.recipes[-pattern_len:])]):
            self.extend_recipes()
            if len(self.recipes) > 100000000:
                break
        return str(self).index(pattern)

    def __str__(self):
        return ''.join([str(v) for v in self.recipes])


def get_digits(num):
    if num < 10:
        return num,
    else:
        return math.floor(num/10), num % 10


if __name__ == '__main__':
    recipes = Recipes()
    print(recipes.ten_after(77201))

    print(recipes.find_pattern('077201'))
