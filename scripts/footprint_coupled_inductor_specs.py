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
    pitch_y: float      # Vertical distance between pads


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
    "MSD7342": InductorSpecs(
        body_dimensions=BodyDimensions(
            width=7.7,
            height=7.7
        ),
        pad_dimensions=PadDimensions(
            width=2.1,
            height=1.1,
            center_x=2.7,
            pitch_y=1.7,
        ),
        ref_offset_y=-4.826,
    ),
    "MSD1048": InductorSpecs(
        body_dimensions=BodyDimensions(
            width=10.5,
            height=10.5
        ),
        pad_dimensions=PadDimensions(
            width=2.4,
            height=1.25,
            center_x=3.9,
            pitch_y=2.05,
        ),
        ref_offset_y=-6.096,
    ),
}
