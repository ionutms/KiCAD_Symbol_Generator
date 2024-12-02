"""Specifications for diode footprint generation."""

from typing import NamedTuple


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for diode body outlines.

    All measurements are in millimeters relative to the origin point (0,0).
    """

    width: float
    height: float


class PadDimensionsAsymmetric(NamedTuple):
    """Defines dimensions for asymmetric diode pads.

    All measurements are in millimeters. For PowerDI-123 package,
    cathode_pad is pad 1, anode_pad is pad 2.

    """

    width: float
    height: float
    pad_center_x: float
    pad_pitch_y: float
    pins_per_side: float
    thermal_width: float
    thermal_height: float
    thermal_pad_center_x: float


class DiodeSpecs(NamedTuple):
    """Complete specifications for generating a diode footprint.

    Defines all physical dimensions, pad properties, and reference designator
    positions needed to generate a complete KiCad footprint file.
    """

    body_dimensions: BodyDimensions
    pad_dimensions: PadDimensionsAsymmetric
    ref_offset_y: float


DIODE_SPECS: dict[str, DiodeSpecs] = {
    "PowerPAK 1212-8": DiodeSpecs(
        body_dimensions=BodyDimensions(width=4.0, height=3.9),
        pad_dimensions=PadDimensionsAsymmetric(
            width=0.99,
            height=0.405,
            pad_center_x=1.435,
            thermal_width=1.725,
            thermal_height=2.385,
            thermal_pad_center_x=0.558,
            pad_pitch_y=0.66,
            pins_per_side=4,
            ),
        ref_offset_y=-2.5),
}
