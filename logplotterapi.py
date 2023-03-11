#!/usr/bin/env python3
from typing import Tuple
from datetime import datetime
import re
from enum import Enum

Axis = Enum('Axis', ['X', 'Y'])


def parse_record(record: str, ts_format: str, sep: str) -> Tuple[float, str, str, str]:
    values = record.split(sep, 3)
    if len(values) != 4:
        raise ValueError(f'Line "{record}" doesn\'t contain enough parameters')
    timestamp, log_level, class_function, text = values
    timestamp = datetime.strptime(timestamp, ts_format)
    return timestamp.timestamp(), log_level, class_function, text


def parse_parameter(message: str, pattern: re.Pattern, groups: list):
    match = pattern.match(message)
    return (False, (None, None)) if match is None else (True, tuple(map(lambda group: match.group(group), groups)))


def add_vertex(vertices: dict, subgroup: str, x: float, y):
    vertices[subgroup] = vertices.get(subgroup, { Axis.X: [], Axis.Y: [] })
    vertices[subgroup][Axis.X].append(x)
    vertices[subgroup][Axis.Y].append(y)


def parse_float(raw_number: str) -> Tuple[bool, any]:
    try:
        number = float(raw_number)
        return True, number
    except (TypeError, ValueError) as e:
        return False, e


def collect_logs(logs_path: str, parameter: str, ts_format: str = '%Y-%m-%d %H:%M:%S.%f', sep: str = '|'):
    pattern = re.compile(f'(?P<prefix>.+)?{re.escape(parameter)}:\s*(?P<value>.+)')
    pattern_group_names = ['prefix', 'value']
    functions_table = dict()
    with open(logs_path) as logs:
        content = logs.readlines()
        # parse first line to get the start time
        start_msecs, _, _, message = parse_record(content[0], ts_format, sep)
        is_match, (prefix, value) = parse_parameter(message, pattern, pattern_group_names)
        if is_match:
            is_parsed, number = parse_float(value)
            add_vertex(functions_table, (prefix or '').strip(" \t\n."), 0.0, number if is_parsed else value)

        # parse the rest lines
        for record in content[1:]:
            try:
                msecs, _, _, message = parse_record(record, ts_format, sep)
                is_match, (prefix, value) = parse_parameter(message, pattern, pattern_group_names)
                if is_match:
                    is_parsed, number = parse_float(value)
                    add_vertex(functions_table, (prefix or '').strip(" \t\n."), (msecs - start_msecs) * 1000, number if is_parsed else value)
            except ValueError as e:
                print(e.__str__().strip())

    return functions_table




