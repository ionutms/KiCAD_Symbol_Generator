"""Specifications for diode footprint generation."""

from typing import NamedTuple


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for diode body outlines.

    All measurements are in millimeters relative to the origin point (0,0).
    """

    width: float    # Total width of diode body
    height: float   # Total height of diode body


class PadDimensions(NamedTuple):
    """Defines dimensions for diode pads.

    All measurements are in millimeters.
    """

    width: float
    height: float
    center_x: float


class DiodeSpecs(NamedTuple):
    """Complete specifications for generating a diode footprint.

    Defines all physical dimensions, pad properties, and reference designator
    positions needed to generate a complete KiCad footprint file.
    """

    body_dimensions: BodyDimensions
    pad_dimensions: PadDimensions
    ref_offset_y: float


DIODE_SPECS: dict[str, DiodeSpecs] = {
    # Example PowerDI-123 package
    "PowerDI-123": DiodeSpecs(
        body_dimensions=BodyDimensions(
            width=3.0,
            height=2.0,
        ),
        pad_dimensions=PadDimensions(
            width=1.0,
            height=1.2,
            center_x=1.15,
        ),
        ref_offset_y=-2.5,
    ),
}
