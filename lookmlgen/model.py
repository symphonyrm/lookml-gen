"""
    File name: model.py
    Author: asingletoaster
    Date Created: 8/10/2021
"""
from collections import OrderedDict
from .base_generator import BaseGenerator, GeneratorFormatOptions
from .field import FieldType

class Model(BaseGenerator):
    """Generates a LookML Model

    Initialize a Model object with your parameters, 
    add Fields such as :class: `~lookmlgen.field.Connection`,
    :class:`~lookmlgen.field.Include`, and  
    :class:`~lookmlgen.field.Explore`, and then generate LookML
    for the model using :py:meth:`~Model.generate_lookml`

    """

    def __init__(self, name, connection, include_list=[], file=None):
        super(Model, self).__init__(file=file)

        self.name = name
        self.connection = connection
        self.fields = OrderedDict()
        self.include_list = include_list

        self.format_options = GeneratorFormatOptions(indent_spaces=0)

    # Some of this could possibly be a base class method
    def generate_lookml(self, file=None, format_options=None):
        """ Write LookML for the model to a field or StringIO buffer

        :param file: File handle of a file open for writing or a StringIO object
        :param format options: Formatting options to use during generation
        """

        if not file and not self.file: 
            raise ValueError('Must provide a file in either the constructor or as a parameter to generate_lookml()')
        f = file if file else self.file

        # If there are passed in format options, we want to use them, while keeping the indent spacing at base 0 
        if format_options:
            fo = format_options
            fo.indent_spaces = 0
        else: 
            fo = self.format_options

        if fo.warning_header_comment:
            f.write(fo.warning_header_comment)
        f.write('connection: "{self.connection}"\n'.format(self=self))

        if fo.newline_between_items:
            f.write('\n')

        for obj in self.include_list: 
            f.write('include: "{}"\n'.format(obj))
            if fo.newline_between_items:
                f.write('\n')
        
        if fo.view_fields_alphabetical:
            self.__ordered_fields = sorted(self.fields.items())
        else:
            self.__ordered_fields = self.fields.items()
        self.__generated_fields = []

        self._gen_fields(f, fo, [FieldType.EXPLORE])
        
        return


    def add_field(self, field):
        """Adds a :class:`~lookmlgen.field.Field` object to a :class:`View`"""
        self.fields[field.name] = field
        return

    def _gen_fields(self, f, fo, field_types):
        for _, d in self.__ordered_fields:

            if d.field_type not in field_types:
                continue
            if len(self.__generated_fields) != 0 and fo.newline_between_items:
                f.write('\n')

            d.generate_lookml(file=f, format_options=fo)
            self.__generated_fields.append(d)