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
    thermal_pad_center_y: list[float]
    thermal_pad_numbers: list[int]
    pad_numbers: list[int]


class FootprintSpecs(NamedTuple):
    """Complete specifications for generating a diode footprint.

    Defines all physical dimensions, pad properties, and reference designator
    positions needed to generate a complete KiCad footprint file.
    """

    body_dimensions: BodyDimensions
    pad_dimensions: PadDimensionsAsymmetric
    ref_offset_y: float


FOOTPRINTS_SPECS: dict[str, FootprintSpecs] = {
    "PowerPAK 1212-8": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.0, height=3.9),
        pad_dimensions=PadDimensionsAsymmetric(
            width=0.99, height=0.405, pad_center_x=1.435,
            pad_pitch_y=0.66, pins_per_side=4,
            thermal_width=1.725, thermal_height=2.385,
            thermal_pad_center_x=0.558, thermal_pad_center_y=[0],
            thermal_pad_numbers=[5], pad_numbers=[1, 2, 3, 4, 5, 5, 5, 5]),
        ref_offset_y=-2.5,
    ),
    "LFPAK33-8": FootprintSpecs(
        body_dimensions=BodyDimensions(width=4.1, height=3.6),
        pad_dimensions=PadDimensionsAsymmetric(
            width=0.83, height=0.4, pad_center_x=1.535,
            pad_pitch_y=0.65, pins_per_side=4,
            thermal_width=1.85, thermal_height=2.35,
            thermal_pad_center_x=0.405, thermal_pad_center_y=[0],
            thermal_pad_numbers=[5], pad_numbers=[1, 2, 3, 4, 5, 5, 5, 5]),
        ref_offset_y=-2.5,
    ),
    "LFPAK56D-8": FootprintSpecs(
        body_dimensions=BodyDimensions(width=7.3, height=5.85),
        pad_dimensions=PadDimensionsAsymmetric(
            width=1.15, height=0.7, pad_center_x=2.95,
            pad_pitch_y=1.27, pins_per_side=4,
            thermal_width=4.4, thermal_height=1.97,
            thermal_pad_center_x=0.425, thermal_pad_center_y=[1.27, -1.27],
            thermal_pad_numbers=[5, 6], pad_numbers=[1, 2, 3, 4, 5, 5, 6, 6]),
        ref_offset_y=-3.6,
    ),
    "PowerPAK SO-8": FootprintSpecs(
        body_dimensions=BodyDimensions(width=7.0, height=5.0),
        pad_dimensions=PadDimensionsAsymmetric(
            width=1.27, height=0.66, pad_center_x=2.67,
            pad_pitch_y=1.27, pins_per_side=4,
            thermal_width=3.81, thermal_height=1.93,
            thermal_pad_center_x=0.69, thermal_pad_center_y=[1.27, -1.27],
            thermal_pad_numbers=[5, 6], pad_numbers=[1, 2, 3, 4, 5, 5, 6, 6]),
        ref_offset_y=-3.2,
    ),
}
