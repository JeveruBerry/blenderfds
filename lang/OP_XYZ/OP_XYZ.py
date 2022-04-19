import logging
from bpy.types import Object
from bpy.props import EnumProperty, BoolProperty, FloatProperty
from ...config import LENGTH_PRECISION
from ...types import BFParam, FDSParam, FDSList, FDSMulti
from ... import utils
from .ob_to_xyzs import ob_to_xyzs
from .xyzs_to_ob import xyzs_to_ob

log = logging.getLogger(__name__)


def update_bf_xyz(ob, context):
    utils.geometry.rm_geometric_cache(ob=ob)
    if ob.bf_has_tmp:
        utils.geometry.rm_tmp_objects()
    # Prevent double multiparam
    if ob.bf_xyz == "VERTICES" and ob.bf_xyz_export:
        if ob.bf_xb in ("VOXELS", "FACES", "PIXELS", "EDGES"):
            ob.bf_xb_export = False
        if ob.bf_pb == "PLANES":
            ob.bf_pb_export = False
        return


class OP_XYZ_export(BFParam):
    label = "Export XYZ"
    description = "Set if XYZ shall be exported to FDS"
    bpy_type = Object
    bpy_idname = "bf_xyz_export"
    bpy_prop = BoolProperty
    bpy_default = False
    bpy_other = {"update": update_bf_xyz}


class OP_XYZ(BFParam):
    label = "XYZ"
    description = "Export as points"
    fds_label = "XYZ"
    bpy_type = Object
    bpy_idname = "bf_xyz"
    bpy_prop = EnumProperty
    bpy_other = {
        "update": update_bf_xyz,
        "items": (
            ("CENTER", "Center", "Point, center point of this object", 100),
            ("VERTICES", "Vertices", "Points, one for each vertex of this object", 200),
        ),
    }
    bpy_export = "bf_xyz_export"

    def to_fds_list(self, context) -> FDSList:
        # Get geometry
        ob, hids, xyzs, msgs, lp = self.element, tuple(), tuple(), tuple(), LENGTH_PRECISION
        if ob.bf_xyz_export:
            hids, xyzs, msgs = ob_to_xyzs(context=context, ob=ob, bf_xyz=ob.bf_xyz)
        # Single
        match len(xyzs):
            case 0:
                return FDSList()
            case 1:
                return FDSParam(fds_label="XYZ", value=xyzs[0], precision=lp)
        # Multi
        return FDSMulti(
            iterable=(
                (FDSParam(fds_label="ID", value=hid) for hid in hids),
                (FDSParam(fds_label="XYZ", value=xyz, precision=lp) for xyz in xyzs),
            ),
            msgs=msgs,
        )

    def from_fds(self, context, value):
        bf_xyz = xyzs_to_ob(
            context=context,
            ob=self.element,
            xyzs=(value,),
            set_origin=True,
            add=True,
        )
        self.element.bf_xyz = bf_xyz
        self.element.bf_xyz_export = True


class OP_XYZ_center(OP_XYZ):
    description = "Export as points (center)"
    bpy_prop = None  # do not redefine
    bf_xyz_idxs = (0,)  # CENTER, VERTICES
