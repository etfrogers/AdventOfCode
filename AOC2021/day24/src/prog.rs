use std::collections::VecDeque;

pub fn program(mut input: VecDeque<i128>) -> bool {
    let i = input.clone();
    // let (mut w, mut x, mut y, mut z) = (0, 0, 0, 0);

    let mut stack = Vec::with_capacity(input.len());
    // w = input.pop_front().unwrap();
    // x = z % 26;
    // z /= 1;
    // x = 11;
    // w never = 11 so x == 1
    // x = if x == w { 0 } else { 1 };
    // x = 1;
    // z *= 26; // but z == 0 so
    // z = 0;
    //then += becomes =
    // z = (w + 16) * x;
    // but x = 1 so
    // z = i[0] + 16;
    stack.push(i[0] + 16);

    // w = input.pop_front().unwrap();
    // x = (z % 26) + 12;
    // x = if x == w { 0 } else { 1 };
    // x >= 12 => x!=w ...
    // x = 1;
    // z = (i[0] + 16) * 26;
    // z = (i[0] * 26 + 16 * 26) + i[1] + 11;
    stack.push(i[1] + 11);

    // w = input.pop_front().unwrap();
    // x = (z % 26) + 13;
    // x = if x == w { 0 } else { 1 };
    // x = 1;
    // z *= (25 * x) + 1
    // z *= 26;
    // z += i[2] + 12;
    stack.push(i[2] + 12);

    // w = input.pop_front().unwrap();
    // // x = z % 26;  ((a*26) + b) % 26 == b =>
    // // x = i[2] + 12 - 5;
    // // x = i[2] + 7;
    // z /= 26;
    // // x += -5;
    // x = if i[2] + 7 == i[3] { 0 } else { 1 };
    // z *= (25 * x) + 1;
    // z += (w + 12) * x;

    if stack.pop().unwrap() - 5 != i[3] {
        stack.push(i[3] + 12)
    }

    // w = input.pop_front().unwrap();
    // x = z % 26;
    // z /= 26;
    // x += -3;
    // x = if x == w { 0 } else { 1 };
    // z *= (25 * x) + 1;
    // z += (w + 12) * x;
    if stack.pop().unwrap() - 3 != i[4] {
        stack.push(i[4] + 12);
    }

    // w = input.pop_front().unwrap();
    // // x = (z % 26) + 14;
    // // x = if x == w { 0 } else { 1 };
    // z *= 26;
    // z += w + 2;
    stack.push(i[5] + 2);

    // w = input.pop_front().unwrap();
    // // x = (z % 26) + 15;
    // // x = if x == w { 0 } else { 1 };
    // z *= 26;
    // z += w + 11;
    stack.push(i[6] + 11);

    // w = input.pop_front().unwrap();
    // x = z % 26;
    // z /= 26;
    // x += -16;
    // x = if x == w { 0 } else { 1 };
    // z *= (25 * x) + 1;
    // z += (w + 4) * x;
    if stack.pop().unwrap() - 16 != i[7] {
        stack.push(i[7] + 4);
    }

    // w = input.pop_front().unwrap();
    // // x = (z % 26) + 14;
    // // x = if x == w { 0 } else { 1 };
    // z *= 26;
    // z += w + 12;
    stack.push(i[8] + 12);

    // w = input.pop_front().unwrap();
    // // x = (z % 26) + 15;
    // // x = if x == w { 0 } else { 1 };
    // z *= 26;
    // z += w + 9;
    stack.push(i[9] + 9);

    // w = input.pop_front().unwrap();
    // x = z % 26;
    // z /= 26;
    // x += -7;
    // x = if x == w { 0 } else { 1 };
    // z *= (25 * x) + 1;
    // z += (w + 10) * x;
    if stack.pop().unwrap() - 7 != i[10] {
        stack.push(i[10] + 10);
    }

    // w = input.pop_front().unwrap();
    // x = z % 26;
    // z /= 26;
    // x += -11;
    // x = if x == w { 0 } else { 1 };
    // z *= (25 * x) + 1;
    // z += (w + 11) * x;
    if stack.pop().unwrap() - 11 != i[11] {
        stack.push(i[11] + 11);
    }

    // w = input.pop_front().unwrap();
    // x = z % 26;
    // z /= 26;
    // x += -6;
    // x = if x == w { 0 } else { 1 };
    // z *= (25 * x) + 1;
    // z += (w + 6) * x;
    if stack.pop().unwrap() - 6 != i[12] {
        stack.push(i[12] + 6);
    }

    // w = input.pop_front().unwrap();
    // x = z % 26;
    // z /= 26;
    // x += -11;
    // x = if x == w { 0 } else { 1 };
    // z *= (25 * x) + 1;
    // z += (w + 15) * x;
    if stack.pop().unwrap() - 11 != i[13] {
        stack.push(i[13]);
    }

    // z == 0
    stack.is_empty()
}

pub fn program2(mut input: VecDeque<i128>) -> bool {
    let i = input.clone();

    let mut stack = Vec::with_capacity(input.len());
    stack.push(i[0] + 16);
    stack.push(i[1] + 11);
    stack.push(i[2] + 12);
    if stack.pop().unwrap() - 5 != i[3] {
        stack.push(i[3] + 12)
    }
    if stack.pop().unwrap() - 3 != i[4] {
        stack.push(i[4] + 12);
    }
    stack.push(i[5] + 2);
    stack.push(i[6] + 11);
    if stack.pop().unwrap() - 16 != i[7] {
        stack.push(i[7] + 4);
    }
    stack.push(i[8] + 12);
    stack.push(i[9] + 9);
    if stack.pop().unwrap() - 7 != i[10] {
        stack.push(i[10] + 10);
    }
    if stack.pop().unwrap() - 11 != i[11] {
        stack.push(i[11] + 11);
    }
    if stack.pop().unwrap() - 6 != i[12] {
        stack.push(i[12] + 6);
    }
    if stack.pop().unwrap() - 11 != i[13] {
        stack.push(i[13]);
    }
    stack.is_empty()
}

pub fn program3(i: &Vec<i128>) -> bool {
    // (i[2] + 12 - 5 == i[3])
    // && (i[1] + 11 - 3 == i[4])
    // && (i[6] + 11 - 16 == i[7])
    // && (i[9] + 9 - 7 == i[10])
    // && (i[8] + 12 - 11 == i[11])
    // && (i[5] + 2 - 6 == i[12])
    // && (i[0] + 16 - 11 == i[13])
    (i[2] + 7 == i[3])         // 2, 9 - 1, 8
        && (i[1] + 8 == i[4])  // 1, 9 - 1, 9
        && (i[6] - 5 == i[7])  // 9, 4 - 6, 1
        && (i[9] + 2 == i[10]) // 7, 9 - 1, 3
        && (i[8] + 1 == i[11]) // 8, 9 - 1, 2
        && (i[5] - 4 == i[12]) // 9, 5 - 5, 1
        && (i[0] + 5 == i[13]) // 4, 9 - 1, 6
                               // 41299994879959
                               // 01234567890123
                               // 11189561113216
}
