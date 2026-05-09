def serialize_line(element, curve):
    start = curve.GetEndPoint(0)
    end = curve.GetEndPoint(1)

    return {
        "element_id": element.Id.IntegerValue,
        "start": {"x": start.X, "y": start.Y, "z": start.Z},
        "end":   {"x": end.X,   "y": end.Y,   "z": end.Z}
    }
