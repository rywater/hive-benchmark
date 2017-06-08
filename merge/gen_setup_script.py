
#!/usr/bin/python

import sys

from string import Template
from script_utils import ScriptUtils

TABLE_TEMPLATE = """
  DROP TABLE IF EXISTS $table_name;
  CREATE TABLE IF NOT EXISTS $table_name
    (
      $columns
    )
  ROW FORMAT DELIMITED FIELDS TERMINATED BY ","
  STORED AS TEXTFILE;
  """

LOAD_TEMPLATE = """
  LOAD DATA LOCAL INPATH '$path' OVERWRITE INTO TABLE $table_name;
  """


def main(argv):
    """ Creates script for initial data load """
    table_name = argv[1]
    columns = int(argv[2])
    path = argv[3]
    outfile = argv[4]

    column_definitions = ScriptUtils.create_column_definitions(columns) + ',partitionid STRING'

    table = Template(TABLE_TEMPLATE).substitute(
        table_name=table_name, columns=column_definitions)

    load = Template(LOAD_TEMPLATE).substitute(
        path=path, table_name=table_name)

    ScriptUtils.write_file(outfile, (table + '\n' + load))


if __name__ == '__main__':
    main(sys.argv)
