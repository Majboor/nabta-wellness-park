"""CAD plan detail -- Nabta Wellness Park, Garden Room 04 "Play Dune".

Adds 2D furnishing-plan geometry inside a circular garden room:
  - 3 nested organic dune-mound contours (closed polylines, wavy radii)
  - a slide: two parallel rails from the dune crest to a run-out pad
  - a net-dome climbing feature (circle with radial tie lines)
  - a soft-fall safety-surface edge around the dune
  - stepping pods along an approach path

All coordinates derive from (center, radius) so the detail scales with
the room. Uses only msp.add_lwpolyline / add_circle / add_line on layer
NABTA-D-ROOM04.
"""

import math

LAYER = "NABTA-D-ROOM04"


def _dune_contour(cx, cy, base_r, wobble, phase, n=48):
    """Closed organic contour: radius modulated by low-frequency waves."""
    pts = []
    for i in range(n):
        a = 2.0 * math.pi * i / n
        r = base_r * (1.0
                      + wobble * math.sin(3.0 * a + phase)
                      + 0.5 * wobble * math.sin(5.0 * a - 2.0 * phase))
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def add_detail(msp, center, radius):
    cx, cy = center
    r = float(radius)
    attribs = {"layer": LAYER}

    # --- Dune mound: offset from room centre toward the north-west ---
    dune_cx = cx - 0.18 * r
    dune_cy = cy + 0.12 * r

    # 3 nested closed dune contours (organic mound levels)
    contour_specs = [
        (0.42 * r, 0.10, 0.0),   # toe of mound
        (0.28 * r, 0.13, 0.7),   # mid contour
        (0.14 * r, 0.16, 1.4),   # crest contour
    ]
    for base_r, wobble, phase in contour_specs:
        pts = _dune_contour(dune_cx, dune_cy, base_r, wobble, phase)
        msp.add_lwpolyline(pts, close=True, dxfattribs=attribs)

    # Soft-fall safety-surface edge around the dune (larger organic loop)
    soft_pts = _dune_contour(dune_cx, dune_cy, 0.55 * r, 0.07, 2.2, n=56)
    msp.add_lwpolyline(soft_pts, close=True, dxfattribs=attribs)

    # --- Slide: from crest down to a run-out pad at the south-east ---
    slide_dir = math.radians(-35.0)
    ux, uy = math.cos(slide_dir), math.sin(slide_dir)
    # perpendicular unit for rail offset
    px, py = -uy, ux
    half_w = 0.035 * r

    start_x = dune_cx + 0.10 * r * ux
    start_y = dune_cy + 0.10 * r * uy
    end_x = dune_cx + 0.62 * r * ux
    end_y = dune_cy + 0.62 * r * uy

    # Two parallel rails
    msp.add_line(
        (start_x + half_w * px, start_y + half_w * py),
        (end_x + half_w * px, end_y + half_w * py),
        dxfattribs=attribs,
    )
    msp.add_line(
        (start_x - half_w * px, start_y - half_w * py),
        (end_x - half_w * px, end_y - half_w * py),
        dxfattribs=attribs,
    )
    # Rungs across the slide (plan indication of slide bed)
    for t in (0.25, 0.5, 0.75):
        mx = start_x + t * (end_x - start_x)
        my = start_y + t * (end_y - start_y)
        msp.add_line(
            (mx + half_w * px, my + half_w * py),
            (mx - half_w * px, my - half_w * py),
            dxfattribs=attribs,
        )
    # Run-out pad at slide end (small closed polyline rectangle)
    pad_l = 0.14 * r
    pad_w = 0.09 * r
    pad_pts = [
        (end_x + pad_w * px, end_y + pad_w * py),
        (end_x - pad_w * px, end_y - pad_w * py),
        (end_x + pad_l * ux - pad_w * px, end_y + pad_l * uy - pad_w * py),
        (end_x + pad_l * ux + pad_w * px, end_y + pad_l * uy + pad_w * py),
    ]
    # order corners correctly (rectangle perimeter)
    pad_pts = [pad_pts[0], pad_pts[1], pad_pts[2], pad_pts[3]]
    msp.add_lwpolyline(
        [pad_pts[0], pad_pts[3], pad_pts[2], pad_pts[1]],
        close=True,
        dxfattribs=attribs,
    )

    # --- Net-dome climbing feature: east side of the room ---
    dome_cx = cx + 0.48 * r
    dome_cy = cy - 0.30 * r
    dome_r = 0.20 * r
    msp.add_circle((dome_cx, dome_cy), dome_r, dxfattribs=attribs)
    # Inner ring (dome apex ring in plan)
    msp.add_circle((dome_cx, dome_cy), 0.35 * dome_r, dxfattribs=attribs)
    # Radial net tie lines between inner ring and outer ring
    for k in range(8):
        a = 2.0 * math.pi * k / 8.0
        msp.add_line(
            (dome_cx + 0.35 * dome_r * math.cos(a),
             dome_cy + 0.35 * dome_r * math.sin(a)),
            (dome_cx + dome_r * math.cos(a),
             dome_cy + dome_r * math.sin(a)),
            dxfattribs=attribs,
        )

    # --- Stepping pods: curved approach path from south entry to dune ---
    n_pods = 5
    pod_r = 0.045 * r
    for i in range(n_pods):
        t = (i + 1.0) / (n_pods + 1.0)
        # sweep along an arc from the south edge toward the dune toe
        a = math.radians(-90.0) + t * math.radians(155.0)
        path_r = 0.72 * r * (1.0 - 0.35 * t)
        pod_x = cx + path_r * math.cos(a)
        pod_y = cy + path_r * math.sin(a)
        msp.add_circle((pod_x, pod_y), pod_r, dxfattribs=attribs)
