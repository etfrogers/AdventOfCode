import re

from AOC2015.day5.day5 import is_nice, has_three_vowels, has_double_letter, has_forbidden_strings

test_cases = [('ugknbfddgicrmopn', True),  # is nice because it has at least three vowels (u...i...o...), a double
              # letter (...dd...), and none of the disallowed substrings.
              ('aaa', True),  # is nice because it has at least three vowels and a double letter, even though the
              # letters used by different rules overlap.
              ('jchzalrnumimnmhp', False),  # is naughty because it has no double letter.
              ('haegwjzuvuyypxyu', False),  # is naughty because it contains the string xy.
              ('dvszwmarrgswjxmb', False),  # is naughty because it contains only one vowel.
              ('xyyaei', False),  # is naughty because it contains only one vowel.
             ]


# code from reddit
# count = sum(1 for s in strings
#                 if len([x for x in s if x in "aeiou"]) > 2
#                 and not any(x in s for x in ["ab", "cd", "pq", "xy"])
#                 and re.search(r"([a-z])\1", s)
#                 )
#     print(count)

def check_is_nice(case):
    assert is_nice(case[0]) == case[1]


def test_1():
    for case in test_cases:
        yield check_is_nice, case


def test_three_vowels():
    for s in ['aei', 'xazegov', 'aeiouaeiouaeiou']:
        assert has_three_vowels(s)


def test_double_letter():
    for s in ['xx', 'abcdde', 'aabbccdd']:
        assert has_double_letter(s)


def check_reddit_tv(s):
    assert (len([x for x in s if x in "aeiou"]) > 2) == has_three_vowels(s)


def check_reddit_fs(s):
    assert any(x in s for x in ["ab", "cd", "pq", "xy"]) == has_forbidden_strings(s)


def check_reddit_dl(s):
    assert (re.search(r"([a-z])\1", s) is not None) == has_double_letter(s)


def test_against_reddit():
    with open('input.txt') as f:
        strings = f.readlines()

    for s in strings:
        yield check_reddit_tv, s
        yield check_reddit_fs, s
        yield check_reddit_dl, s
