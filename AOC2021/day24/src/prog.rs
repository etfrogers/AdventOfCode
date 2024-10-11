use std::collections::VecDeque;

pub fn program(mut input: VecDeque<i128>) -> bool {
    let (mut w, mut x, mut y, mut z) = (0, 0, 0, 0);

    w = input.pop_front().unwrap();
    // x = z % 26;
    // z /= 1;
    x = 11;
    // w never = 11 so x == 1
    // x = if x == w { 0 } else { 1 };
    x = 1;
    z *= (25 * x) + 1;
    z += (w + 16) * x;

    w = input.pop_front().unwrap();
    x = z % 26;
    z /= 1;
    x += 12;
    x = if x == w { 0 } else { 1 };
    z *= (25 * x) + 1;
    z += (w + 11) * x;

    w = input.pop_front().unwrap();
    x = z % 26;
    z /= 1;
    x += 13;
    x = if x == w { 0 } else { 1 };
    z *= (25 * x) + 1;
    z += (w + 12) * x;

    w = input.pop_front().unwrap();
    x = z % 26;
    z /= 26;
    x += -5;
    x = if x == w { 0 } else { 1 };
    z *= (25 * x) + 1;
    z += (w + 12) * x;

    w = input.pop_front().unwrap();
    x = z % 26;
    z /= 26;
    x += -3;
    x = if x == w { 0 } else { 1 };
    z *= (25 * x) + 1;
    z += (w + 12) * x;

    w = input.pop_front().unwrap();
    x = z % 26;
    z /= 1;
    x += 14;
    x = if x == w { 0 } else { 1 };
    z *= (25 * x) + 1;
    z += (w + 2) * x;

    w = input.pop_front().unwrap();
    x = z % 26;
    z /= 1;
    x += 15;
    x = if x == w { 0 } else { 1 };
    z *= (25 * x) + 1;
    z += (w + 11) * x;

    w = input.pop_front().unwrap();
    x = z % 26;
    z /= 26;
    x += -16;
    x = if x == w { 0 } else { 1 };
    z *= (25 * x) + 1;
    z += (w + 4) * x;

    w = input.pop_front().unwrap();
    x = z % 26;
    z /= 1;
    x += 14;
    x = if x == w { 0 } else { 1 };
    z *= (25 * x) + 1;
    z += (w + 12) * x;

    w = input.pop_front().unwrap();
    x = z % 26;
    z /= 1;
    x += 15;
    x = if x == w { 0 } else { 1 };
    z *= (25 * x) + 1;
    z += (w + 9) * x;

    w = input.pop_front().unwrap();
    x = z % 26;
    z /= 26;
    x += -7;
    x = if x == w { 0 } else { 1 };
    z *= (25 * x) + 1;
    z += (w + 10) * x;

    w = input.pop_front().unwrap();
    x = z % 26;
    z /= 26;
    x += -11;
    x = if x == w { 0 } else { 1 };
    z *= (25 * x) + 1;
    z += (w + 11) * x;

    w = input.pop_front().unwrap();
    x = z % 26;
    z /= 26;
    x += -6;
    x = if x == w { 0 } else { 1 };
    z *= (25 * x) + 1;
    z += (w + 6) * x;

    w = input.pop_front().unwrap();
    x = z % 26;
    z /= 26;
    x += -11;
    x = if x == w { 0 } else { 1 };
    z *= (25 * x) + 1;
    z += (w + 15) * x;

    z == 0
}
