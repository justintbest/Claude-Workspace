def serialize_aline(element, curve, name):
    start = curve.GetEndPoint(0)
    end = curve.GetEndPoint(1)
    return {
        "name": name,
        "closed": False,
        "points": [
            {"x": start.X, "y": start.Y},
            {"x": end.X,   "y": end.Y},
        ],
    }
