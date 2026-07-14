"""Nabta Wellness Park - Garden Room 02: Majlis Plaza.

2D plan furnishing detail, drawn inside a circular room of given
center and radius (meters). Traditional majlis seating arrangement:

  - central circular water feature (basin + coping ring)
  - two concentric seat-wall rings, each broken into 8 arc benches
    with 8 entry gaps (outer ring gaps rotated half a bay)
  - 8 radial paving joint lines between the rings
  - perimeter planting-band edge circle

All entities go on layer "NABTA-D-ROOM02" via msp.add_lwpolyline,
msp.add_circle and msp.add_line only. Geometry is proportional to
the room radius so the detail scales with the room.
"""

import math

LAYER = "NABTA-D-ROOM02"
ATTRS = {"layer": LAYER}


def _pt(center, radius, angle):
    """Point at polar (radius, angle) from center."""
    return (center[0] + radius * math.cos(angle),
            center[1] + radius * math.sin(angle))


def _arc_points(center, radius, a0, a1, n=16):
    """List of n+1 points approximating the arc a0->a1."""
    return [_pt(center, radius, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


def _seat_wall_ring(msp, center, r_mid, half_width, n_seats, gap_angle, rot):
    """One ring of n_seats arc benches (closed polylines) with gaps."""
    bay = 2.0 * math.pi / n_seats
    for k in range(n_seats):
        a0 = rot + k * bay + gap_angle / 2.0
        a1 = rot + (k + 1) * bay - gap_angle / 2.0
        outer = _arc_points(center, r_mid + half_width, a0, a1)
        inner = _arc_points(center, r_mid - half_width, a1, a0)
        msp.add_lwpolyline(outer + inner, close=True, dxfattribs=ATTRS)
        # seat centerline (drawn surface joint on the bench top)
        mid = _arc_points(center, r_mid, a0, a1)
        msp.add_lwpolyline(mid, dxfattribs=ATTRS)


def add_detail(msp, center, radius):
    """Add Majlis Plaza plan detail inside circle (center, radius)."""
    r = float(radius)
    n = 8                      # eight bays / eight entry gaps

    # --- central water feature (nominally 3 m dia at r = 7.5 m) ---
    r_water = 0.20 * r         # basin water edge
    r_coping = 0.26 * r        # raised coping outer edge
    msp.add_circle(center, r_water, dxfattribs=ATTRS)
    msp.add_circle(center, r_coping, dxfattribs=ATTRS)
    # scupper joints across the coping, one per bay
    for k in range(n):
        a = k * 2.0 * math.pi / n
        msp.add_line(_pt(center, r_water, a), _pt(center, r_coping, a),
                     dxfattribs=ATTRS)

    # --- inner seat-wall ring: 8 benches, gaps on the bay axes ---
    gap_inner = 2.0 * math.pi / n * 0.30        # ~30% of bay is gap
    _seat_wall_ring(msp, center, r_mid=0.52 * r, half_width=0.035 * r,
                    n_seats=n, gap_angle=gap_inner,
                    rot=2.0 * math.pi / n / 2.0)

    # --- outer seat-wall ring: gaps rotated half a bay ---
    gap_outer = 2.0 * math.pi / n * 0.22
    _seat_wall_ring(msp, center, r_mid=0.78 * r, half_width=0.035 * r,
                    n_seats=n, gap_angle=gap_outer, rot=0.0)

    # --- radial paving joint lines between the two rings ---
    for k in range(n):
        a = (k + 0.5) * 2.0 * math.pi / n
        msp.add_line(_pt(center, r_coping, a),
                     _pt(center, 0.52 * r - 0.035 * r, a),
                     dxfattribs=ATTRS)
        msp.add_line(_pt(center, 0.52 * r + 0.035 * r, a),
                     _pt(center, 0.78 * r - 0.035 * r, a),
                     dxfattribs=ATTRS)

    # --- perimeter planting band edge (inside the room wall) ---
    msp.add_circle(center, 0.92 * r, dxfattribs=ATTRS)

    # --- low side tables: small circles centered in each inner bay ---
    r_table = 0.045 * r
    for k in range(n):
        a = (k + 0.5) * 2.0 * math.pi / n
        msp.add_circle(_pt(center, 0.38 * r, a), r_table, dxfattribs=ATTRS)
