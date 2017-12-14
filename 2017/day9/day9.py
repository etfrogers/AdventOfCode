

def process_stream(stream):
    depth = 0
    scores = []
    ignoring = False
    in_garbage = False

    for char in stream:
        if ignoring:
            ignoring = False
            continue
        if char == '!':
            ignoring = True
            continue
        if in_garbage:
            if char == '>':
                in_garbage = False
            continue
        if char == '{':
            depth += 1
            continue
        if char == '<':
            in_garbage = True
            continue
        if char == '}':
            scores.append(depth)
            depth -= 1

    return len(scores), sum(scores)


def main():
    with open('input.txt', 'r') as file:
        stream = file.read()
    stream = stream.strip()
    # stream = '{{<!>},{<!>},{<!>},{<a>}}'
    n_groups, total_score = process_stream(stream)
    print('%d groups found. Total score was %d' % (n_groups, total_score))


if __name__ == '__main__':
    main()
