
#!/usr/bin/python

import sys
from script_utils import ScriptUtils

MERGE_TEMPLATE = 'MergeTemplate'


def main(argv):
    """ Creates a test hql script for merge """

    columns = int(argv[1])
    column_delta = int(argv[2])
    base_table = argv[3]
    update_table = argv[4]

    merge_table = argv[5]
    merge_cluster_column = argv[6]
    merge_buckets = argv[7]

    output_file = argv[8]

    column_definitions = ScriptUtils.create_column_definitions(columns)
    column_names = ScriptUtils.create_column_names(columns, 'S.')
    match_statement = __create_match_statement(column_delta)

    test_script = ScriptUtils.create_script(
        MERGE_TEMPLATE, base_table=base_table,
        update_table=update_table,
        match_statement=match_statement,
        merge_table=merge_table,
        merge_cluster_column=merge_cluster_column,
        merge_buckets=merge_buckets,
        columns=column_definitions,
        column_names=column_names)

    ScriptUtils.write_file(output_file, test_script)


def __create_match_statement(column_delta):
    match = '({})'.format(' OR '.join('S.col{} != T.col{}'.format(i, i)
                                      for i in range(column_delta)))

    sets = ','.join('col{} = S.col{}'.format(i, i)
                    for i in range(column_delta))
    return '{} THEN UPDATE SET {}'.format(match, sets)


if __name__ == '__main__':
    main(sys.argv)
