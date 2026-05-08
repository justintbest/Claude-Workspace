"""
Fractal Snowflake — Geometry Nodes setup
Run this in Blender's Scripting workspace (Run Script).
Tested on Blender 3.3 LTS, 3.6 LTS, 4.0, 4.1, 4.2.

Node ID reference used (all verified):
  GeometryNodeCurvePrimitiveLine   <- curve line (NOT GeometryNodeCurveLine)
  GeometryNodeSubdivideCurve
  GeometryNodeCurveToPoints
  GeometryNodeCurveToMesh
  GeometryNodeInstanceOnPoints
  GeometryNodeRealizeInstances
  GeometryNodeJoinGeometry
  GeometryNodeMeshCircle
  GeometryNodeMergeByDistance
  GeometryNodeSetMaterial
  GeometryNodeInputIndex
  ShaderNodeMath
  ShaderNodeCombineXYZ
  NodeGroupInput / NodeGroupOutput
"""

import bpy
import math

# ---- Config -----------------------------------------------------------------
ARM_LENGTH   = 1.0    # length of each main arm
BRANCH_SCALE = 0.38   # sub-branch length relative to parent
BRANCH_ANGLE = 60.0   # degrees each sub-branch splays out
ARM_SUBDIV   = 3      # subdivision cuts on main arm
SUB_SUBDIV   = 2      # subdivision cuts on sub-arms
# -----------------------------------------------------------------------------


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for ng in list(bpy.data.node_groups):
        bpy.data.node_groups.remove(ng)


def new_object(name):
    mesh = bpy.data.meshes.new(name)
    obj  = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    return obj


def add_geo_nodes(obj, name):
    mod = obj.modifiers.new(name=name, type='NODES')
    ng  = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    mod.node_group = ng
    return ng, mod


def add_io(ng):
    """Add group input/output sockets — handles Blender 3.x and 4.x."""
    try:
        ng.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
        ng.interface.new_socket("Geometry", in_out='INPUT',  socket_type='NodeSocketGeometry')
    except AttributeError:
        ng.outputs.new('NodeSocketGeometry', "Geometry")
        ng.inputs.new('NodeSocketGeometry',  "Geometry")


def N(ng, idname, loc, **props):
    n = ng.nodes.new(idname)
    n.location = loc
    for k, v in props.items():
        if hasattr(n, k):
            setattr(n, k, v)
    return n


def L(ng, a, ao, b, bi):
    ng.links.new(a.outputs[ao], b.inputs[bi])


def curve_line(ng, loc, start, end):
    """GeometryNodeCurvePrimitiveLine — correct ID for all Blender versions."""
    n = N(ng, 'GeometryNodeCurvePrimitiveLine', loc)
    n.inputs['Start'].default_value = start
    n.inputs['End'].default_value   = end
    return n


def math_node(ng, loc, operation, val_a=None, val_b=None):
    n = N(ng, 'ShaderNodeMath', loc, operation=operation)
    if val_a is not None: n.inputs[0].default_value = val_a
    if val_b is not None: n.inputs[1].default_value = val_b
    return n


def combine_xyz(ng, loc, x=0.0, y=0.0, z=0.0):
    n = N(ng, 'ShaderNodeCombineXYZ', loc)
    n.inputs['X'].default_value = x
    n.inputs['Y'].default_value = y
    n.inputs['Z'].default_value = z
    return n


