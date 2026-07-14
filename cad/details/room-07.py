"""Nabta Wellness Park - Garden Room 07 "Picnic Groves"
2D plan furnishing detail: five picnic grove pockets arranged on a
quincunx inside the room circle. Each pocket has a picnic table
(rectangle), four seat squares, and a grove canopy circle. Pockets
are linked back to the room centre by path lines.

All geometry is scaled from (center, radius) so the detail fits any
room size. Entities are placed on layer NABTA-D-ROOM07.
"""

import math

LAYER = "NABTA-D-ROOM07"


def _rot(px, py, ang):
    """Rotate point (px, py) about origin by ang radians."""
    c = math.cos(ang)
    s = math.sin(ang)
    return px * c - py * s, px * s + py * c


def _closed_rect(msp, cx, cy, hw, hh, ang):
    """Add a closed lwpolyline rectangle centred at (cx, cy),
    half-width hw, half-height hh, rotated by ang radians."""
    corners = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
    pts = []
    for px, py in corners:
        rx, ry = _rot(px, py, ang)
        pts.append((cx + rx, cy + ry))
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": LAYER})


def _grove_pocket(msp, cx, cy, r, ang):
    """One picnic grove pocket at (cx, cy), scaled by room radius r,
    rotated so the table long axis faces angle ang."""
    # Canopy circle enclosing the pocket (tree grove edge)
    canopy = 0.24 * r
    msp.add_circle((cx, cy), canopy, dxfattribs={"layer": LAYER})

    # Picnic table: long rectangle
    t_hw = 0.11 * r   # half length of table
    t_hh = 0.045 * r  # half width of table
    _closed_rect(msp, cx, cy, t_hw, t_hh, ang)

    # Four seat squares: two along each long side of the table
    seat = 0.035 * r          # half-size of seat square
    seat_off = t_hh + 0.055 * r  # offset from table centreline
    seat_dx = 0.055 * r          # spacing along table length
    for sx in (-seat_dx, seat_dx):
        for sy in (-seat_off, seat_off):
            rx, ry = _rot(sx, sy, ang)
            _closed_rect(msp, cx + rx, cy + ry, seat, seat, ang)


def add_detail(msp, center, radius):
    """Add Picnic Groves plan detail inside circle (center, radius)."""
    cx, cy = center
    r = radius

    # Quincunx layout: one central pocket + four diagonal pockets
    ring = 0.58 * r
    pockets = [(cx, cy, 0.0)]
    for k in range(4):
        ang = math.radians(45.0 + 90.0 * k)
        px = cx + ring * math.cos(ang)
        py = cy + ring * math.sin(ang)
        # Rotate each outer table tangent to its radial direction
        pockets.append((px, py, ang + math.pi / 2.0))

    for px, py, ang in pockets:
        _grove_pocket(msp, px, py, r, ang)

    # Path spokes from central pocket edge to each outer pocket edge
    canopy = 0.24 * r
    for k in range(4):
        ang = math.radians(45.0 + 90.0 * k)
        ca = math.cos(ang)
        sa = math.sin(ang)
        start = (cx + canopy * ca, cy + canopy * sa)
        end = (cx + (ring - canopy) * ca, cy + (ring - canopy) * sa)
        msp.add_line(start, end, dxfattribs={"layer": LAYER})

    # Perimeter strolling path ring just inside the room edge
    msp.add_circle((cx, cy), 0.92 * r, dxfattribs={"layer": LAYER})
