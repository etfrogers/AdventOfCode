import day21


def test_enhance():
    with open('test_input.txt', 'r') as file:
        rules = file.readlines()
    rules = [rule.strip() for rule in rules]
    rulebook = day21.RuleBook(rules)
    n_iter = 2
    image = day21.Pattern(day21.start_pattern)
    image.enhance_cycle(n_iter, rulebook)
    assert image.number_of_pixels() == 12


def test_part1():
    with open('input.txt', 'r') as file:
        rules = file.readlines()
    rules = [rule.strip() for rule in rules]
    rulebook = day21.RuleBook(rules)
    n_iter = 5
    image = day21.Pattern(day21.start_pattern)
    image.enhance_cycle(n_iter, rulebook)
    assert image.number_of_pixels() == 133
