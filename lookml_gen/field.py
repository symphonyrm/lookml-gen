"""
    File name: field.py
    Author: joeschmid
    Date created: 4/9/17
"""
from base_generator import BaseGenerator

DEFAULT_TYPE = 'string'


class FieldType(object):
    DIMENSION, DIMENSION_GROUP, FILTER, MEASURE = range(1, 5)

    @classmethod
    def type_name(cls, type_id):
        if type_id == cls.DIMENSION:
            return 'dimension'
        elif type_id == cls.DIMENSION_GROUP:
            return 'dimension_group'
        elif type_id == cls.FILTER:
            return 'filter'
        elif type_id == cls.MEASURE:
            return 'measure'
        else:
            raise ValueError('Type {} is not a valid FieldType'.
                             format(type_id))


class Field(BaseGenerator):
    def __init__(self, field_type, name, type=DEFAULT_TYPE, label=None,
                 sql=None, primary_key=None, hidden=None,
                 file=None, **kwargs):
        super(Field, self).__init__(file=file)
        self.field_type = field_type
        self.type_name = FieldType.type_name(field_type)
        self.name = name
        self.type = type
        self.label = label
        self.sql = sql
        self.primary_key = primary_key
        self.hidden = hidden

    def generate_lookml(self, file=None, format_options=None):
        f = file if file else self.file
        fo = format_options if format_options else self.format_options
        f.write('{indent}{self.type_name}: {self.name} {{\n'.
                format(indent=' ' * fo.indent_spaces, self=self))
        if self.primary_key:
            f.write('{indent}primary_key: yes\n'.
                    format(indent=' ' * 2 * fo.indent_spaces))
        if self.hidden:
            f.write('{indent}hidden: yes\n'.
                    format(indent=' ' * 2 * fo.indent_spaces))
        if self.label:
            f.write('{indent}label: "{self.label}"\n'.
                    format(indent=' ' * 2 * fo.indent_spaces, self=self))
        if self.type and not (fo.omit_default_field_type and
                              self.type == DEFAULT_TYPE):
            f.write('{indent}type: {self.type}\n'.
                    format(indent=' ' * 2 * fo.indent_spaces, self=self))
        self._generate(f, fo)
        if self.sql:
            f.write('{indent}sql: {self.sql} ;;\n'.
                    format(indent=' ' * 2 * fo.indent_spaces, self=self))
        f.write('{indent}}}\n'.format(indent=' ' * fo.indent_spaces))
        return

    def _generate(self, f, fo):
        return


class Dimension(Field):
    def __init__(self, name, **kwargs):
        super(Dimension, self).__init__(FieldType.DIMENSION, name, **kwargs)


class DimensionGroup(Field):
    def __init__(self, name, timeframes='[time, date, week, month]',
                 datatype='datetime', **kwargs):
        super(DimensionGroup, self).__init__(FieldType.DIMENSION_GROUP, name,
                                             type='time', **kwargs)
        self.timeframes = timeframes
        self.datatype = datatype

    def _generate(self, f, fo):
        if self.timeframes:
            f.write('{indent}timeframes: {self.timeframes}\n'.
                    format(indent=' ' * 2 * fo.indent_spaces, self=self))
        if self.datatype:
            f.write('{indent}datatype: {self.datatype}\n'.
                    format(indent=' ' * 2 * fo.indent_spaces, self=self))


class Measure(Field):
    def __init__(self, name, **kwargs):
        super(Measure, self).__init__(FieldType.MEASURE, name, **kwargs)


class Filter(Field):
    def __init__(self, name, **kwargs):
        super(Filter, self).__init__(FieldType.FILTER, name, **kwargs)
