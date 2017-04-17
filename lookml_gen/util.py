"""
    File name: util.py
    Author: joeschmid
    Date created: 4/16/17
"""


def indent(s, num_spaces):
    lines = s.splitlines()
    indented = [' ' * num_spaces + l for l in lines]
    # indented[0] = lines[0]
    if s[-1] == '\n':
        indented[-1] += '\n'
    indented = '\n'.join(indented)
    return indented
