"""
    File name: test_model.py
    Author: asingletoaster
    Date Created: 8/10/2021
"""

import six
import os

from lookmlgen import model 
from lookmlgen import field 
from lookmlgen import base_generator

test_format_options = base_generator.GeneratorFormatOptions(warning_header_comment=None)

def test_basic_model():
    testname = "basic_model"
    m = model.Model(testname, "test_connection", ["test_include1"])
    m.add_field(field.Explore("explore1", group_label="Group Label"))

    f = six.StringIO()

    m.generate_lookml(f, format_options=test_format_options)
    lookml = f.getvalue()
    with open(os.path.join(os.path.dirname(__file__), 'expected_output/%s.lkml' % testname), 'rt') as expected:
        assert lookml == expected.read()