"""
    File name: field.py
    Author: joeschmid
    Date created: 4/9/17
"""
import json

from .base_generator import BaseGenerator

DEFAULT_TYPE = "string"


class FieldType(object):
    """Enum-style class used to specify known Field types"""

    DIMENSION, DIMENSION_GROUP, FILTER, MEASURE, EXPLORE = range(1, 6)

    @classmethod
    def type_name(cls, type_id):
        if type_id == cls.DIMENSION:
            return "dimension"
        elif type_id == cls.DIMENSION_GROUP:
            return "dimension_group"
        elif type_id == cls.FILTER:
            return "filter"
        elif type_id == cls.MEASURE:
            return "measure"
        elif type_id == cls.EXPLORE:
            return "explore"
        else:
            raise ValueError(
                "Type {} is not a valid FieldType".format(type_id)
            )


class Field(BaseGenerator):
    """Base class used to generate fields within a
    :class:`~lookmlgen.view.View`

    :param field_type: Name of the view
    :param name: Name of the field
    :param type: Type of the field contents, e.g. string, number, etc.
    :param label: Label to use when displaying the field
    :param sql: SQL snippet for the field
    :param hidden: Flag to designate the field as hidden
    :param file: File handle of a file open for writing or a StringIO object
    :param group_label: Group label to use for grouping the field
    :param description: Field description that is show if a user hovers over
                        the help link in the field picker
    :type field_type: a class variable from :class:`FieldType`
    :type name: string
    :type type: string
    :type label: string
    :type sql: string
    :type hidden: bool
    :type file: File handle or StringIO object
    :type group_label: string
    :type description: string

    """

    def __init__(
        self,
        field_type,
        name,
        auto_sql=True,
        type=DEFAULT_TYPE,
        label=None,
        sql=None,
        hidden=None,
        file=None,
        group_label=None,
        description=None,
        **kwargs
    ):
        super(Field, self).__init__(file=file)
        self.field_type = field_type
        self.type_name = FieldType.type_name(field_type)
        self.name = name
        self.type = type
        self.label = label
        self.group_label = group_label
        self.hidden = hidden
        self.description = description

        if auto_sql:
            self.sql = sql if sql else "${TABLE}.%s" % name
        else:
            self.sql = None

    def generate_lookml(self, file=None, format_options=None):
        """Writes LookML for a field to a file or StringIO buffer.

        :param file: File handle of a file open for writing or a
                     StringIO object
        :param format_options: Formatting options to use during generation
        :type file: File handle or StringIO object
        :type format_options:
            :class:`~lookmlgen.base_generator.GeneratorFormatOptions`

        """
        f = file if file else self.file
        fo = format_options if format_options else self.format_options

        f.write(
            "{indent}{self.type_name}: {self.name} {{\n".format(
                indent=" " * fo.indent_spaces, self=self
            )
        )

        # Allow for base 0 spacing -- i.e. no indent at the beginning
        if fo.indent_spaces == 0:
            modifier = 2
        else:
            modifier = 2 * fo.indent_spaces

        if self.hidden:
            f.write("{indent}hidden: yes\n".format(indent=" " * modifier))
        if self.label:
            f.write(
                '{indent}label: "{self.label}"\n'.format(
                    indent=" " * modifier, self=self
                )
            )
        if self.group_label:
            f.write(
                '{indent}group_label: "{self.group_label}"\n'.format(
                    indent=" " * modifier, self=self
                )
            )

        if self.description:
            f.write(
                '{indent}description: "{self.description}"\n'.format(
                    indent=" " * modifier, self=self
                )
            )

        if self.type and not (
            fo.omit_default_field_type and self.type == DEFAULT_TYPE
        ):
            f.write(
                "{indent}type: {self.type}\n".format(
                    indent=" " * modifier, self=self
                )
            )
        self._generate(f, fo)
        if self.sql:
            f.write(
                "{indent}sql: {self.sql} ;;\n".format(
                    indent=" " * modifier, self=self
                )
            )
        f.write("{indent}}}\n".format(indent=" " * fo.indent_spaces))
        return

    def _generate(self, f, fo):
        return


class Dimension(Field):
    """Generates LookML for a dimension field in a
    :class:`~lookmlgen.view.View`

    :param name: Name of the dimension
    :param primary_key: Flag to designate the field as a primary key
    :type name: string
    :type primary_key: bool

    """

    def __init__(self, name, primary_key=None, **kwargs):
        super(Dimension, self).__init__(FieldType.DIMENSION, name, **kwargs)
        self.primary_key = primary_key

    def _generate(self, f, fo):
        if self.primary_key:
            f.write(
                "{indent}primary_key: yes\n".format(
                    indent=" " * 2 * fo.indent_spaces
                )
            )


class DimensionGroup(Field):
    """Generates LookML for a dimension_group field in a
        :class:`~lookmlgen.view.View`

    :param name: Name of the dimension group
    :param timeframes: Timeframes for the group
    :param datatype: Datatype for the group, defaults to 'datetime'
    :type name: string
    :type timeframes: list of strings
    :type datatype: string

    """

    def __init__(self, name, timeframes=None, datatype="datetime", **kwargs):
        super(DimensionGroup, self).__init__(
            FieldType.DIMENSION_GROUP, name, type="time", **kwargs
        )
        self.timeframes = timeframes
        self.datatype = datatype

    def _generate(self, f, fo):
        if not self.timeframes and not fo.omit_time_frames_if_not_set:
            self.timeframes = ["time", "date", "week", "month"]

        if self.timeframes:
            f.write(
                "{indent}timeframes: {timeframes}\n".format(
                    indent=" " * 2 * fo.indent_spaces,
                    timeframes=json.dumps(self.timeframes).replace('"', ""),
                )
            )
        if self.datatype:
            f.write(
                "{indent}datatype: {self.datatype}\n".format(
                    indent=" " * 2 * fo.indent_spaces, self=self
                )
            )


class Measure(Field):
    """Generates LookML for a measure field in a
            :class:`~lookmlgen.view.View`

    :param name: Name of the measure
    :type name: string

    """

    def __init__(self, name, **kwargs):
        super(Measure, self).__init__(FieldType.MEASURE, name, **kwargs)


class Filter(Field):
    """Generates LookML for a filter field in a
            :class:`~lookmlgen.view.View`

    :param name: Name of the filter
    :type name: string

    """

    def __init__(self, name, **kwargs):
        super(Filter, self).__init__(FieldType.FILTER, name, **kwargs)


class Explore(Field):
    """Generates LookML for an explore field in a
            :class:`~lookmlgen.model.Model`

    :param explore_name: Name of explore
    """

    def __init__(self, explore_name, **kwargs):
        super(Explore, self).__init__(
            FieldType.EXPLORE, explore_name, auto_sql=False, **kwargs
        )
