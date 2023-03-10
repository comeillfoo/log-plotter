#!/usr/bin/env python3
from typing import Tuple
from datetime import datetime
import re
from enum import Enum

Axis = Enum('Axis', ['X', 'Y'])


def parse_record(record: str, ts_format: str, sep: str) -> Tuple[float, str, str, str]:
    timestamp, log_level, class_function, text = record.split(sep, 3)
    timestamp = datetime.strptime(timestamp, ts_format)
    return timestamp.timestamp(), log_level, class_function, text


def parse_parameter(text: str, pattern: re.Pattern, groups: list):
    match = pattern.match(text)
    return bool(match), tuple(map(lambda group: match.group(group), groups))


def collect_logs(logs_path: str, parameter: str, ts_format: str = '%Y-%m-%d %H:%M:%S.%f', sep: str = '|'):
    pattern = re.compile(f'(?P<prefix>.+)?{parameter}:\s*(?P<value>.+)')
    group_names = ['prefix', 'value']
    result = dict()
    with open(logs_path) as logs:
        content = logs.readlines()
        start_msecs, _, _, text = parse_record(content[0], ts_format, sep)
        is_match, (prefix, value) = parse_parameter(text, pattern, group_names)
        if is_match:
            result[prefix][Axis.X].append(0.0)
            result[prefix][Axis.Y].append(value)

        for record in content[:1]:
            msecs, _, _, text = parse_record(record, ts_format, sep)
            is_match, (prefix, value) = parse_parameter(text, pattern, group_names)
            if is_match:
                result[prefix][Axis.X].append(msecs - start_msecs)
                result[prefix][Axis.Y].append(value)

    return result




