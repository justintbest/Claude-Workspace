def serialize_aline(element, curve, name):
    start = curve.GetEndPoint(0)
    end = curve.GetEndPoint(1)
    mid_x = (start.X + end.X) / 2.0
    mid_y = (start.Y + end.Y) / 2.0
    return {
        "name": name,
        "closed": False,
        "points": [
            {"x": start.X, "y": start.Y},
            {"x": mid_x,   "y": mid_y},
            {"x": end.X,   "y": end.Y},
        ],
    }
