from Autodesk.Revit.DB import Line, CurveElement
from pyrevit import revit

def get_selected_line():
    selection = revit.get_selection()
    if not selection:
        raise ValueError("Nothing selected. Please select a line.")

    element = selection[0]

    if not isinstance(element, CurveElement):
        raise ValueError("Selected element is not a line.")

    curve = element.GeometryCurve
    if not isinstance(curve, Line):
        raise ValueError("Selected curve is not a straight line.")

    return element, curve
