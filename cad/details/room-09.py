"""Room 09 -- "Quiet Garden" plan detail, Nabta Wellness Park.

Furnishing plan geometry drawn inside the room circle (center, radius):
  - paired enclosing berm arcs (earth mound edges) wrapping the room,
    open to the south-east as the entry gap
  - central circular reflection basin (4 m dia at r = 10 m) with coping ring
  - single feature tree (canopy + trunk circles) on the north-west axis
  - three contemplation benches arranged tangentially around the basin
All coordinates derive from (center, radius) so the detail scales.
Entities: add_lwpolyline / add_circle / add_line only, on layer NABTA-D-ROOM09.
"""

import math

LAYER = "NABTA-D-ROOM09"


def _arc_points(cx, cy, r, a_start, a_end, n=32):
    """Sample an arc (angles in radians) as a point list for a lwpolyline."""
    pts = []
    for i in range(n + 1):
        a = a_start + (a_end - a_start) * i / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def _rect_points(cx, cy, length, width, angle):
    """Corner points of a rectangle centered at (cx, cy), rotated by angle."""
    ca, sa = math.cos(angle), math.sin(angle)
    hl, hw = length / 2.0, width / 2.0
    corners = ((-hl, -hw), (hl, -hw), (hl, hw), (-hl, hw))
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in corners]


def add_detail(msp, center, radius):
    cx, cy = center
    r = float(radius)
    attribs = {"layer": LAYER}

    # ------------------------------------------------------------------
    # 1. Enclosing berm -- two concentric arc edges (outer toe / inner
    #    crest), sweeping 300 degrees and leaving a 60 degree entry gap
    #    facing south-east (-45 deg).
    # ------------------------------------------------------------------
    gap_center = math.radians(-45.0)
    half_gap = math.radians(30.0)
    a_start = gap_center + half_gap
    a_end = gap_center + 2.0 * math.pi - half_gap

    berm_outer = 0.90 * r
    berm_inner = 0.78 * r
    msp.add_lwpolyline(_arc_points(cx, cy, berm_outer, a_start, a_end, 48),
                       dxfattribs=attribs)
    msp.add_lwpolyline(_arc_points(cx, cy, berm_inner, a_start, a_end, 48),
                       dxfattribs=attribs)

    # Close the berm ends across the entry gap (toe-to-crest return lines).
    for a in (a_start, a_end):
        msp.add_line(
            (cx + berm_inner * math.cos(a), cy + berm_inner * math.sin(a)),
            (cx + berm_outer * math.cos(a), cy + berm_outer * math.sin(a)),
            dxfattribs=attribs,
        )

    # ------------------------------------------------------------------
    # 2. Reflection basin at the room center: water edge + coping ring.
    #    basin_r = 0.20 * r  ->  4 m diameter when the room radius is 10 m.
    # ------------------------------------------------------------------
    basin_r = 0.20 * r
    coping_r = 0.24 * r
    msp.add_circle((cx, cy), basin_r, dxfattribs=attribs)
    msp.add_circle((cx, cy), coping_r, dxfattribs=attribs)

    # Still-water symbol: three short horizontal ripple lines in the basin.
    for k in (-1, 0, 1):
        y = cy + k * 0.35 * basin_r
        half = 0.55 * basin_r * (1.0 if k == 0 else 0.75)
        msp.add_line((cx - half, y), (cx + half, y), dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 3. Single feature tree on the north-west axis (135 deg): canopy
    #    circle, trunk circle, and four crossing branch tick lines.
    # ------------------------------------------------------------------
    tree_a = math.radians(135.0)
    tree_d = 0.52 * r
    tx = cx + tree_d * math.cos(tree_a)
    ty = cy + tree_d * math.sin(tree_a)
    canopy_r = 0.18 * r
    trunk_r = 0.03 * r
    msp.add_circle((tx, ty), canopy_r, dxfattribs=attribs)
    msp.add_circle((tx, ty), trunk_r, dxfattribs=attribs)
    for i in range(4):
        a = tree_a + i * math.pi / 2.0 + math.pi / 4.0
        msp.add_line(
            (tx + trunk_r * math.cos(a), ty + trunk_r * math.sin(a)),
            (tx + 0.85 * canopy_r * math.cos(a), ty + 0.85 * canopy_r * math.sin(a)),
            dxfattribs=attribs,
        )

    # ------------------------------------------------------------------
    # 4. Three benches ringing the basin, tangential (long side facing
    #    the water), placed clear of both the entry gap and the tree.
    #    Bench = 1.8 m x 0.5 m at r = 10 m.
    # ------------------------------------------------------------------
    bench_d = 0.42 * r
    bench_len = 0.18 * r
    bench_wid = 0.05 * r
    for a_deg in (0.0, 90.0, 225.0):
        a = math.radians(a_deg)
        bx = cx + bench_d * math.cos(a)
        by = cy + bench_d * math.sin(a)
        # long axis perpendicular to the radial direction -> tangential
        pts = _rect_points(bx, by, bench_len, bench_wid, a + math.pi / 2.0)
        msp.add_lwpolyline(pts, close=True, dxfattribs=attribs)
        # seat back line along the outer long edge
        back = _rect_points(bx, by, bench_len, 0.6 * bench_wid, a + math.pi / 2.0)
        msp.add_line(back[2], back[3], dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 5. Entry path: two edge lines from the berm gap toward the coping.
    # ------------------------------------------------------------------
    path_half_w = 0.06 * r
    perp = gap_center + math.pi / 2.0
    ox, oy = math.cos(perp) * path_half_w, math.sin(perp) * path_half_w
    for sx, sy in ((ox, oy), (-ox, -oy)):
        msp.add_line(
            (cx + berm_outer * math.cos(gap_center) + sx,
             cy + berm_outer * math.sin(gap_center) + sy),
            (cx + coping_r * math.cos(gap_center) + sx,
             cy + coping_r * math.sin(gap_center) + sy),
            dxfattribs=attribs,
        )
