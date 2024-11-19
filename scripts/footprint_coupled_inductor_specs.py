"""Specifications for inductor footprint generation."""

from typing import Dict, NamedTuple


class BodyDimensions(NamedTuple):
    """
    Defines rectangular dimensions for inductor body outlines.

    All measurements are in millimeters relative to the origin point (0,0).
    """
    width: float   # Total width of inductor body
    height: float  # Total height of inductor body


class PadDimensions(NamedTuple):
    """
    Defines dimensions for inductor pads.

    All measurements are in millimeters.
    """
    width: float        # Width of each pad
    height: float       # Height of each pad
    center_x: float     # Distance from origin to pad center on X axis


class InductorSpecs(NamedTuple):
    """
    Complete specifications for generating an inductor footprint.

    Defines all physical dimensions, pad properties, and reference designator
    positions needed to generate a complete KiCad footprint file.
    """
    body_dimensions: BodyDimensions  # Basic rectangle dimensions
    pad_dimensions: PadDimensions   # Pad size and positioning
    ref_offset_y: float            # Y offset for reference designator


INDUCTOR_SPECS: Dict[str, InductorSpecs] = {
    "XAL1010": InductorSpecs(
        body_dimensions=BodyDimensions(
            width=10.922,
            height=12.192
        ),
        pad_dimensions=PadDimensions(
            width=2.3876,
            height=8.9916,
            center_x=3.3274
        ),
        ref_offset_y=-6.858
    ),
}
