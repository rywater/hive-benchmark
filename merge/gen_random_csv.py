
#!/usr/bin/python

import sys
import time
import random
import string
import datetime


def main(argv):
    """
    Generates random CSV data based off of the provided parameters
    Expects the following in order: rows, columns, column_size, partitions, ofile
    """
    rows = int(argv[1])
    columns = int(argv[2])
    column_size = int(argv[3])
    partitions = int(argv[4])
    ofile = argv[5]

    available_partitions = __generate_partitions(partitions)

    print 'Writing {} rows, {} columns (+3 metadata columns)' \
        'of size {} to {}'.format(rows, columns, column_size, ofile)

    start = time.time()
    with open(ofile, 'w') as ofile:
        for i in range(rows):
            line = __generate_line(
                i, columns, column_size, available_partitions) + '\n'

            ofile.write(line)

    print 'Wrote {} rows, {} columns in {}'.format(rows, columns, time.time() - start)


def __generate_line(index, columns, column_size, partitions):
    partition_column = str(random.choice(partitions))
    timestamp = str(datetime.datetime.now())
    column_data = list(__generate_column(column_size) for _ in range(columns))
    return ','.join([str(index), timestamp] + column_data + [partition_column])


def __generate_partitions(partitions):
    return [i for i in xrange(partitions)]


def __generate_column(column_size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(column_size))


if __name__ == '__main__':
    main(sys.argv)
