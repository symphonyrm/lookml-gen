"""
    File name: conftest.py
    Author: joeschmid
    Date created: 4/17/17
"""
import sys
from os.path import abspath, dirname, join

package_path = abspath(dirname(__file__))
# sys.path.insert(0, join(package_path, 'lookmlgen'))
sys.path.insert(0, package_path)
