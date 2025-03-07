#!/usr/bin/env python3
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=wildcard-import
# pylint: disable=too-many-lines

import sys

from cairo_util import *

def test_get_fmt1():
    assert get_fmt('foo.png') == 'png'

# if '__main__' == __name__:  # pragma: no cover
#     svg_size = [300, 300]
#     user_aabb = ((0, 0), (20, 10))
#     points = [
#         (5,5),
#         (5,10),
#         (10,5),
#         (10,10),
#     ]
#
#     with mapped_svg_context('test.svg', user_aabb, svg_size) as ctx:
#         ctx.set_font_size(1.5)
#         vflip_font(ctx)
#         ctx.set_line_width(0.1)
#
#         ctx.move_to(user_aabb[0][0], user_aabb[0][1])
#         ctx.line_to(user_aabb[1][0], user_aabb[0][1])
#         ctx.line_to(user_aabb[1][0], user_aabb[1][1])
#         ctx.line_to(user_aabb[0][0], user_aabb[1][1])
#         ctx.line_to(user_aabb[0][0], user_aabb[0][1])
#         ctx.stroke()
#
#         for point in points:
#             ctx.move_to(point[0], point[1])
#             ctx.show_text(str(point))
#             ctx.arc(point[0], point[1], 0.2, 0, 2*math.pi)
#             ctx.fill()

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

