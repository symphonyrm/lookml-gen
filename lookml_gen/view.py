"""
    File name: view.py
    Author: joeschmid
    Date created: 4/8/17
"""
import json
try:
    from textwrap import indent
except ImportError:
    from util import indent

from base_generator import BaseGenerator
from field import FieldType


class View(BaseGenerator):
    def __init__(self, name, label=None, sql_table_name=None, file=None):
        super(View, self).__init__(file=file)
        self.name = name
        self.label = label
        self.sql_table_name = sql_table_name
        self.fields = dict()
        self.derived_table = None

    def generate_lookml(self, file=None, format_options=None):
        if not file and not self.file:
            raise ValueError('Must provide a file in either the constructor '
                             'or as a parameter to generate_lookml()')
        f = file if file else self.file
        fo = format_options if format_options else self.format_options
        if fo.warning_header_comment:
            f.write(fo.warning_header_comment)
        f.write('view: {self.name} {{\n'.format(self=self))
        if self.label:
            f.write('{indent}label: "{self.label}"\n'.
                    format(indent=' ' * fo.indent_spaces, self=self))

        if fo.newline_between_items:
            f.write('\n')

        if self.derived_table:
            self.derived_table.generate_lookml(file=f, format_options=fo)

        if fo.newline_between_items:
            f.write('\n')

        sorted_fields = sorted(self.fields.items())

        self._gen_fields(f, fo, sorted_fields, [FieldType.FILTER])
        self._gen_fields(f, fo, sorted_fields,
                         [FieldType.DIMENSION, FieldType.DIMENSION_GROUP])
        self._gen_fields(f, fo, sorted_fields, [FieldType.MEASURE])

        f.write('}\n')
        return

    def add_field(self, field):
        self.fields[field.name] = field
        return

    def add_derived_table(self, derived_table):
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
    def __init__(self, sql, sql_trigger_value=None, indexes=None, file=None):
        super(DerivedTable, self).__init__(file=file)
        self.sql = sql
        self.sql_trigger_value = sql_trigger_value
        self.indexes = indexes

    def generate_lookml(self, file=None, format_options=None):
        if not file and not self.file:
            raise ValueError('Must provide a file in either the constructor '
                             'or as a parameter to generate_lookml()')
        f = file if file else self.file
        fo = format_options if format_options else self.format_options
        f.write('{indent}derived_table: {{\n'.
                format(indent=' ' * fo.indent_spaces))
        if self.sql:
            final_sql = self.sql if '\n' not in self.sql \
                else '\n' + indent(self.sql, ' ' * 3 * fo.indent_spaces)
            f.write('{indent}sql: {sql} ;;\n'.
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
