def serialize_aline(points, name, closed):
    return {
        "name": name,
        "closed": closed,
        "points": [{"x": p.X, "y": p.Y} for p in points],
    }
