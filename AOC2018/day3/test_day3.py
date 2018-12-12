import day3


def test1():
    input = ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']
    claims = [day3.Claim(c) for c in input]
    claim_map = day3.build_map(claims)
    conflicts = day3.count_conflicts(claim_map)
    assert conflicts == 4


def test2():
    input = ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']
    claims = [day3.Claim(c) for c in input]
    claim_map = day3.build_map(claims)
    uncontested = day3.find_uncontested_claim(claims, claim_map)
    assert uncontested.id == 3
