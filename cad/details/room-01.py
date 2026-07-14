"""NABTA Wellness Park - Garden Room 01 "Entry Plaza" plan detail.

Furnishing plan geometry drawn inside the room circle:
  - Gateway pergola: double row of 12 square posts (0.4 m) flanking the
    main entry axis, with pergola edge beams.
  - Central paving band: axis walkway with transverse paving joint lines.
  - Bike rack row: 6 U-racks (hoops) near the plaza edge.
  - Central welcome feature: circular planter/fountain rings.
  - Two flanking bench pairs.

All coordinates derive from (center, radius) so the detail scales with
the room. Layer "NABTA-D-ROOM01" is assumed to exist.
"""

import math

LAYER = "NABTA-D-ROOM01"


def _rect(msp, cx, cy, w, h):
    """Closed rectangle centered at (cx, cy)."""
    hw, hh = w / 2.0, h / 2.0
    pts = [
        (cx - hw, cy - hh),
        (cx + hw, cy - hh),
        (cx + hw, cy + hh),
        (cx - hw, cy + hh),
    ]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": LAYER})


def add_detail(msp, center, radius):
    cx, cy = center
    r = float(radius)
    attribs = {"layer": LAYER}

    # ------------------------------------------------------------------
    # 1. Central paving band (entry axis walkway, running south -> north)
    # ------------------------------------------------------------------
    band_hw = 0.18 * r                 # half-width of the paving band
    band_y0 = cy - 0.92 * r            # start (near south rim)
    band_y1 = cy + 0.92 * r            # end (near north rim)

    # Band edge lines
    msp.add_line((cx - band_hw, band_y0), (cx - band_hw, band_y1),
                 dxfattribs=attribs)
    msp.add_line((cx + band_hw, band_y0), (cx + band_hw, band_y1),
                 dxfattribs=attribs)

    # Transverse paving joint lines every ~0.13*r along the band,
    # skipping the central feature zone.
    feature_r = 0.24 * r
    n_joints = 14
    for i in range(n_joints + 1):
        jy = band_y0 + (band_y1 - band_y0) * i / n_joints
        if abs(jy - cy) < feature_r + 0.03 * r:
            continue  # keep the central feature clear
        msp.add_line((cx - band_hw, jy), (cx + band_hw, jy),
                     dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 2. Gateway pergola: double row of 12 posts (0.4 m squares),
    #    6 per side, flanking the paving band on the south half.
    # ------------------------------------------------------------------
    post = 0.4                          # post size in meters (fixed detail)
    row_off = band_hw + 0.10 * r        # row offset from axis
    perg_y0 = cy - 0.85 * r             # pergola run start
    perg_y1 = cy - 0.30 * r             # pergola run end
    n_per_row = 6
    for i in range(n_per_row):
        py = perg_y0 + (perg_y1 - perg_y0) * i / (n_per_row - 1)
        _rect(msp, cx - row_off, py, post, post)   # west row post
        _rect(msp, cx + row_off, py, post, post)   # east row post

    # Pergola edge beams (dashed effect via outer beam lines)
    beam_off = row_off + post / 2.0 + 0.02 * r
    msp.add_line((cx - beam_off, perg_y0 - post), (cx - beam_off, perg_y1 + post),
                 dxfattribs=attribs)
    msp.add_line((cx + beam_off, perg_y0 - post), (cx + beam_off, perg_y1 + post),
                 dxfattribs=attribs)
    # Cross beams over the walkway at each post pair
    for i in range(n_per_row):
        py = perg_y0 + (perg_y1 - perg_y0) * i / (n_per_row - 1)
        msp.add_line((cx - beam_off, py), (cx + beam_off, py),
                     dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 3. Central welcome feature: planter / fountain rings on axis
    # ------------------------------------------------------------------
    msp.add_circle((cx, cy), feature_r, dxfattribs=attribs)
    msp.add_circle((cx, cy), 0.16 * r, dxfattribs=attribs)
    msp.add_circle((cx, cy), 0.06 * r, dxfattribs=attribs)
    # Radial paving score lines around the feature
    for k in range(8):
        a = math.pi / 8.0 + k * math.pi / 4.0
        x0 = cx + 0.16 * r * math.cos(a)
        y0 = cy + 0.16 * r * math.sin(a)
        x1 = cx + feature_r * math.cos(a)
        y1 = cy + feature_r * math.sin(a)
        msp.add_line((x0, y0), (x1, y1), dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 4. Bike rack row: 6 U-racks (plan hoops) on the east side,
    #    aligned parallel to the axis, with a rack pad outline.
    # ------------------------------------------------------------------
    rack_x = cx + 0.55 * r
    rack_y0 = cy - 0.05 * r
    rack_y1 = cy + 0.55 * r
    n_racks = 6
    hoop_r = 0.035 * r
    for i in range(n_racks):
        ry = rack_y0 + (rack_y1 - rack_y0) * i / (n_racks - 1)
        msp.add_circle((rack_x, ry), hoop_r, dxfattribs=attribs)
        # rack bar tick through each hoop (perpendicular to row)
        msp.add_line((rack_x - 2.2 * hoop_r, ry), (rack_x + 2.2 * hoop_r, ry),
                     dxfattribs=attribs)
    # Rack pad outline
    pad_pts = [
        (rack_x - 0.10 * r, rack_y0 - 0.08 * r),
        (rack_x + 0.10 * r, rack_y0 - 0.08 * r),
        (rack_x + 0.10 * r, rack_y1 + 0.08 * r),
        (rack_x - 0.10 * r, rack_y1 + 0.08 * r),
    ]
    msp.add_lwpolyline(pad_pts, close=True, dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 5. Bench pairs: two benches on the west side facing the axis
    # ------------------------------------------------------------------
    bench_x = cx - 0.55 * r
    bench_w = 0.06 * r      # bench depth (plan)
    bench_l = 0.22 * r      # bench length
    for by in (cy + 0.15 * r, cy + 0.45 * r):
        pts = [
            (bench_x - bench_w / 2.0, by - bench_l / 2.0),
            (bench_x + bench_w / 2.0, by - bench_l / 2.0),
            (bench_x + bench_w / 2.0, by + bench_l / 2.0),
            (bench_x - bench_w / 2.0, by + bench_l / 2.0),
        ]
        msp.add_lwpolyline(pts, close=True, dxfattribs=attribs)
        # seat plank line
        msp.add_line((bench_x, by - bench_l / 2.0), (bench_x, by + bench_l / 2.0),
                     dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 6. Plaza edge paving arc ticks (radial score marks near the rim)
    # ------------------------------------------------------------------
    for k in range(24):
        a = k * math.pi / 12.0
        x0 = cx + 0.88 * r * math.cos(a)
        y0 = cy + 0.88 * r * math.sin(a)
        x1 = cx + 0.96 * r * math.cos(a)
        y1 = cy + 0.96 * r * math.sin(a)
        # keep ticks off the paving band opening at south and north
        if abs(x0 - cx) < band_hw and abs(x1 - cx) < band_hw:
            continue
        msp.add_line((x0, y0), (x1, y1), dxfattribs=attribs)