def make_arm(ng, arm_len, branch_len, arm_subdiv, sub_subdiv, angle_deg, col_offset):
    """
    Build one arm of the snowflake with 2 levels of sub-branches.
    Returns the JoinGeometry node whose Geometry output is the full arm.
    """
    cx, cy = col_offset
    ang = math.radians(angle_deg)

    # Main arm
    arm_c   = curve_line(ng, (cx, cy+400), (0,0,0), (0, arm_len, 0))
    arm_sdv = N(ng, 'GeometryNodeSubdivideCurve', (cx+160, cy+400))
    arm_sdv.inputs['Cuts'].default_value = arm_subdiv
    L(ng, arm_c, 'Curve', arm_sdv, 'Curve')

    arm_pts = N(ng, 'GeometryNodeCurveToPoints', (cx+320, cy+400))
    arm_pts.mode = 'EVALUATED'
    L(ng, arm_sdv, 'Curve', arm_pts, 'Curve')

    arm_mesh = N(ng, 'GeometryNodeCurveToMesh', (cx+320, cy+550))
    L(ng, arm_sdv, 'Curve', arm_mesh, 'Curve')

    # Level-1 sub-branch geometry
    sub_c    = curve_line(ng, (cx, cy+200), (0,0,0), (0, branch_len, 0))
    sub_sdv  = N(ng, 'GeometryNodeSubdivideCurve', (cx+160, cy+200))
    sub_sdv.inputs['Cuts'].default_value = sub_subdiv
    L(ng, sub_c, 'Curve', sub_sdv, 'Curve')

    sub_pts  = N(ng, 'GeometryNodeCurveToPoints', (cx+320, cy+200))
    sub_pts.mode = 'EVALUATED'
    L(ng, sub_sdv, 'Curve', sub_pts, 'Curve')

    sub_mesh = N(ng, 'GeometryNodeCurveToMesh', (cx+160, cy+50))
    L(ng, sub_c, 'Curve', sub_mesh, 'Curve')

    # Instance at +angle
    rot_p = combine_xyz(ng, (cx+320, cy+50), z=ang)
    iop_p = N(ng, 'GeometryNodeInstanceOnPoints', (cx+480, cy+200))
    L(ng, arm_pts,  'Points',   iop_p, 'Points')
    L(ng, sub_mesh, 'Mesh',     iop_p, 'Instance')
    L(ng, rot_p,    'Vector',   iop_p, 'Rotation')

    # Instance at -angle
    rot_n = combine_xyz(ng, (cx+320, cy-50), z=-ang)
    iop_n = N(ng, 'GeometryNodeInstanceOnPoints', (cx+480, cy+50))
    L(ng, arm_pts,  'Points',   iop_n, 'Points')
    L(ng, sub_mesh, 'Mesh',     iop_n, 'Instance')
    L(ng, rot_n,    'Vector',   iop_n, 'Rotation')

    real_p = N(ng, 'GeometryNodeRealizeInstances', (cx+640, cy+200))
    L(ng, iop_p, 'Instances', real_p, 'Geometry')
    real_n = N(ng, 'GeometryNodeRealizeInstances', (cx+640, cy+50))
    L(ng, iop_n, 'Instances', real_n, 'Geometry')

    # Level-2 sub-sub-branch geometry
    sub2_len  = branch_len * BRANCH_SCALE
    sub2_c    = curve_line(ng, (cx, cy-200), (0,0,0), (0, sub2_len, 0))
    sub2_mesh = N(ng, 'GeometryNodeCurveToMesh', (cx+160, cy-200))
    L(ng, sub2_c, 'Curve', sub2_mesh, 'Curve')

    rot_p2 = combine_xyz(ng, (cx+320, cy-200), z= ang)
    rot_n2 = combine_xyz(ng, (cx+320, cy-320), z=-ang)

    iop_p2 = N(ng, 'GeometryNodeInstanceOnPoints', (cx+480, cy-200))
    L(ng, sub_pts,   'Points',   iop_p2, 'Points')
    L(ng, sub2_mesh, 'Mesh',     iop_p2, 'Instance')
    L(ng, rot_p2,    'Vector',   iop_p2, 'Rotation')

    iop_n2 = N(ng, 'GeometryNodeInstanceOnPoints', (cx+480, cy-320))
    L(ng, sub_pts,   'Points',   iop_n2, 'Points')
    L(ng, sub2_mesh, 'Mesh',     iop_n2, 'Instance')
    L(ng, rot_n2,    'Vector',   iop_n2, 'Rotation')

    real_p2 = N(ng, 'GeometryNodeRealizeInstances', (cx+640, cy-200))
    L(ng, iop_p2, 'Instances', real_p2, 'Geometry')
    real_n2 = N(ng, 'GeometryNodeRealizeInstances', (cx+640, cy-320))
    L(ng, iop_n2, 'Instances', real_n2, 'Geometry')

    # Join everything
    join = N(ng, 'GeometryNodeJoinGeometry', (cx+800, cy+200))
    L(ng, arm_mesh, 'Mesh',     join, 'Geometry')
    L(ng, real_p,   'Geometry', join, 'Geometry')
    L(ng, real_n,   'Geometry', join, 'Geometry')
    L(ng, real_p2,  'Geometry', join, 'Geometry')
    L(ng, real_n2,  'Geometry', join, 'Geometry')

    return join


def build(ng):
    N(ng, 'NodeGroupInput',  (-200, 0))
    gOut = N(ng, 'NodeGroupOutput', (2100, 200))

    branch_len = ARM_LENGTH * BRANCH_SCALE

    arm_join = make_arm(
        ng,
        arm_len    = ARM_LENGTH,
        branch_len = branch_len,
        arm_subdiv = ARM_SUBDIV,
        sub_subdiv = SUB_SUBDIV,
        angle_deg  = BRANCH_ANGLE,
        col_offset = (-100, 0),
    )

    # 6-fold symmetry — 6 points at origin, each arm rotated index * 60deg
    six_pts = N(ng, 'GeometryNodeMeshCircle', (1000, 200))
    six_pts.inputs['Vertices'].default_value = 6
    six_pts.inputs['Radius'].default_value   = 0.0001

    idx = N(ng, 'GeometryNodeInputIndex', (1000, 0))
    mul = math_node(ng, (1150, 0), 'MULTIPLY', val_b=math.tau / 6.0)
    L(ng, idx, 'Index', mul, 0)

    rot6 = combine_xyz(ng, (1300, 0))
    L(ng, mul, 'Value', rot6, 'Z')

    iop6 = N(ng, 'GeometryNodeInstanceOnPoints', (1450, 200))
    L(ng, six_pts,  'Mesh',     iop6, 'Points')
    L(ng, arm_join, 'Geometry', iop6, 'Instance')
    L(ng, rot6,     'Vector',   iop6, 'Rotation')

    real_all = N(ng, 'GeometryNodeRealizeInstances', (1600, 200))
    L(ng, iop6, 'Instances', real_all, 'Geometry')

    merge = N(ng, 'GeometryNodeMergeByDistance', (1750, 200))
    merge.inputs['Distance'].default_value = 0.001
    L(ng, real_all, 'Geometry', merge, 'Geometry')

    setm = N(ng, 'GeometryNodeSetMaterial', (1900, 200))
    L(ng, merge, 'Geometry', setm, 'Geometry')

    L(ng, setm, 'Geometry', gOut, 'Geometry')

    print("Fractal Snowflake built successfully!")
    print(f"  6 arms | angle={BRANCH_ANGLE} | scale={BRANCH_SCALE} | arm={ARM_LENGTH}")
    print("Tips:")
    print("  Add a Solidify modifier for thickness")
    print("  Add a Wireframe modifier for line-art look")
    print("  Tweak ARM_LENGTH, BRANCH_SCALE, BRANCH_ANGLE at top of file")


# ---- Main -------------------------------------------------------------------
clear_scene()
obj     = new_object("FractalSnowflake")
ng, mod = add_geo_nodes(obj, "FractalSnowflake")
add_io(ng)
build(ng)

bpy.context.view_layer.objects.active = obj
obj.select_set(True)
