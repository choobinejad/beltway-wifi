from datetime import datetime
import fire
from prettytable import PrettyTable
from analytics.travel import find_companions as fc


def find_companions(mac):
    counter, result, unique_companions = fc(mac)

    # Print out the companions list
    print('\nThe `companions` algorithm identified {} unique companions for {}. They are:'.format(
        len(unique_companions), mac
    ))
    print(', '.join(list(unique_companions)[:10]) + ', ...')

    # Print out the raw result records, bucketed by time and space dimensions
    raw = PrettyTable()
    raw.field_names = ['Timestamp', 'Geohash', 'Companions']
    for r in result:
        truncated = '...' if len(r[2]) > 3 else ''
        raw.add_row([datetime.fromtimestamp(r[0]/1000.0).isoformat(), r[1], ', '.join(r[2][:3]) + truncated])
    raw.add_row(['...', '...', '...'])
    print('\nHere is a sample of the raw results:')
    print(raw)

    # Print out the inverted summary of closest companions
    indexed = PrettyTable()
    indexed.field_names = ['Companion', 'Occurrences']
    for k, v in counter.most_common(10):
        indexed.add_row([k, str(v)])
    indexed.add_row(['...', '...'])
    print('\nThe most significantly correlated companions for {} are:'.format(mac))
    print(indexed)


if __name__ == '__main__':
    fire.Fire()
