
#!/usr/bin/python

import sys

from script_utils import ScriptUtils

INSERT_TEMPLATE = 'InsertOverwriteTemplate'


def main(argv):
    """ Creates test script for insert overwrite """
    columns = int(argv[1])
    base_table = argv[2]
    update_table = argv[3]
    overwrite_table = argv[4]
    output_file = argv[5]

    column_definitions = ScriptUtils.create_column_definitions(columns)
    column_names = ScriptUtils.create_column_names(columns)

    test_script = ScriptUtils.create_script(INSERT_TEMPLATE,
                                            columns=column_definitions,
                                            column_names=column_names,
                                            base_table=base_table,
                                            update_table=update_table,
                                            overwrite_table=overwrite_table)

    ScriptUtils.write_file(output_file, test_script)


if __name__ == '__main__':
    main(sys.argv)
