"""Nabta Wellness Park - Garden Room 08 "Wadi Garden".

2D plan furnishing detail: a meandering dry-riverbed (wadi) channel that
crosses the room, two timber bridge decks spanning the channel, boulder
clusters along the banks, a boardwalk approach polyline and stepping-stone
circles inside the wadi bed. All geometry is derived from the room's
center and radius so the detail scales with the enclosing circle.

Only msp.add_lwpolyline / msp.add_circle / msp.add_line are used, all on
layer "NABTA-D-ROOM08" (assumed to exist).
"""

import math

LAYER = "NABTA-D-ROOM08"


def _rot(px, py, cx, cy, ang):
    """Rotate point (px, py) about (cx, cy) by ang radians."""
    dx, dy = px - cx, py - cy
    c, s = math.cos(ang), math.sin(ang)
    return (cx + dx * c - dy * s, cy + dx * s + dy * c)


def add_detail(msp, center, radius):
    cx, cy = center
    r = float(radius)
    attribs = {"layer": LAYER}

    # ------------------------------------------------------------------
    # 1. Wadi channel: two sinuous bank polylines running roughly W -> E,
    #    meandering with a sine curve. Channel half-width tapers slightly.
    # ------------------------------------------------------------------
    n_pts = 24
    bank_north = []
    bank_south = []
    for i in range(n_pts + 1):
        t = i / n_pts                      # 0..1 along the channel
        x = cx + (t - 0.5) * 2.0 * r * 0.88
        # centerline meander
        y_mid = cy + 0.22 * r * math.sin(t * math.pi * 2.0)
        # channel half width, gently tapering toward the ends
        hw = r * (0.10 + 0.05 * math.sin(t * math.pi))
        bank_north.append((x, y_mid + hw))
        bank_south.append((x, y_mid - hw))
    msp.add_lwpolyline(bank_north, dxfattribs=attribs)
    msp.add_lwpolyline(bank_south, dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 2. Stepping stones inside the wadi bed (small circles on centerline)
    # ------------------------------------------------------------------
    for i in range(7):
        t = 0.15 + 0.70 * i / 6.0
        x = cx + (t - 0.5) * 2.0 * r * 0.88
        y = cy + 0.22 * r * math.sin(t * math.pi * 2.0)
        msp.add_circle((x, y), r * 0.030, dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 3. Two timber bridge decks spanning the channel (rotated rectangles
    #    with deck plank lines), at t = 0.30 and t = 0.72 along the wadi.
    # ------------------------------------------------------------------
    for t_b in (0.30, 0.72):
        bx = cx + (t_b - 0.5) * 2.0 * r * 0.88
        by = cy + 0.22 * r * math.sin(t_b * math.pi * 2.0)
        # local channel direction -> bridge crosses perpendicular to it
        slope = 0.22 * r * math.cos(t_b * math.pi * 2.0) * math.pi * 2.0 / (2.0 * r * 0.88)
        ang = math.atan2(slope, 1.0) + math.pi / 2.0  # bridge axis
        half_len = r * 0.22   # spans past both banks
        half_wid = r * 0.055  # deck width

        corners = [
            (bx - half_wid, by - half_len),
            (bx + half_wid, by - half_len),
            (bx + half_wid, by + half_len),
            (bx - half_wid, by + half_len),
        ]
        deck = [_rot(px, py, bx, by, ang - math.pi / 2.0) for px, py in corners]
        msp.add_lwpolyline(deck, close=True, dxfattribs=attribs)

        # plank lines across the deck
        n_planks = 6
        for k in range(1, n_planks):
            f = -half_len + 2.0 * half_len * k / n_planks
            p1 = _rot(bx - half_wid, by + f, bx, by, ang - math.pi / 2.0)
            p2 = _rot(bx + half_wid, by + f, bx, by, ang - math.pi / 2.0)
            msp.add_line(p1, p2, dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 4. Boulder clusters along the banks (grouped circles, varied sizes)
    # ------------------------------------------------------------------
    clusters = [
        (0.12, 1, 3),   # (t along channel, side +1 north / -1 south, count)
        (0.45, -1, 4),
        (0.60, 1, 3),
        (0.88, -1, 3),
    ]
    for t_c, side, count in clusters:
        x0 = cx + (t_c - 0.5) * 2.0 * r * 0.88
        y0 = cy + 0.22 * r * math.sin(t_c * math.pi * 2.0) + side * r * 0.24
        for k in range(count):
            a = 2.1 * k + t_c * 7.0            # deterministic pseudo-scatter
            bx = x0 + r * 0.055 * math.cos(a) * (1 + k * 0.35)
            by = y0 + r * 0.055 * math.sin(a) * (1 + k * 0.30)
            br = r * (0.028 + 0.014 * ((k * 2 + int(t_c * 10)) % 3))
            msp.add_circle((bx, by), br, dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 5. Boardwalk approach: an angled polyline path from the south rim
    #    to the first bridge, drawn as two parallel edge polylines with
    #    tie lines (deck joints).
    # ------------------------------------------------------------------
    t_b = 0.30
    bx = cx + (t_b - 0.5) * 2.0 * r * 0.88
    by = cy + 0.22 * r * math.sin(t_b * math.pi * 2.0)
    start = (cx - 0.15 * r, cy - 0.80 * r)
    knee = (cx - 0.05 * r, cy - 0.45 * r)
    end = (bx, by - 0.24 * r)
    path = [start, knee, end]
    half_w = r * 0.045

    left_edge = []
    right_edge = []
    for j, (px, py) in enumerate(path):
        # direction of the adjacent segment for offsetting
        if j < len(path) - 1:
            dx, dy = path[j + 1][0] - px, path[j + 1][1] - py
        else:
            dx, dy = px - path[j - 1][0], py - path[j - 1][1]
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d, dx / d
        left_edge.append((px + nx * half_w, py + ny * half_w))
        right_edge.append((px - nx * half_w, py - ny * half_w))
    msp.add_lwpolyline(left_edge, dxfattribs=attribs)
    msp.add_lwpolyline(right_edge, dxfattribs=attribs)

    # tie / joint lines across the boardwalk
    for seg in range(len(path) - 1):
        for k in range(1, 4):
            f = k / 4.0
            la = left_edge[seg]
            lb = left_edge[seg + 1]
            ra = right_edge[seg]
            rb = right_edge[seg + 1]
            p1 = (la[0] + (lb[0] - la[0]) * f, la[1] + (lb[1] - la[1]) * f)
            p2 = (ra[0] + (rb[0] - ra[0]) * f, ra[1] + (rb[1] - ra[1]) * f)
            msp.add_line(p1, p2, dxfattribs=attribs)

    # ------------------------------------------------------------------
    # 6. Seating boulder circle (contemplation spot) on the north side:
    #    a ring of six small boulder circles around a focal stone.
    # ------------------------------------------------------------------
    fx, fy = cx + 0.42 * r, cy + 0.52 * r
    msp.add_circle((fx, fy), r * 0.050, dxfattribs=attribs)
    for k in range(6):
        a = k * math.pi / 3.0 + 0.3
        msp.add_circle(
            (fx + r * 0.14 * math.cos(a), fy + r * 0.14 * math.sin(a)),
            r * 0.032,
            dxfattribs=attribs,
        )
