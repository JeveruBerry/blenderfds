import logging
from ..types import BFNamelistOb
from .bf_object import OP_ID, OP_FYI, OP_other
from .OP_XB import OP_XB
from .SN_MULT import OP_MULT_ID

log = logging.getLogger(__name__)


class ON_HOLE(BFNamelistOb):
    label = "HOLE"
    description = "Obstruction cutout"
    collection = "Obstacles"
    enum_id = 1009
    fds_label = "HOLE"
    bf_params = OP_ID, OP_FYI, OP_XB, OP_MULT_ID, OP_other
    bf_other = {"appearance": "WIRE"}
