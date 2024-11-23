"""Specifications for diode footprint generation."""

from typing import Dict, NamedTuple


class BodyDimensions(NamedTuple):
    """
    Defines rectangular dimensions for diode body outlines.

    All measurements are in millimeters relative to the origin point (0,0).
    """
    width: float    # Total width of diode body
    height: float   # Total height of diode body


class PadDimensions(NamedTuple):
    """
    Defines dimensions for diode pads.

    All measurements are in millimeters.
    """
    width: float        # Width of each pad
    height: float       # Height of each pad
    center_x: float     # Distance from origin to pad center on X axis
    thermal_width: float = 0.0    # Width of optional thermal pad (0 if none)
    thermal_height: float = 0.0   # Height of optional thermal pad (0 if none)


class DiodeSpecs(NamedTuple):
    """
    Complete specifications for generating a diode footprint.

    Defines all physical dimensions, pad properties, and reference designator
    positions needed to generate a complete KiCad footprint file.
    """
    body_dimensions: BodyDimensions  # Basic rectangle dimensions
    pad_dimensions: PadDimensions   # Pad size and positioning
    ref_offset_y: float            # Y offset for reference designator
    has_thermal_pad: bool = False  # Whether the package includes a thermal pad


DIODE_SPECS: Dict[str, DiodeSpecs] = {
    # Example PowerDI-123 package
    "PowerDI-123": DiodeSpecs(
        body_dimensions=BodyDimensions(
            width=3.0,
            height=2.0
        ),
        pad_dimensions=PadDimensions(
            width=1.0,
            height=1.2,
            center_x=1.15,
            thermal_width=1.8,
            thermal_height=1.2
        ),
        ref_offset_y=-2.5,
        has_thermal_pad=True
    ),
    # Example SOD-123 package
    "SOD-123": DiodeSpecs(
        body_dimensions=BodyDimensions(
            width=2.85,
            height=1.8
        ),
        pad_dimensions=PadDimensions(
            width=1.0,
            height=1.2,
            center_x=1.635
        ),
        ref_offset_y=-2.0
    ),
}
