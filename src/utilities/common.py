import sys


def progress(count, total, status='', visual=True):
    bar_len = 100
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    if visual:
        sys.stdout.write('[{}] {}{} ...{}\r'.format(bar, percents, '%', status))
        sys.stdout.flush()
    else:
        return '[{}] {}{} ...{}\r'.format(bar, percents, '%', status)


def frange(start, stop, step, precision=5):
    while start < stop:
        yield int(start * 10**precision) / 10**precision
        start += step
