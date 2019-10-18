from AOC2015.day11.day11 import is_valid, has_forbidden_letters, has_two_double_letters, has_straight, \
    get_next_password, to_num_list, to_string, increment

tests = [[is_valid, [('hijklmmn', False),  # meets the first requirement (because it contains the straight hij) but
                     # fails the second requirement requirement (because it contains i and l).
                    ('abbceffg', False),  # meets the third requirement (because it repeats bb and ff) but fails the
                     # first requirement.
                    ('abbcegjk', False),  # fails the third requirement, because it only has one double letter (bb).
                    ]],
         [has_straight, [('hijklmmn', True),  # meets the first requirement (because it contains the straight hij) but
                         # fails the second requirement requirement (because it contains i and l).
                         ('abbceffg', False),  # meets the third requirement (because it repeats bb and ff) but fails
                         # the first requirement.
                         ('abbcegjk', False),  # fails the third requirement, because it only has one double
                         # letter (bb).
                         ]],
         [has_two_double_letters, [('hijklmmn', False),  # meets the first requirement (because it contains the
                                   # straight hij) but fails the second requirement requirement
                                   # (because it contains i and l).
                                   ('abbceffg', True),  # meets the third requirement (because it repeats bb and ff)
                                   # but fails the first requirement.
                                   ('abbcegjk', False),  # fails the third requirement, because it only has one
                                   # double letter (bb).
                                   ]],
         [has_forbidden_letters, [('hijklmmn', True),  # meets the first requirement (because it contains the straight
                                  # hij) but fails the second requirement requirement (because it contains i and l).
                                  ('abbceffg', False),  # meets the third requirement (because it repeats bb and ff)
                                  # but fails the first requirement.
                                  ('abbcegjk', False),  # fails the third requirement, because it only has one double
                                  # letter (bb).
                                  ]
          ]
         ]

next_password_tests = [('abcdefgh', 'abcdffaa'),
                       ('ghijklmn', 'ghjaabcc'),
                       ]


def check_method(fun, input_, result):
    assert fun(input_) == result


def test_1():
    for fun, cases in tests:
        for case in cases:
            yield check_method, fun, case[0], case[1]


def test_next_password():
    for old, new in next_password_tests:
        assert get_next_password(old) == new


def test_increment_list():
    input_ = [4, 4, 25, 4, 25, 25, 25]
    expected_output = [4, 4, 25, 5, 0, 0, 0]
    output = input_.copy()
    increment(output)
    assert all(i == o for i, o in zip(output, expected_output))


def test_increment_string():
    input_ = 'abuiydsahjkzzzzz'
    expected_output = 'abuiydsahjlaaaaa'
    list_ = to_num_list(input_)
    increment(list_)
    output = to_string(list_)
    assert output == expected_output
