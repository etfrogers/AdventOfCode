from _datetime import datetime
import re
from enum import Enum

import numpy as np


MAP_WIDTH = 60
COMMANDS = {0: 'Guard #(\d+) begins shift',
            1: 'falls asleep',
            2: 'wakes up'}


class RecordType(Enum):
    WAKE = 2
    SLEEP = 1
    GUARD_CHANGE = 0

    @staticmethod
    def from_string(string):
        return RecordType(list(COMMANDS.keys())[list(COMMANDS.values()).index(string)])

    def __str__(self):
        return COMMANDS[self.value]

    @staticmethod
    def to_string(type):
        return COMMANDS[type.value]


class Record:
    LINE_PATTERN = re.compile(r'\[(\d\d\d\d-\d\d-\d\d \d\d:\d\d)\] (.*)')
    GUARD_PATTER = re.compile(COMMANDS[0])

    def __init__(self, line):
        matches = self.LINE_PATTERN.match(line)
        date_str, cmd = matches.groups()
        self.guard_id = None
        self.time = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        if cmd in COMMANDS.values():
            self.type = RecordType.from_string(cmd)
        else:
            guard_match = self.GUARD_PATTER.match(cmd)
            if not guard_match:
                raise ValueError('Unexpected command in record creation')
            self.type = RecordType.GUARD_CHANGE
            self.guard_id = int(guard_match.group(1))

    @property
    def label(self):
        return self.time.strftime('%m-%d')

    @property
    def minute_label(self):
        return self.time.strftime('%m-%d %H:%M')

    def __str__(self):
        return self.minute_label + ' ' + str(self.type).replace('(\d+)', str(self.guard_id))

    @property
    def in_target_hour(self):
        return self.time.hour == 0


class RecordSet:
    def __init__(self, notes):
        self.records = [Record(line) for line in notes]
        assert is_unique([r.minute_label for r in self.records])
        self.records.sort(key=lambda elem: elem.time)
        self.guard_map = None
        self.sleep_map = None
        self.guards = set([record.guard_id for record in self.records if record.guard_id is not None])
        self.days = sorted(list(set([r.label for r in self.records])))
        self.build_map()

    def build_map(self):
        current_guard = None
        self.guard_map = np.zeros((len(self.days), MAP_WIDTH))
        self.sleep_map = np.zeros((len(self.days), MAP_WIDTH))
        for i, record in enumerate(self.records):
            row = self.days.index(record.label)
            if record.type == RecordType.GUARD_CHANGE:
                current_guard = record.guard_id
            elif record.type == RecordType.SLEEP:
                next_record = self.records[i+1]
                sleep_min = record.time.minute
                if next_record.type == RecordType.WAKE:
                    wake_min = next_record.time.minute
                else:
                    assert next_record.time.date() != record.time.date()
                    wake_min = 59
                self.sleep_map[row, sleep_min:wake_min] = RecordType.SLEEP.value
                self.guard_map[row, sleep_min:wake_min] = current_guard
            elif record.type == RecordType.WAKE:
                pass
            else:
                raise ValueError()

    def __str__(self):
        return '\n'.join([str(r) for r in self.records])

    def guard_is_asleep(self, guard_id):
        return np.logical_and(self.guard_map == guard_id, self.sleep_map == RecordType.SLEEP.value)

    def time_asleep(self, guard_id):
        return np.sum(self.guard_is_asleep(guard_id))

    def sleepiest_guard(self):
        ids = list(self.guards)
        sleep_minutes = [self.time_asleep(guard) for guard in ids]
        return ids[sleep_minutes.index(max(sleep_minutes))]

    def sleepiest_minute(self, guard_id):
        minutes = self.minutes_asleep(guard_id)
        return np.argmax(minutes)

    def minutes_asleep(self, guard_id):
        minutes = np.sum(self.guard_is_asleep(guard_id), 0)
        return minutes

    def sleepiest_guard_minute(self):
        ids = list(self.guards)
        sleep_minutes = np.array([self.minutes_asleep(guard) for guard in ids])
        guard_index, minute = np.unravel_index(np.argmax(sleep_minutes), sleep_minutes.shape)
        return ids[guard_index], minute


def is_unique(list_):
    return len(list_) == len(set(list_))


if __name__ == '__main__':
    with open('input.txt') as f:
        input_ = f.readlines()
    input_ = [line.strip() for line in input_]
    records = RecordSet(input_)
    print(records)

    guard = records.sleepiest_guard()
    minute = records.sleepiest_minute(guard)
    print(guard)
    print(minute)
    print(guard * minute)

    guard, minute = records.sleepiest_guard_minute()
    print()
    print(guard)
    print(minute)
    print(guard * minute)

