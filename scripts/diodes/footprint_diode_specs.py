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

    cathode_width: float
    cathode_height: float
    cathode_center_x: float
    anode_width: float
    anode_height: float
    anode_center_x: float
    roundrect_ratio: float = 0.25


class FootprintSpecs(NamedTuple):
    """Complete specifications for generating a diode footprint.

    Defines all physical dimensions, pad properties, and reference designator
    positions needed to generate a complete KiCad footprint file.
    """

    body_dimensions: BodyDimensions
    pad_dimensions: PadDimensionsAsymmetric
    ref_offset_y: float


FOOTPRINTS_SPECS: dict[str, FootprintSpecs] = {
    "PowerDI_123": FootprintSpecs(
        body_dimensions=BodyDimensions(
            width=5.0,
            height=2.6),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=2.4,
            cathode_height=1.5,
            cathode_center_x=0.85,
            anode_width=1.05,
            anode_height=1.5,
            anode_center_x=1.525),
        ref_offset_y=-2.5),
    "SOD_123": FootprintSpecs(
        body_dimensions=BodyDimensions(
            width=4.8,
            height=2.0),
        pad_dimensions=PadDimensionsAsymmetric(
            cathode_width=0.91,
            cathode_height=1.22,
            cathode_center_x=1.635,
            anode_width=0.91,
            anode_height=1.22,
            anode_center_x=1.635),
        ref_offset_y=-1.778),
}
