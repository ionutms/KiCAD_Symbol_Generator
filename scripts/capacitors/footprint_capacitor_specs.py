"""Capacitor footprint specifications using structured data types."""

from typing import NamedTuple


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for component footprint body.

    All measurements are in millimeters.
    """

    width: float  # Total width of the component body
    height: float  # Total height of the component body


class PadDimensions(NamedTuple):
    """Defines dimensions for component pads.

    All measurements are in millimeters.
    """

    width: float  # Width of each pad
    height: float  # Height of each pad
    center_x: float  # Distance from origin to pad center


class FootprintSpecs(NamedTuple):
    """Complete specifications for generating a capacitor footprint.

    Defines all physical dimensions, pad properties, and text positions
    needed to generate a complete KiCad footprint file.
    """

    body_dimensions: BodyDimensions
    pad_dimensions: PadDimensions
    ref_offset_y: float


FOOTPRINTS_SPECS: dict[str, FootprintSpecs] = {
    "0402": FootprintSpecs(
        body_dimensions=BodyDimensions(width=1.82, height=0.955),
        pad_dimensions=PadDimensions(width=0.6, height=0.7, center_x=0.54),
        ref_offset_y=-1.27),
    "0603": FootprintSpecs(
        body_dimensions=BodyDimensions(width=2.96, height=1.54),
        pad_dimensions=PadDimensions(width=0.9, height=1.0, center_x=0.875),
        ref_offset_y=-1.524),
    "0805": FootprintSpecs(
        body_dimensions=BodyDimensions(width=3.36, height=2.09),
        pad_dimensions=PadDimensions(width=1.15, height=1.45, center_x=0.95),
        ref_offset_y=-1.778),
    "1206": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.56, height=2.74),
        pad_dimensions=PadDimensions(width=1.25, height=1.8, center_x=1.5),
        ref_offset_y=-2.032),
}
