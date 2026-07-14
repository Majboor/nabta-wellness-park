"""Nabta Wellness Park - Garden Room 06 "Fitness Grove".

2D plan furnishing detail rendered inside a circular garden room.
All geometry is derived from (center, radius) so the detail scales
with the room. Nominal design radius is 20 m: at that size the six
outdoor-gym equipment pads measure exactly 2 x 4 m.

Layout (all inside the room circle):
  - Perimeter jogging/soft-track loop (two concentric circles).
  - Six equipment pads (2x4 m at nominal radius) on an arc, each
    rotated to face the room center, with an equipment axis line.
  - Central stretching-lawn ellipse (polyline approximation).
  - Two pull-up / calisthenics bar frames flanking the lawn.
  - Entry path spine from the track to the lawn.

Only msp.add_lwpolyline / msp.add_circle / msp.add_line are used,
all on layer "NABTA-D-ROOM06". No imports beyond math.
"""

import math

LAYER = "NABTA-D-ROOM06"
NOMINAL_RADIUS = 20.0  # meters; pads are 2x4 m at this room radius


def _attrs():
    return {"layer": LAYER}


def _rot(px, py, ang):
    """Rotate point (px, py) about origin by ang radians."""
    c = math.cos(ang)
    s = math.sin(ang)
    return px * c - py * s, px * s + py * c


def _rect(msp, cx, cy, width, length, ang):
    """Closed rectangle centered at (cx, cy), long axis along ang."""
    hw = width / 2.0
    hl = length / 2.0
    corners = [(-hl, -hw), (hl, -hw), (hl, hw), (-hl, hw)]
    pts = []
    for px, py in corners:
        rx, ry = _rot(px, py, ang)
        pts.append((cx + rx, cy + ry))
    msp.add_lwpolyline(pts, close=True, dxfattribs=_attrs())


def _ellipse_poly(msp, cx, cy, a, b, ang, segments=48):
    """Closed polyline approximating an ellipse (semi-axes a, b)."""
    pts = []
    for i in range(segments):
        t = 2.0 * math.pi * i / segments
        px = a * math.cos(t)
        py = b * math.sin(t)
        rx, ry = _rot(px, py, ang)
        pts.append((cx + rx, cy + ry))
    msp.add_lwpolyline(pts, close=True, dxfattribs=_attrs())


def add_detail(msp, center, radius):
    """Add Fitness Grove plan detail inside circle (center, radius)."""
    cx, cy = center
    s = radius / NOMINAL_RADIUS  # scale factor (1.0 at 20 m radius)

    # ------------------------------------------------------------------
    # 1. Perimeter jogging / soft-surface track loop
    # ------------------------------------------------------------------
    track_outer = radius * 0.92
    track_inner = radius * 0.80
    msp.add_circle((cx, cy), track_outer, dxfattribs=_attrs())
    msp.add_circle((cx, cy), track_inner, dxfattribs=_attrs())

    # Lane tick marks across the track every 30 degrees
    for i in range(12):
        a = math.radians(30.0 * i)
        x1 = cx + track_inner * math.cos(a)
        y1 = cy + track_inner * math.sin(a)
        x2 = cx + track_outer * math.cos(a)
        y2 = cy + track_outer * math.sin(a)
        msp.add_line((x1, y1), (x2, y2), dxfattribs=_attrs())

    # ------------------------------------------------------------------
    # 2. Six equipment pads (2x4 m nominal) on an arc, facing center
    # ------------------------------------------------------------------
    pad_w = 2.0 * s
    pad_l = 4.0 * s
    pad_ring = radius * 0.62
    # Arc from 120 deg to 420 deg leaves a gap at ~90 deg for the entry
    for i in range(6):
        a = math.radians(120.0 + 60.0 * i)
        px = cx + pad_ring * math.cos(a)
        py = cy + pad_ring * math.sin(a)
        # Long axis tangent to the arc so short side faces the center
        _rect(msp, px, py, pad_w, pad_l, a + math.pi / 2.0)
        # Equipment axis line on the pad (frame footprint hint)
        ax, ay = _rot(pad_l * 0.35, 0.0, a + math.pi / 2.0)
        msp.add_line((px - ax, py - ay), (px + ax, py + ay),
                     dxfattribs=_attrs())
        # Anchor bolt circles at the ends of the equipment axis
        bolt_r = 0.15 * s
        msp.add_circle((px - ax, py - ay), bolt_r, dxfattribs=_attrs())
        msp.add_circle((px + ax, py + ay), bolt_r, dxfattribs=_attrs())

    # ------------------------------------------------------------------
    # 3. Central stretching lawn (ellipse) with mowing-edge offset
    # ------------------------------------------------------------------
    lawn_a = radius * 0.34
    lawn_b = radius * 0.22
    lawn_ang = math.radians(15.0)
    _ellipse_poly(msp, cx, cy, lawn_a, lawn_b, lawn_ang)
    _ellipse_poly(msp, cx, cy, lawn_a - 0.5 * s, lawn_b - 0.5 * s, lawn_ang)

    # ------------------------------------------------------------------
    # 4. Pull-up / calisthenics bar frames flanking the lawn
    # ------------------------------------------------------------------
    bar_len = 3.0 * s
    bar_ring = radius * 0.52
    for side_deg in (200.0, 340.0):
        a = math.radians(side_deg)
        bx = cx + bar_ring * math.cos(a)
        by = cy + bar_ring * math.sin(a)
        tang = a + math.pi / 2.0
        dx, dy = _rot(bar_len / 2.0, 0.0, tang)
        # Bar line between two post circles
        msp.add_line((bx - dx, by - dy), (bx + dx, by + dy),
                     dxfattribs=_attrs())
        post_r = 0.2 * s
        msp.add_circle((bx - dx, by - dy), post_r, dxfattribs=_attrs())
        msp.add_circle((bx + dx, by + dy), post_r, dxfattribs=_attrs())
        # Safety surfacing rectangle around the frame
        _rect(msp, bx, by, 2.0 * s, bar_len + 2.0 * s, tang)

    # ------------------------------------------------------------------
    # 5. Entry path spine from track to lawn (through the pad-arc gap)
    # ------------------------------------------------------------------
    path_hw = 1.0 * s  # half width of the 2 m nominal path
    a = math.radians(90.0)  # gap left in the equipment arc
    r0 = track_inner
    r1 = lawn_b + 1.0 * s
    ca, sa = math.cos(a), math.sin(a)
    # Perpendicular offset direction for the path edges
    ox, oy = -sa * path_hw, ca * path_hw
    msp.add_line((cx + r1 * ca + ox, cy + r1 * sa + oy),
                 (cx + r0 * ca + ox, cy + r0 * sa + oy),
                 dxfattribs=_attrs())
    msp.add_line((cx + r1 * ca - ox, cy + r1 * sa - oy),
                 (cx + r0 * ca - ox, cy + r0 * sa - oy),
                 dxfattribs=_attrs())
