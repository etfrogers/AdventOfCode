import day13


def test_firewall1():
    with open('test_input.txt', 'r') as file:
        firewall_spec = file.readlines()
    firewall_spec = [line.strip() for line in firewall_spec]
    firewall_spec = day13.parse_firewall_spec(firewall_spec)

    firewall = day13.Firewall(firewall_spec)
    firewall.run()
    assert firewall.total_severity == 24


def test_part1():
    with open('input.txt', 'r') as file:
        firewall_spec = file.readlines()
    firewall_spec = [line.strip() for line in firewall_spec]
    firewall_spec = day13.parse_firewall_spec(firewall_spec)

    firewall = day13.Firewall(firewall_spec)
    firewall.run()
    assert firewall.total_severity == 2384


def test_firewall2():
    with open('test_input.txt', 'r') as file:
        firewall_spec = file.readlines()
    firewall_spec = [line.strip() for line in firewall_spec]
    firewall_spec = day13.parse_firewall_spec(firewall_spec)
    firewall = day13.Firewall(firewall_spec)
    delay = firewall.find_delay()
    assert delay == 10
