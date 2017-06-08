
#!/usr/bin/python

from string import Template


class ScriptUtils(object):
    """ Util methods for generating column names and definitions """

    @staticmethod
    def create_column_definitions(num_columns):
        """ Creates column and metadata name string with column and type def """
        return ','.join(['rowid int', 'insert_time TIMESTAMP'] +
                        ['col{} STRING'.format(i) for i in range(num_columns)])

    @staticmethod
    def create_column_names(num_columns, prefix=None):
        """ Creates column and metadata column name string with only the column name """
        columns = (['rowid', 'insert_time'] +
                   ['col{}'.format(i) for i in range(num_columns)] +
                   ['partitionid'])
        if prefix != None:
            columns = [prefix + col for col in columns]

        return ','.join(columns)

    @staticmethod
    def __prefix(prefix, value):
        return value.format(prefix)

    @staticmethod
    def create_script(template_file, **placeholder_values):
        """ Returns a string with the placeholders in the template file substituted"""
        template = Template(open(template_file, 'r').read())
        return template.substitute(placeholder_values)

    @staticmethod
    def write_file(output_file, output):
        """ Writes output to output_file """
        with open(output_file, 'w') as ofile:
            ofile.write(output)
