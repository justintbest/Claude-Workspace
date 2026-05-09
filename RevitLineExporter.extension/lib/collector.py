from Autodesk.Revit.DB import Line, CurveElement
from pyrevit import revit


def get_selected_lines():
    selection = revit.get_selection()
    if not selection:
        raise ValueError("Nothing selected. Please select one or more lines.")

    segments = []
    for element in selection:
        if not isinstance(element, CurveElement):
            raise ValueError("All selected elements must be lines.")
        curve = element.GeometryCurve
        if not isinstance(curve, Line):
            raise ValueError("All selected curves must be straight lines.")
        segments.append(curve)

    return segments


def chain_segments(segments, tol=1e-6):
    """Order line segments end-to-end and return an ordered list of XYZ points."""
    if len(segments) == 1:
        c = segments[0]
        return [c.GetEndPoint(0), c.GetEndPoint(1)]

    # Build list of (start, end) pairs
    pairs = [(s.GetEndPoint(0), s.GetEndPoint(1)) for s in segments]
    remaining = list(range(len(pairs)))

    def close(a, b):
        return abs(a.X - b.X) < tol and abs(a.Y - b.Y) < tol

    # Start with the first segment
    chain = list(pairs[remaining.pop(0)])

    while remaining:
        matched = False
        for i in remaining:
            s, e = pairs[i]
            if close(chain[-1], s):
                chain.append(e)
                remaining.remove(i)
                matched = True
                break
            elif close(chain[-1], e):
                chain.append(s)
                remaining.remove(i)
                matched = True
                break
        if not matched:
            raise ValueError("Selected lines are not connected end-to-end.")

    # Drop duplicate closing vertex if present
    if close(chain[0], chain[-1]):
        chain = chain[:-1]

    return chain
