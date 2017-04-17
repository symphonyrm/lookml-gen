"""
    File name: conftest.py
    Author: joeschmid
    Date created: 4/17/17
"""
import sys
from os.path import abspath, join, dirname

package_path = abspath(dirname(__file__))
# sys.path.insert(0, join(package_path, 'lookml_gen'))
sys.path.insert(0, package_path)
