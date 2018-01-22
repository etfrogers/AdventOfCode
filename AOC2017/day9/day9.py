

def process_stream(stream):
    depth = 0
    scores = []
    ignoring = False
    in_garbage = False
    garbage_count = 0

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
            garbage_count += 1
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

    return len(scores), sum(scores), garbage_count


def main():
    with open('input.txt', 'r') as file:
        stream = file.read()
    stream = stream.strip()
    # stream = '<random characters>'
    results = process_stream(stream)
    print('%d groups found. Total score was %d. Garbage count was %d' % results)


if __name__ == '__main__':
    main()
