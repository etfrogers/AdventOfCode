use grid::Grid;
use rstest::{rstest, fixture};
use super::*;

const TEST_1: &str = "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7";

#[fixture]
fn input() -> Vec<String> {
    utils::string_input_lines(TEST_1)
}

#[fixture]
fn game(input: Vec<String>) -> Game {
    Game::from_strs(input).expect("Failed to build game")
}

#[rstest]
fn test_parse_calls(game: Game) {
    assert_eq!(game.calls,
        vec![7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1])
}

#[rstest]
fn test_parse_boards(input: Vec<String>){
    let game = Game::from_strs(input).expect("Failed to build game");
    let boards = game.boards.borrow();

    assert_eq!(boards.len(), 3);
    assert_eq!(boards[0].matched, Grid::full(5, 5, false));
    assert_eq!(boards[2].numbers.get_row(4), &vec![2, 0, 12, 3, 7])
}


#[rstest]
fn test_run_game(mut game: Game){
    let winners = game.play_game();
    let winner = &winners[0];
    let score = winner.board.total_unmarked() * winner.last_call;
    assert_eq!(winner.last_call, 24);
    assert_eq!(winner.board.total_unmarked(), 188);
    assert_eq!(score, 4512);
}

#[rstest]
fn test_run_game_part_2(mut game: Game){
    let winners = game.play_game();
    let winner = winners.last().unwrap();
    let score = winner.board.total_unmarked() * winner.last_call;
    // 148 * 13 = 1924.
    assert_eq!(winner.last_call, 13);
    assert_eq!(winner.board.total_unmarked(), 148);
    assert_eq!(score, 1924);
}


#[test]
fn test_part1() {
    let input = utils::input_lines(4);
    let mut game = Game::from_strs(input).expect("Failed to build game");
    let winners = game.play_game();
    let winner = &winners[0];

    let part_1_answer = winner.board.total_unmarked() * winner.last_call;
    assert_eq!(part_1_answer, 58374);
}


#[test]
fn test_part2() {
    let input = utils::input_lines(4);
    let mut game = Game::from_strs(input).expect("Failed to build game");
    let winners = game.play_game();
    let winner = winners.last().unwrap();

    let part_2_answer = winner.board.total_unmarked() * winner.last_call;
    assert_eq!(part_2_answer, 11377);
}