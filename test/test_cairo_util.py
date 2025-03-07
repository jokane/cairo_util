#!/usr/bin/env python3
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-lines
# pylint: disable=wildcard-import
# pylint: disable=wrong-import-position

import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '..'))
from cairo_util import *

@contextlib.contextmanager
def temporarily_changed_directory(directory):
    """A context in which the current directory has been changed to the
    given one, which should exist already.

    When the context ends, change the current directory back."""
    previous_current_directory = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(previous_current_directory)


@contextlib.contextmanager
def temporary_current_directory():
    """A context in which the current directory is a new temporary
    directory.

    When the context begins, a new temporary directory is created.  This new
    directory becomes the current directory.

    When the context ends, the current directory is restored and the temporary
    directory is vaporized."""
    with tempfile.TemporaryDirectory() as td:
        with temporarily_changed_directory(td):
            try:
                yield
            finally:
                pass

def test_get_fmt1():
    assert get_fmt('foo.png') == 'png'
    assert get_fmt('/home/joe/foo.svg') == 'svg'
    assert get_fmt('/home/joe/foo.svg') == 'svg'

def test_mapped_context1():
    # Basic usage: Get a context, draw some stuff.  In various formats and
    # various sizes.

    sizes = [ [300, 300], [100,300], [300, 100] ]
    user_aabb = ((0, 0), (20, 10))
    points = [ (5,5), (5,10), (10,5), (10,10) ]
    formats = ['svg', 'png', 'pdf']

    for size in sizes:
        for fmt in formats:
            with temporary_current_directory():
                filename = f'test.{fmt}'
                with mapped_context(filename, user_aabb, size) as ctx:
                    for point in points:
                        ctx.set_font_size(1.5)
                        vflip_font(ctx)
                        ctx.set_line_width(0.1)
                        ctx.move_to(point[0], point[1])
                        ctx.show_text(str(point))
                        ctx.arc(point[0], point[1], 0.2, 0, 2*math.pi)
                        ctx.fill()

                assert os.path.exists(filename)
                os.system(f'cp {filename} /tmp')
                assert os.path.getsize(filename) > 100

def test_mapped_context2():
    # Missing format.
    with pytest.raises(ValueError):
        with mapped_context('/dev/null', ((0,0),(20,10)), (300, 300)):
            pass # pragma: nocover

def test_mapped_context3():
    # Unknown format.
    with pytest.raises(ValueError):
        with mapped_context('/dev/null', ((0,0),(20,10)), (300, 300), fmt='tif'):
            pass # pragma: nocover



# If we're run as a script, just execute all of the tests.  Or, if a
# command line argument is given, execute only the tests containing
# that pattern.
if __name__ == '__main__':  #pragma: no cover
    try:
        pattern = sys.argv[1]
    except IndexError:
        pattern = ""
    for name, thing in list(globals().items()):
        if 'test_' in name and pattern in name:
            print('-'*80)
            print(name)
            print('-'*80)
            thing()
            print()

