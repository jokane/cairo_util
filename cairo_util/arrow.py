"""For drawing arrows."""
import math

def draw_arrowhead(ctx, start, end, length, spread, filled=True):
    """Draw an arrowhead on a pycairo context."""
    v = (start[0] - end[0], start[1] - end[1])
    angle_center = math.atan2(v[1], v[0])
    angle_left = angle_center + spread/2
    tip_left = (end[0] + length*math.cos(angle_left), end[1] + length*math.sin(angle_left))
    angle_right = angle_center - spread/2
    tip_right = (end[0] + length*math.cos(angle_right), end[1] + length*math.sin(angle_right))

    if filled:
        ctx.move_to(end[0], end[1])
        ctx.line_to(tip_left[0], tip_left[1])
        ctx.line_to(tip_right[0], tip_right[1])
        ctx.line_to(end[0], end[1])
        ctx.fill()

    ctx.move_to(end[0], end[1])
    ctx.line_to(tip_left[0], tip_left[1])
    ctx.move_to(tip_right[0], tip_right[1])
    ctx.line_to(end[0], end[1])
    ctx.stroke()

