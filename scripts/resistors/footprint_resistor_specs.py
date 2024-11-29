"""Resistor footprint specifications using structured data types."""

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


class ResistorSpecs(NamedTuple):
    """Complete specifications for generating a resistor footprint.

    Defines all physical dimensions, pad properties, and text positions
    needed to generate a complete KiCad footprint file.
    """

    body_dimensions: BodyDimensions
    pad_dimensions: PadDimensions
    ref_offset_y: float


RESISTOR_SPECS: dict[str, ResistorSpecs] = {
    "0402": ResistorSpecs(
        body_dimensions=BodyDimensions(width=1.82, height=0.955),
        pad_dimensions=PadDimensions(width=0.54, height=0.64, center_x=0.51),
        ref_offset_y=-1.27),
    "0603": ResistorSpecs(
        body_dimensions=BodyDimensions(width=2.96, height=1.54),
        pad_dimensions=PadDimensions(width=0.8, height=0.95, center_x=0.825),
        ref_offset_y=-1.524),
    "0805": ResistorSpecs(
        body_dimensions=BodyDimensions(width=3.36, height=2.09),
        pad_dimensions=PadDimensions(
            width=1.025, height=1.4, center_x=0.9125),
        ref_offset_y=-1.778),
    "1206": ResistorSpecs(
        body_dimensions=BodyDimensions(width=4.56, height=2.74),
        pad_dimensions=PadDimensions(
            width=1.125, height=1.75, center_x=1.4625),
        ref_offset_y=-2.032),
}
