use super::*;
use rstest::{fixture, rstest};

const TEST_1: &str = "[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[rstest]
fn test_n_corrupted(input: Vec<String>) {
    assert_eq!(
        input
            .iter()
            .map(|s| process_line(s))
            .filter(|status| match status {
                LineState::Corrupted(_) => true,
                _ => false,
            })
            .collect::<Vec<_>>()
            .len(),
        5
    )
}

#[rstest]
fn test_n_incomplete(input: Vec<String>) {
    assert_eq!(
        input
            .iter()
            .map(|s: &String| process_line(s))
            .filter(|status| match status {
                LineState::Incomplete(_) => true,
                _ => false,
            })
            .collect::<Vec<_>>()
            .len(),
        5
    )
}

#[rstest]
fn test_incomplete_scores(input: Vec<String>) {
    let scores = input
        .iter()
        .map(|s: &String| process_line(s))
        .filter(|status| match status {
            LineState::Incomplete(_) => true,
            _ => false,
        })
        .map(line_score)
        .collect::<Vec<_>>();
    assert_eq!(scores, vec![288957, 5566, 1480781, 995444, 294])
}

#[rstest]
fn test_incomplete_score_total(input: Vec<String>) {
    assert_eq!(completion_score(&input), 288957);
}

#[rstest]
fn test_corruption_score(input: Vec<String>) {
    assert_eq!(corruption_score(&input), 26397);
}

#[test]
fn test_part1() {
    let input = utils::input_lines(10);

    let part_1_answer = corruption_score(&input);
    assert_eq!(part_1_answer, 166191);
}
