"""
    File name: test_view.py
    Author: joeschmid
    Date created: 4/17/17
"""
import os
import six

from lookmlgen import view
from lookmlgen import field
from lookmlgen import base_generator


test_format_options = base_generator.\
    GeneratorFormatOptions(warning_header_comment=None)


def test_basic_view():
    testname = 'basic_view'
    v = view.View(testname)
    v.add_field(field.Dimension('dimension1', sql='${TABLE}.dim1'))
    f = six.StringIO()
    v.generate_lookml(f, format_options=test_format_options)
    lookml = f.getvalue()
    with open(os.path.join(os.path.dirname(__file__),
                           'expected_output/%s.lkml' % testname),
              'rt') as expected:
        assert lookml == expected.read()


def test_pdt_view():
    testname = 'pdt_view'
    pdt = view.DerivedTable(sql="SELECT id, count(*) c FROM table GROUP BY id",
                            sql_trigger_value='DATE()',
                            indexes=['id'])
    v = view.View(testname)
    v.derived_table = pdt
    v.add_field(field.Dimension('id', type='number',
                                primary_key=True))
    v.add_field(field.Dimension('c', type='number'))
    v.add_field(field.Measure('sum_c', sql='${TABLE}.c', type='sum'))
    f = six.StringIO()
    v.generate_lookml(f, format_options=test_format_options)
    lookml = f.getvalue()
    six.print_(lookml)
    with open(os.path.join(os.path.dirname(__file__),
                           'expected_output/%s.lkml' % testname),
              'rt') as expected:
        assert lookml == expected.read()


def test_dimension_group():
    testname = 'dimension_group_test'
    v = view.View(testname)
    v.add_field(field.DimensionGroup('dimension1', sql='${TABLE}.dim1'))
    f = six.StringIO()
    v.generate_lookml(f, format_options=test_format_options)
    lookml = f.getvalue()
    six.print_(lookml)
    with open(os.path.join(os.path.dirname(__file__),
                           'expected_output/%s.lkml' % testname),
              'rt') as expected:
        assert lookml == expected.read()


def test_dimension_group_no_timeframes():
    testname = 'dimension_group_no_timeframes_test'
    v = view.View(testname)
    v.add_field(field.DimensionGroup('dimension1', sql='${TABLE}.dim1'))
    f = six.StringIO()
    fo_omit_timeframes = base_generator.\
        GeneratorFormatOptions(warning_header_comment=None, omit_time_frames_if_not_set=True)
    v.generate_lookml(f, format_options=fo_omit_timeframes)
    lookml = f.getvalue()
    six.print_(lookml)
    with open(os.path.join(os.path.dirname(__file__),
                           'expected_output/%s.lkml' % testname),
              'rt') as expected:
        assert lookml == expected.read()
