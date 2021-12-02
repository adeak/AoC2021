import os
from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.ticker import IndexLocator

def plot_times():
    file_mapping = defaultdict(list)
    for file in sorted(os.listdir()):
        if not file.endswith(('start', 'end')):
            continue
        day = int(file.split('.')[0][3:])
        file_mapping[day].append(file)

    days = []
    deltas = []
    for day, files in file_mapping.items():
        for file in files:
            with open(file) as f:
                if file.endswith('start'):
                    # multiple lines: pairs of break/end dates
                    startlines = f.readlines()
                else:
                    endline = f.readline()
        timelines = startlines + [endline]

        times = [datetime.strptime(timeline.strip(), '%a %d %b %X %Z %Y') for timeline in timelines]
        intervals = zip(times[::2], times[1::2])  # normally a single [from, to] interval
        delta = 0
        for fr, to in intervals:
            delta += (to - fr).seconds/60
        days.append(day)
        deltas.append(delta)

    fig, ax = plt.subplots()
    ax.plot(days, deltas, 's-')
    ax.grid(True)
    ax.set_xlabel('day')
    ax.set_ylabel('minutes')
    ax.xaxis.set_major_locator(IndexLocator(base=1, offset=0))
    ax.set_xlim(0.5, 25.5)
    fig.tight_layout()

    return fig

if __name__ == "__main__":
    fig = plot_times()

    savefig = False
    if savefig:
        fig.savefig('aoc_work_times.png')

    plt.show()
