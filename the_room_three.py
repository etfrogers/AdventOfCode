from copy import deepcopy

OPS = {'+': int.__add__,
       '*': int.__mul__,
       '-': int.__sub__,
       }


def get_routes(options):
    routes = [[]]
    for i, entry in enumerate(options):
        routes += deepcopy(routes)
        n = 2**i
        for j in range(n):
            routes[j].append(entry[0])
        for j in range(n, 2*n):
            routes[j].append(entry[1])
    assert len(routes[0]) == len(options)
    assert len(routes) == 2 ** len(options)
    return routes


def apply_entry(entry, input_):
    operator = OPS[entry[0]]
    value = int(entry[1:])
    return operator(input_, value)


def evaluate(route):
    val = 0
    for entry in route:
        val = apply_entry(entry, val)
    return val


def find_route(target, options):
    routes = get_routes(options)
    results = [evaluate(route) for route in routes]
    index = results.index(target)
    return routes[index]


def main():
    target_3 = 30
    options_3 = [['+02', '+08'],
                 ['*02', '*05'],
                 ['+04', '+07'],
                 ['+03', '+12'],
                 ['-05', '-17'],
                 ['+02', '+09'],
                 ]

    target_1 = 17
    options_1 = [['+11', '+08'],
                 ['+04', '+03'],
                 ['+01', '+05'],
                 ]

    target_2 = 31
    options_2 = [['+07', '+08'],
                 ['*03', '*04'],
                 ['+03', '+08'],
                 ]

    route = find_route(target_1, options_1)
    print(f'{target_1}: {route}')
    route = find_route(target_2, options_2)
    print(f'{target_2}: {route}')
    route = find_route(target_3, options_3)
    print(f'{target_3}: {route}')


if __name__ == '__main__':
    main()
