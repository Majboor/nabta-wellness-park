"""NABTA Wellness Park - Garden Room 05 "Teen Court".

2D plan furnishing detail: multi-use teen sports court (basketball layout)
fitted inside the room circle, plus perimeter benches. All geometry is
derived from (center, radius) so the detail scales with the room.

Only msp.add_lwpolyline / msp.add_circle / msp.add_line are used, all on
layer "NABTA-D-ROOM05" (layer assumed to exist).
"""

import math

LAYER = "NABTA-D-ROOM05"


def _attribs():
    return {"layer": LAYER}


def _rect(msp, cx, cy, hw, hh):
    """Closed rectangle centered at (cx, cy) with half-width/half-height."""
    pts = [
        (cx - hw, cy - hh),
        (cx + hw, cy - hh),
        (cx + hw, cy + hh),
        (cx - hw, cy + hh),
    ]
    msp.add_lwpolyline(pts, close=True, dxfattribs=_attribs())


def _arc_polyline(msp, cx, cy, r, a0, a1, segments=24):
    """Approximate a circular arc (radians a0->a1) with a polyline."""
    pts = []
    for i in range(segments + 1):
        a = a0 + (a1 - a0) * i / segments
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    msp.add_lwpolyline(pts, close=False, dxfattribs=_attribs())


def add_detail(msp, center, radius):
    """Add Teen Court furnishing plan detail inside circle (center, radius)."""
    cx, cy = center

    # --- Court sizing -----------------------------------------------------
    # Reference court: 15 m x 28 m (FIBA-style). Scale it so the court's
    # corners sit comfortably inside the room circle (85% of radius).
    ref_w, ref_l = 15.0, 28.0
    half_diag = 0.5 * math.hypot(ref_w, ref_l)
    k = (0.85 * radius) / half_diag  # scale factor: ref meters -> plan meters

    hw = 0.5 * ref_w * k   # court half-width  (x direction)
    hl = 0.5 * ref_l * k   # court half-length (y direction)

    # --- Court outline ----------------------------------------------------
    _rect(msp, cx, cy, hw, hl)

    # --- Center (half-court) line and center circle ------------------------
    msp.add_line((cx - hw, cy), (cx + hw, cy), dxfattribs=_attribs())
    msp.add_circle((cx, cy), 1.8 * k, dxfattribs=_attribs())

    # --- Keys, free-throw circles, hoops, three-point arcs -----------------
    key_hw = 0.5 * 4.9 * k        # key half-width
    key_depth = 5.8 * k           # key depth from baseline
    ft_r = 1.8 * k                # free-throw circle radius
    hoop_r = 0.225 * k            # hoop ring radius
    hoop_off = 1.575 * k          # hoop center offset from baseline
    board_hw = 0.5 * 1.8 * k      # backboard half-width
    board_off = 1.2 * k           # backboard offset from baseline
    three_r = 6.75 * k            # three-point arc radius

    for sign in (1.0, -1.0):
        base_y = cy + sign * hl                 # baseline y
        ft_y = base_y - sign * key_depth        # free-throw line y
        hoop_y = base_y - sign * hoop_off       # hoop center y
        board_y = base_y - sign * board_off     # backboard y

        # Key (lane) rectangle from baseline to free-throw line.
        key_pts = [
            (cx - key_hw, base_y),
            (cx - key_hw, ft_y),
            (cx + key_hw, ft_y),
            (cx + key_hw, base_y),
        ]
        msp.add_lwpolyline(key_pts, close=False, dxfattribs=_attribs())

        # Free-throw circle and hoop ring.
        msp.add_circle((cx, ft_y), ft_r, dxfattribs=_attribs())
        msp.add_circle((cx, hoop_y), hoop_r, dxfattribs=_attribs())

        # Backboard.
        msp.add_line(
            (cx - board_hw, board_y),
            (cx + board_hw, board_y),
            dxfattribs=_attribs(),
        )

        # Three-point arc centered on the hoop, opening toward mid-court.
        if sign > 0:
            _arc_polyline(msp, cx, hoop_y, three_r, math.pi, 2.0 * math.pi)
        else:
            _arc_polyline(msp, cx, hoop_y, three_r, 0.0, math.pi)

    # --- Perimeter benches ------------------------------------------------
    # Four benches on the ring between the court corners and the room edge,
    # placed on the diagonals, tangent to the circle direction.
    bench_len = 0.5 * 4.0 * k * 2.0   # bench length ~4 m (scaled), half below
    bench_hl = 0.5 * bench_len
    bench_hw = 0.5 * 0.6 * k          # bench half-depth (~0.6 m seat)
    bench_rad = 0.93 * radius         # radial placement of bench centerline

    for ang_deg in (45.0, 135.0, 225.0, 315.0):
        a = math.radians(ang_deg)
        bx = cx + bench_rad * math.cos(a)
        by = cy + bench_rad * math.sin(a)
        # Tangent (perpendicular to radial) direction.
        tx, ty = -math.sin(a), math.cos(a)
        # Radial (inward) direction for bench depth.
        nx, ny = -math.cos(a), -math.sin(a)
        pts = [
            (bx - tx * bench_hl - nx * bench_hw, by - ty * bench_hl - ny * bench_hw),
            (bx + tx * bench_hl - nx * bench_hw, by + ty * bench_hl - ny * bench_hw),
            (bx + tx * bench_hl + nx * bench_hw, by + ty * bench_hl + ny * bench_hw),
            (bx - tx * bench_hl + nx * bench_hw, by - ty * bench_hl + ny * bench_hw),
        ]
        msp.add_lwpolyline(pts, close=True, dxfattribs=_attribs())
