"""Tools to easily get contexts with sensible coordinate systems."""

import contextlib
import os

import cairo # type: ignore

def matrix_to_stretch_rectangle(user_aabb, device_aabb):
    """ Return a Cairo transformation matrix that maps the given user
    rectangle into the given device rectangle, both given as (lower left,
    upper right).  Stretches as needed."""

    xx = (device_aabb[1][0] - device_aabb[0][0]) / (user_aabb[1][0] - user_aabb[0][0])
    x0 = device_aabb[0][0] - xx*user_aabb[0][0]

    yy = (device_aabb[1][1] - device_aabb[0][1]) / (user_aabb[1][1] - user_aabb[0][1])
    y0 = device_aabb[0][1] - yy*user_aabb[0][1]

    return cairo.Matrix(xx=xx, yx=0, xy=0, yy=yy, x0=x0, y0=y0)

def matrix_to_fit_rectangle(user_aabb, device_aabb, padding=0.1):
    """Return a matrix that fits the given user rectangle, as large as
    possible, within the given device rectangle.  Does not stretch.  Preserves
    aspect ratio and centers if there's slack."""

    c = user_aabb[1][0] - user_aabb[0][0]  # user width
    d = user_aabb[1][1] - user_aabb[0][1]  # user height

    pad = max(c,d) * padding

    user_aabb = ((user_aabb[0][0]-pad, user_aabb[0][1]-pad),
                 (user_aabb[1][0]+pad, user_aabb[1][1]+pad))

    c = user_aabb[1][0] - user_aabb[0][0]  # user width, padded
    d = user_aabb[1][1] - user_aabb[0][1]  # user height, padded

    b = device_aabb[1][0] - device_aabb[0][0]  # device width
    a = device_aabb[1][1] - device_aabb[0][1]  # device height

    if -a/d >= b/c:
        m = -b/c
        extra = (a - m*d)/m
        real_user_aabb = ((user_aabb[0][0], user_aabb[0][1]-extra/2),
                          (user_aabb[1][0], user_aabb[1][1]+extra/2))
    else:
        m = -a/d
        extra = (b - m*c)/m
        real_user_aabb = ((user_aabb[0][0]-extra/2, user_aabb[0][1]),
                          (user_aabb[1][0]+extra/2, user_aabb[1][1]))

    return matrix_to_stretch_rectangle(real_user_aabb, device_aabb)


def vflip_font(context):  # pragma: no cover
    """ Change the current font matrix by inverting its vertical axis.  This is
    important if we've re-wired the coordinate system to have the origin in the
    bottom left where it belongs.  Note that calling set_font_size() after
    this will overwrite this change."""

    m = context.get_font_matrix()
    m.yy = -m.yy
    context.set_font_matrix(m)



@contextlib.contextmanager
def mapped_context(filename, user_aabb, device_size, fmt=None, padding=0.1):
    """Return a pycairo surface and a context that can be used to create the
    given file.  Coordinates are mapped so that the given axis-aligned bounding
    box is visible within the given device size.  The specific file format can
    be given directly, or guessed from the filename."""
    with mapped_surface_and_context(filename=filename,
                                    user_aabb=user_aabb,
                                    device_size=device_size,
                                    fmt=fmt,
                                    padding=padding) as (_, context):
        yield context

def get_fmt(filename):
    """Extract and return the extension from a given filename."""
    return os.path.splitext(filename)[1][1:]

@contextlib.contextmanager
def mapped_surface_and_context(filename, user_aabb, device_size, fmt=None, padding=0.1):
    """Same as mapped_context above, but returns the surface as well.  Usually
    you won't need this."""

    surface_classes = {'svg' : cairo.SVGSurface,
                       'pdf' : cairo.PDFSurface}

    if fmt is None:
        fmt = get_fmt(filename)

    if fmt == 'png':
        # Creating a PNG is handled differently by pycairo.  We need to pretend
        # it's going to be an SVG, but then use the SVG surface to save the PNG
        # at the last second.  Send the SVG to /dev/null because we don't
        # actually want that.

        with mapped_surface_and_context('/dev/null',
                                        user_aabb,
                                        device_size,
                                        fmt='svg',
                                        padding=padding) as (surface, context):
            yield surface, context
            surface.write_to_png(filename)

    elif fmt in surface_classes:
        # The general, non-PNG, case.  Create a surface of the appropriate
        # type, create a context for that surface, set its matrix so the
        # coordinates are mapped correctly, and yield it for drawing.

        cls = surface_classes[fmt]

        device_aabb = ((0, device_size[1]), (device_size[0], 0))

        with cls(filename, device_size[0], device_size[1]) as surface:
            context = cairo.Context(surface)
            matrix = matrix_to_fit_rectangle(user_aabb, device_aabb, padding=padding)
            context.set_matrix(matrix)
            yield surface, context
    elif fmt == '':
        raise ValueError(f'Could not determine format from filename: {filename}')
    else:
        raise ValueError(f'Unknown format {fmt}.')
