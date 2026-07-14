import math

LAYER = "NABTA-D-ROOM03"


def add_detail(msp, center, radius):
    """Garden room 03 'Event Lawn' plan detail for Nabta Wellness Park.

    Adds 2D furnishing geometry inside the room circle at *center* (x, y)
    with radius *radius* (meters), all on layer NABTA-D-ROOM03:

    - Oval lawn edge (elliptical polyline approximated with vertices)
    - Stage pad rectangle tucked against the north rim, with a front-edge
      apron line
    - 4 kiosk pads (small squares with a center marker circle) spaced on
      the east / south-east / south-west / west rim band
    - Two crossing mow-path lines through the lawn oval
    """
    cx, cy = center
    r = float(radius)
    attribs = {"layer": LAYER}

    # ------------------------------------------------------------------
    # 1. Oval lawn edge — ellipse approximated as a closed lwpolyline
    #    Semi-axes: 0.62 r (east-west) x 0.45 r (north-south),
    #    center pushed slightly south to leave room for the stage.
    # ------------------------------------------------------------------
    lawn_cx = cx
    lawn_cy = cy - 0.08 * r
    a = 0.62 * r  # semi-major (x)
    b = 0.45 * r  # semi-minor (y)
    n = 48
    lawn_pts = []
    for i in range(n):
        t = 2.0 * math.pi * i / n
        lawn_pts.append((lawn_cx + a * math.cos(t), lawn_cy + b * math.sin(t)))
    msp.add_lwpolyline(lawn_pts, close=True, dxfattribs=attribs)

    # Inner mow ring, offset 0.06 r inside the lawn edge
    ring_pts = []
    for i in range(n):
        t = 2.0 * math.pi * i / n
        ring_pts.append((lawn_cx + (a - 0.06 * r) * math.cos(t),
                         lawn_cy + (b - 0.06 * r) * math.sin(t)))
    msp.add_lwpolyline(ring_pts, close=True, dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 2. Stage pad rectangle at the north rim
    #    Width 0.50 r, depth 0.22 r, top edge at 0.85 r north of center.
    # ------------------------------------------------------------------
    sw = 0.50 * r   # stage width
    sd = 0.22 * r   # stage depth
    s_top = cy + 0.85 * r
    s_bot = s_top - sd
    s_lft = cx - 0.5 * sw
    s_rgt = cx + 0.5 * sw
    msp.add_lwpolyline(
        [(s_lft, s_bot), (s_rgt, s_bot), (s_rgt, s_top), (s_lft, s_top)],
        close=True,
        dxfattribs=attribs,
    )
    # Stage apron / front-of-stage line, slightly wider than the pad
    apron_y = s_bot - 0.03 * r
    msp.add_line(
        (s_lft - 0.05 * r, apron_y),
        (s_rgt + 0.05 * r, apron_y),
        dxfattribs=attribs,
    )
    # Two stair stubs flanking the stage front
    for sx in (s_lft - 0.02 * r, s_rgt + 0.02 * r):
        msp.add_line((sx, s_bot), (sx, apron_y), dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 3. Four kiosk pads on the rim band (E, SE, SW, W), each a square
    #    of side 0.14 r with a small service marker circle at its center.
    # ------------------------------------------------------------------
    kiosk_half = 0.07 * r
    kiosk_ring = 0.78 * r
    for ang_deg in (0.0, 315.0, 225.0, 180.0):  # E, SE, SW, W
        t = math.radians(ang_deg)
        kx = cx + kiosk_ring * math.cos(t)
        ky = cy + kiosk_ring * math.sin(t)
        msp.add_lwpolyline(
            [
                (kx - kiosk_half, ky - kiosk_half),
                (kx + kiosk_half, ky - kiosk_half),
                (kx + kiosk_half, ky + kiosk_half),
                (kx - kiosk_half, ky + kiosk_half),
            ],
            close=True,
            dxfattribs=attribs,
        )
        msp.add_circle((kx, ky), 0.03 * r, dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 4. Crossing mow-path lines through the lawn oval (subtle plan
    #    texture indicating maintained event turf).
    # ------------------------------------------------------------------
    msp.add_line(
        (lawn_cx - 0.55 * a, lawn_cy - 0.55 * b),
        (lawn_cx + 0.55 * a, lawn_cy + 0.55 * b),
        dxfattribs=attribs,
    )
    msp.add_line(
        (lawn_cx - 0.55 * a, lawn_cy + 0.55 * b),
        (lawn_cx + 0.55 * a, lawn_cy - 0.55 * b),
        dxfattribs=attribs,
    )
