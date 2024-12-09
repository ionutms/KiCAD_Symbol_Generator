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
        body_dimensions=BodyDimensions(width=1.82, height=0.92),
        pad_dimensions=PadDimensions(width=0.56, height=0.62, center_x=0.48),
        ref_offset_y=-1.27),
    "0603": FootprintSpecs(
        body_dimensions=BodyDimensions(width=2.96, height=1.46),
        pad_dimensions=PadDimensions(width=0.9, height=0.95, center_x=0.775),
        ref_offset_y=-1.524),
    "0805": FootprintSpecs(
        body_dimensions=BodyDimensions(width=3.4, height=1.96),
        pad_dimensions=PadDimensions(width=1.0, height=1.45, center_x=0.95),
        ref_offset_y=-1.778),
    "1206": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.6, height=2.3),
        pad_dimensions=PadDimensions(width=1.15, height=1.8, center_x=1.475),
        ref_offset_y=-2.032),
}
