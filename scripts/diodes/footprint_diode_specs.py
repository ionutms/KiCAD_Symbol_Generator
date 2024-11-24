"""Specifications for diode footprint generation."""

from typing import NamedTuple


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for diode body outlines.

    All measurements are in millimeters relative to the origin point (0,0).
    """

    width: float    # Total width of diode body
    height: float   # Total height of diode body


class PadDimensionsAsymmetric(NamedTuple):
    """Defines dimensions for asymmetric diode pads.

    All measurements are in millimeters. For PowerDI-123 package,
    cathode_pad is pad 1, anode_pad is pad 2.

    """

    cathode_width: float    # Width of cathode pad (pad 1)
    cathode_height: float   # Height of cathode pad
    anode_width: float      # Width of anode pad (pad 2)
    anode_height: float     # Height of anode pad
    center_x: float         # Distance from center to pad center


class DiodeSpecs(NamedTuple):
    """Complete specifications for generating a diode footprint.

    Defines all physical dimensions, pad properties, and reference designator
    positions needed to generate a complete KiCad footprint file.
    """

    body_dimensions: BodyDimensions
    pad_dimensions: PadDimensionsAsymmetric
    ref_offset_y: float


DIODE_SPECS: dict[str, DiodeSpecs] = {
    # PowerDI-123 package specs for DFLS1200Q-7
    "PowerDI-123": DiodeSpecs(
        body_dimensions=BodyDimensions(
            width=2.90,    # Body width
            height=1.95,   # Body height
        ),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=1.20,     # Cathode (pad 1) width
            cathode_height=1.80,    # Cathode height
            anode_width=0.95,       # Anode (pad 2) width
            anode_height=1.40,      # Anode height
            center_x=1.35,          # Center to pad distance
        ),
        ref_offset_y=-2.5,
    ),
}
