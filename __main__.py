#!/usr/bin/env python3
import os
from sys import argv
from logplotterapi import collect_logs, Axis
from matplotlib import pyplot as plt


def main(argv) -> int:
    if len(argv) < 3:
        return -1

    _, logs, parameter = argv
    functions = collect_logs(logs, parameter)
    fig, ax = plt.subplots(figsize=(7.20, 4.80))
    for (label, data) in functions.items():
        ax.plot(data[Axis.X], data[Axis.Y], marker='o', label=label)
    ax.set_title(parameter)
    plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left')
    fig.savefig(f'{os.path.basename(logs)}.{parameter}.png', bbox_inches='tight')
    return 0


if __name__ == '__main__':
    exit(main(argv))