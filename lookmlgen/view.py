"""
    File name: view.py
    Author: joeschmid
    Date created: 4/8/17
"""
import json
from collections import OrderedDict
try:
    from textwrap import indent
except ImportError:
    from .util import indent

from .base_generator import BaseGenerator
from .field import FieldType


class View(BaseGenerator):
    """Generates a LookML View

    Initialize a View object with your parameters,
    add Fields such as :class:`~lookmlgen.field.Dimension`,
    :class:`~lookmlgen.field.Measure`,
    :class:`~lookmlgen.field.DimensionGroup`, and
    :class:`~lookmlgen.field.Filter`, and then
    generate LookML for the view using :py:meth:`~View.generate_lookml`

    :param name: Name of the view
    :param label: Label to use for the view (may contain spaces)
    :param sql_table_name: Name of the SQL table to use in the view
    :param file: File handle of a file open for writing or a
                 StringIO object
    :type name: string
    :type label: string
    :type sql_table_name: list of strings
    :type file: File handle or StringIO object

    """
    def __init__(self, name, label=None, sql_table_name=None, file=None):
        super(View, self).__init__(file=file)
        self.name = name
        self.label = label
        self.sql_table_name = sql_table_name
        self.fields = OrderedDict()
        self.derived_table = None

    def generate_lookml(self, file=None, format_options=None):
        """ Writes LookML for the view to a file or StringIO buffer.

        :param file: File handle of a file open for writing or a
                     StringIO object
        :param format_options: Formatting options to use during generation
        :type file: File handle or StringIO object
        :type format_options:
            :class:`~lookmlgen.base_generator.GeneratorFormatOptions`

        """
        if not file and not self.file:
            raise ValueError('Must provide a file in either the constructor '
                             'or as a parameter to generate_lookml()')
        f = file if file else self.file
        fo = format_options if format_options else self.format_options
        if fo.warning_header_comment:
            f.write(fo.warning_header_comment)
        f.write('view: {self.name} {{\n'.format(self=self))
        if self.sql_table_name:
            f.write('{indent}sql_table_name: {self.sql_table_name} ;;\n'.
                    format(indent=' ' * fo.indent_spaces, self=self))
        if self.label:
            f.write('{indent}label: "{self.label}"\n'.
                    format(indent=' ' * fo.indent_spaces, self=self))

        if fo.newline_between_items:
            f.write('\n')

        if self.derived_table:
            self.derived_table.generate_lookml(file=f, format_options=fo)
            if fo.newline_between_items:
                f.write('\n')

        if fo.view_fields_alphabetical:
            ordered_fields = sorted(self.fields.items())
        else:
            ordered_fields = self.fields.items()
        self._gen_fields(f, fo, ordered_fields, [FieldType.FILTER])
        self._gen_fields(f, fo, ordered_fields,
                         [FieldType.DIMENSION, FieldType.DIMENSION_GROUP])
        self._gen_fields(f, fo, ordered_fields, [FieldType.MEASURE])

        f.write('}\n')
        return

    def add_field(self, field):
        """Adds a :class:`~lookmlgen.field.Field` object to a :class:`View`"""
        self.fields[field.name] = field
        return

    def set_derived_table(self, derived_table):
        """Adds a :class:`~lookmlgen.view.DerivedTable` object to a
         :class:`View`
        """
        self.derived_table = derived_table

    @classmethod
    def _gen_fields(cls, f, fo, sorted_fields, field_types):
        first = True
        for k, d in sorted_fields:
            if not first and fo.newline_between_items:
                f.write('\n')
            if d.field_type not in field_types:
                continue
            d.generate_lookml(file=f, format_options=fo)
            if first:
                first = False


class DerivedTable(BaseGenerator):
    """Generates the LookML View parameters to support derived
    tables, including persistent derived tables (PDTs).

    :param sql: SQL statement to execute
    :param sql_trigger_value: SQL to determine when to trigger build
    :param indexes: List of coluxn names to use as indexes
    :param file: File handle of a file open for writing or a StringIO object
    :type sql: string
    :type sql_trigger_value: string
    :type indexes: list of strings
    :type file: File handle or StringIO object

    """
    def __init__(self, sql, sql_trigger_value=None, indexes=None, file=None):
        super(DerivedTable, self).__init__(file=file)
        self.sql = sql
        self.sql_trigger_value = sql_trigger_value
        self.indexes = indexes

    def generate_lookml(self, file=None, format_options=None):
        """ Writes LookML for a derived table to a file or StringIO buffer.

        :param file: File handle of a file open for writing or a
                     StringIO object
        :param format_options: Formatting options to use during generation
        :type file: File handle or StringIO object
        :type format_options:
            :class:`~lookmlgen.base_generator.GeneratorFormatOptions`

        """
        if not file and not self.file:
            raise ValueError('Must provide a file in either the constructor '
                             'or as a parameter to generate_lookml()')
        f = file if file else self.file
        fo = format_options if format_options else self.format_options
        f.write('{indent}derived_table: {{\n'.
                format(indent=' ' * fo.indent_spaces))
        if self.sql:
            final_sql = ' ' + self.sql if '\n' not in self.sql \
                else '\n' + indent(self.sql, ' ' * 3 * fo.indent_spaces)
            f.write('{indent}sql:{sql} ;;\n'.
                    format(indent=' ' * 2 * fo.indent_spaces, sql=final_sql))
        if self.sql_trigger_value:
            f.write('{indent}sql_trigger_value: '
                    '{self.sql_trigger_value} ;;\n'.
                    format(indent=' ' * 2 * fo.indent_spaces, self=self))
        if self.indexes:
            f.write('{indent}indexes: {indexes}\n'.
                    format(indent=' ' * 2 * fo.indent_spaces,
                           indexes=json.dumps(self.indexes)))
        f.write('{indent}}}\n'.format(indent=' ' * fo.indent_spaces))
