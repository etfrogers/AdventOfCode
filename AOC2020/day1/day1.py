

def search_report_2(report):
    numbers = parse_report(report)
    for i in range(len(numbers)):
        for j in range(i+1, len(numbers)):
            answer = numbers[i] + numbers[j]
            if answer == 2020:
                return numbers[i], numbers[j]


def search_report_3(report):
    numbers = parse_report(report)
    for i in range(len(numbers)):
        for j in range(i+1, len(numbers)):
            for k in range(j+1, len(numbers)):
                answer = numbers[i] + numbers[j] + numbers[k]
                if answer == 2020:
                    return numbers[i], numbers[j], numbers[k]


def parse_report(report):
    numbers = report.split('\n')
    numbers = [int(n) for n in numbers]
    return numbers


def main():
    with open('input.txt') as file:
        report = file.read()
    answers = search_report_2(report)
    print(answers)
    print(f'Day 1, Part 1: {answers[0] * answers[1]}')

    answers = search_report_3(report)
    print(answers)
    print(f'Day 1, Part 1: {answers[0] * answers[1] * answers[2]}')


if __name__ == '__main__':
    main()
