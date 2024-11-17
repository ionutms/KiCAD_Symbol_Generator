"""TODO"""

from typing import Callable, Dict, NamedTuple, Tuple


class BodyDimensions(NamedTuple):
    """
    Defines rectangular dimensions for component footprint outlines.

    All measurements are in millimeters relative to the origin point (0,0).
    Positive values extend right/up, negative values extend left/down.
    """
    width_left: float     # Distance from origin to left edge
    width_right: float    # Distance from origin to right edge
    height_top: float     # Distance from origin to top edge
    height_bottom: float  # Distance from origin to bottom edge


class ConnectorSpecs(NamedTuple):
    """
    Complete specifications for generating a connector footprint.

    Defines all physical dimensions, pad properties, reference designator
    positions, and 3D model alignment parameters needed to generate a complete
    KiCad footprint file.
    """
    pitch: float   # Additional width needed per pin
    body_dimensions: BodyDimensions  # Basic rectangle dimensions
    pad_size: float       # Diameter/size of through-hole pads
    drill_size: float     # Diameter of drill holes
    silk_margin: float    # Clearance for silkscreen outlines
    mask_margin: float    # Solder mask clearance around pads
    mpn_y: float         # Y position for manufacturer part number
    ref_y: float         # Y position for reference designator
    model_offset_func: Callable  # Function to calculate model offsets


def offset_add(
        base_offset: Tuple[float, float, float],
        step_value: float
) -> Tuple[float, float, float]:
    """
    Calculate 3D model offset by adding step to base X coordinate.

    Args:
        base_offset: Starting (x, y, z) coordinates
        step_value: Value to add to x coordinate

    Returns:
        Updated (x, y, z) coordinates with modified x value
    """
    return (base_offset[0] + step_value, base_offset[1], base_offset[2])


def offset_sub(
        base_offset: Tuple[float, float, float],
        step_value: float
) -> Tuple[float, float, float]:
    """
    Calculate 3D model offset by subtracting step from base X coordinate.

    Args:
        base_offset: Starting (x, y, z) coordinates
        step_value: Value to subtract from x coordinate

    Returns:
        Updated (x, y, z) coordinates with modified x value
    """
    return (base_offset[0] - step_value, base_offset[1], base_offset[2])


CONNECTOR_SPECS: Dict[str, ConnectorSpecs] = {
    "TB004-508": ConnectorSpecs(
        pitch=5.08,
        body_dimensions=BodyDimensions(
            width_left=5.8,
            width_right=5.2,
            height_top=5.2,
            height_bottom=-5.2
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=6.096,
        ref_y=-6.096,
        model_offset_func=offset_sub
    ),
    "TB006-508": ConnectorSpecs(
        pitch=5.08,
        body_dimensions=BodyDimensions(
            width_left=5.8,
            width_right=5.2,
            height_top=4.2,
            height_bottom=-4.2
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=5.334,
        ref_y=-5.334,
        model_offset_func=offset_sub
    ),
    "TBP02R1-381": ConnectorSpecs(
        pitch=3.81,
        body_dimensions=BodyDimensions(
            width_left=4.4,
            width_right=4.4,
            height_top=-7.9,
            height_bottom=1.4
        ),
        pad_size=2.1,
        drill_size=1.4,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=-8.8,
        ref_y=2.4,
        model_offset_func=offset_add
    ),
    "TBP02R2-381": ConnectorSpecs(
        pitch=3.81,
        body_dimensions=BodyDimensions(
            width_left=4.445,
            width_right=4.445,
            height_top=3.2512,
            height_bottom=-4.445
        ),
        pad_size=2.1,
        drill_size=1.4,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=-5.4,
        ref_y=4.2,
        model_offset_func=offset_sub
    ),
    "TBP04R1-500": ConnectorSpecs(
        pitch=5.0,
        body_dimensions=BodyDimensions(
            width_left=5.2,
            width_right=5.2,
            height_top=-2.2,
            height_bottom=9.9
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=10.8,
        ref_y=-3.0,
        model_offset_func=offset_add
    ),
    "TBP04R2-500": ConnectorSpecs(
        pitch=5.0,
        body_dimensions=BodyDimensions(
            width_left=5.8,
            width_right=5.8,
            height_top=4.8,
            height_bottom=-4.0
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=-4.8,
        ref_y=5.8,
        model_offset_func=offset_add
    ),
    "TBP04R3-500": ConnectorSpecs(
        pitch=5.0,
        body_dimensions=BodyDimensions(
            width_left=5.2,
            width_right=5.2,
            height_top=4.8,
            height_bottom=-4.0
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=-4.8,
        ref_y=5.8,
        model_offset_func=offset_add
    ),
    "TBP04R12-500": ConnectorSpecs(
        pitch=5.0,
        body_dimensions=BodyDimensions(
            width_left=5.8,
            width_right=5.8,
            height_top=-2.2,
            height_bottom=9.9
        ),
        pad_size=2.55,
        drill_size=1.7,
        silk_margin=0.1524,
        mask_margin=0.102,
        mpn_y=10.8,
        ref_y=-3.0,
        model_offset_func=offset_sub
    ),
}
