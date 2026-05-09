FEET_TO_INCHES = 12.0

def serialize_aline(points, name, closed):
    return {
        "name": name,
        "closed": closed,
        "points": [{"x": p.X * FEET_TO_INCHES, "y": p.Y * FEET_TO_INCHES} for p in points],
    }
