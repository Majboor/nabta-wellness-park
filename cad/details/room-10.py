"""Nabta Wellness Park - Garden Room 10 "Cafe Terrace" plan detail.

Furnishing plan geometry drawn inside the room circle:
  - Cafe kiosk building (8 x 12 m footprint, scaled to room) with door notch
  - Service counter line along the kiosk front
  - Terrace grid of 8 parasols (circle + center post) with cafe tables
  - Terrace paving edge band and two planter strips

All coordinates are derived from (center, radius) so the detail scales
with the room. Layer: NABTA-D-ROOM10.
"""

import math

LAYER = "NABTA-D-ROOM10"


def _attrs():
    return {"layer": LAYER}


def add_detail(msp, center, radius):
    cx, cy = center
    r = float(radius)

    # ------------------------------------------------------------------
    # Scale: geometry authored for a nominal 20 m radius room, scaled by s.
    # ------------------------------------------------------------------
    s = r / 20.0

    # ------------------------------------------------------------------
    # 1. Terrace paving edge band (inner ring boundary as polyline octagon-32)
    # ------------------------------------------------------------------
    edge_r = r * 0.92
    pts = []
    n_seg = 32
    for i in range(n_seg):
        a = 2.0 * math.pi * i / n_seg
        pts.append((cx + edge_r * math.cos(a), cy + edge_r * math.sin(a)))
    msp.add_lwpolyline(pts, close=True, dxfattribs=_attrs())

    # ------------------------------------------------------------------
    # 2. Cafe kiosk building: 8 x 12 m rectangle (scaled), placed toward
    #    the north side of the room, long axis east-west.
    # ------------------------------------------------------------------
    kw = 12.0 * s   # kiosk width  (x extent)
    kd = 8.0 * s    # kiosk depth  (y extent)
    k_cy = cy + r * 0.45          # kiosk band center y
    kx0 = cx - kw / 2.0
    kx1 = cx + kw / 2.0
    ky0 = k_cy - kd / 2.0
    ky1 = k_cy + kd / 2.0
    msp.add_lwpolyline(
        [(kx0, ky0), (kx1, ky0), (kx1, ky1), (kx0, ky1)],
        close=True,
        dxfattribs=_attrs(),
    )

    # Inner wall line (kiosk wall thickness 0.3 m scaled)
    t = 0.3 * s
    msp.add_lwpolyline(
        [(kx0 + t, ky0 + t), (kx1 - t, ky0 + t),
         (kx1 - t, ky1 - t), (kx0 + t, ky1 - t)],
        close=True,
        dxfattribs=_attrs(),
    )

    # Door notch on the south face (2 m opening, centered)
    door_w = 2.0 * s
    msp.add_line((cx - door_w / 2.0, ky0), (cx - door_w / 2.0, ky0 + t),
                 dxfattribs=_attrs())
    msp.add_line((cx + door_w / 2.0, ky0), (cx + door_w / 2.0, ky0 + t),
                 dxfattribs=_attrs())
    # Door swing leaf (simple line)
    msp.add_line((cx - door_w / 2.0, ky0),
                 (cx - door_w / 2.0 + door_w * math.cos(math.radians(60)),
                  ky0 - door_w * math.sin(math.radians(60))),
                 dxfattribs=_attrs())

    # ------------------------------------------------------------------
    # 3. Service counter line in front of kiosk (south of building),
    #    10 m long with a return at each end.
    # ------------------------------------------------------------------
    counter_y = ky0 - 2.5 * s
    counter_half = 5.0 * s
    counter_d = 0.6 * s
    msp.add_lwpolyline(
        [(cx - counter_half, counter_y + counter_d),
         (cx - counter_half, counter_y),
         (cx + counter_half, counter_y),
         (cx + counter_half, counter_y + counter_d)],
        dxfattribs=_attrs(),
    )
    # Counter front edge tick marks (stool positions, 5 stools)
    for i in range(5):
        sx = cx - counter_half + (i + 0.5) * (2.0 * counter_half / 5.0)
        msp.add_circle((sx, counter_y - 0.6 * s), 0.35 * s,
                       dxfattribs=_attrs())

    # ------------------------------------------------------------------
    # 4. Terrace grid of 8 parasols (4 x 2 grid) in the southern half,
    #    each parasol: canopy circle 3.2 m dia + center post + cafe table.
    # ------------------------------------------------------------------
    parasol_r = 1.6 * s
    table_r = 0.6 * s
    grid_dx = 4.5 * s
    grid_dy = 4.5 * s
    grid_cy = cy - r * 0.35
    for row in range(2):
        for col in range(4):
            px = cx + (col - 1.5) * grid_dx
            py = grid_cy + (row - 0.5) * grid_dy
            # canopy
            msp.add_circle((px, py), parasol_r, dxfattribs=_attrs())
            # center post (small cross)
            msp.add_line((px - 0.15 * s, py), (px + 0.15 * s, py),
                         dxfattribs=_attrs())
            msp.add_line((px, py - 0.15 * s), (px, py + 0.15 * s),
                         dxfattribs=_attrs())
            # cafe table under canopy
            msp.add_circle((px, py), table_r, dxfattribs=_attrs())
            # two chairs flanking the table
            msp.add_circle((px - table_r - 0.45 * s, py), 0.3 * s,
                           dxfattribs=_attrs())
            msp.add_circle((px + table_r + 0.45 * s, py), 0.3 * s,
                           dxfattribs=_attrs())

    # ------------------------------------------------------------------
    # 5. Planter strips: two rectangular planters flanking the kiosk.
    # ------------------------------------------------------------------
    pw = 1.2 * s   # planter depth
    pl = 5.0 * s   # planter length
    for side in (-1, 1):
        px0 = cx + side * (kw / 2.0 + 1.5 * s)
        if side < 0:
            px0 -= pl
        msp.add_lwpolyline(
            [(px0, k_cy - pw / 2.0), (px0 + pl, k_cy - pw / 2.0),
             (px0 + pl, k_cy + pw / 2.0), (px0, k_cy + pw / 2.0)],
            close=True,
            dxfattribs=_attrs(),
        )
        # planting hatch: three diagonal lines inside each planter
        for i in range(1, 4):
            hx = px0 + pl * i / 4.0
            msp.add_line((hx - pw / 2.0, k_cy - pw / 2.0),
                         (hx + pw / 2.0, k_cy + pw / 2.0),
                         dxfattribs=_attrs())

    # ------------------------------------------------------------------
    # 6. Walkway centerline from door to terrace grid (dashed by segments).
    # ------------------------------------------------------------------
    walk_y0 = counter_y - 1.5 * s
    walk_y1 = grid_cy + grid_dy
    seg = 1.0 * s
    y = walk_y0
    while y - seg > walk_y1:
        msp.add_line((cx, y), (cx, y - seg), dxfattribs=_attrs())
        y -= 2.0 * seg
