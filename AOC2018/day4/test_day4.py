import day4

test_input = '''[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up'''

notes = test_input.split('\n')
records = day4.RecordSet(notes)


def test_1():
    assert records.time_asleep(10) == 50


def test_2():
    assert records.time_asleep(99) == 30


def test_3():
    assert records.sleepiest_guard() == 10


def test_4():
    assert records.sleepiest_minute(10) == 24


def test_5():
    guard = records.sleepiest_guard()
    minute = records.sleepiest_minute(guard)
    assert guard * minute == 240
