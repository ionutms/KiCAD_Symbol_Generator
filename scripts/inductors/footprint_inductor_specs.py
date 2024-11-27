"""Specifications for inductor footprint generation."""

from typing import NamedTuple


class BodyDimensions(NamedTuple):
    """Defines rectangular dimensions for inductor body outlines.

    All measurements are in millimeters relative to the origin point (0,0).
    """

    width: float  # Total width of inductor body
    height: float  # Total height of inductor body


class PadDimensions(NamedTuple):
    """Defines dimensions for inductor pads.

    All measurements are in millimeters.
    """

    width: float  # Width of each pad
    height: float  # Height of each pad
    center_x: float  # Distance from origin to pad center on X axis


class InductorSpecs(NamedTuple):
    """Complete specifications for generating an inductor footprint.

    Defines all physical dimensions, pad properties, and reference designator
    positions needed to generate a complete KiCad footprint file.
    """

    body_dimensions: BodyDimensions  # Basic rectangle dimensions
    pad_dimensions: PadDimensions  # Pad size and positioning
    ref_offset_y: float  # Y offset for reference designator


INDUCTOR_SPECS: dict[str, InductorSpecs] = {
    "XAL1010": InductorSpecs(
        body_dimensions=BodyDimensions(width=10.922, height=12.192),
        pad_dimensions=PadDimensions(
            width=2.3876, height=8.9916, center_x=3.3274),
        ref_offset_y=-6.858),
    "XAL1030": InductorSpecs(
        body_dimensions=BodyDimensions(width=10.922, height=12.192),
        pad_dimensions=PadDimensions(
            width=2.3876, height=8.9916, center_x=3.3274),
        ref_offset_y=-6.858),
    "XAL1060": InductorSpecs(
        body_dimensions=BodyDimensions(width=10.922, height=12.192),
        pad_dimensions=PadDimensions(
            width=2.3876, height=8.9916, center_x=3.3274),
        ref_offset_y=-6.858),
    "XAL1080": InductorSpecs(
        body_dimensions=BodyDimensions(width=10.922, height=12.192),
        pad_dimensions=PadDimensions(
            width=2.3876, height=8.9916, center_x=3.3274),
        ref_offset_y=-6.858),
    "XAL1350": InductorSpecs(
        body_dimensions=BodyDimensions(width=13.716, height=14.732),
        pad_dimensions=PadDimensions(
            width=2.9718, height=11.9888, center_x=4.3053),
        ref_offset_y=-8.128),
    "XAL1510": InductorSpecs(
        body_dimensions=BodyDimensions(width=15.748, height=16.764),
        pad_dimensions=PadDimensions(
            width=3.175, height=13.208, center_x=5.2959),
        ref_offset_y=-9.144),
    "XAL1513": InductorSpecs(
        body_dimensions=BodyDimensions(width=15.748, height=16.764),
        pad_dimensions=PadDimensions(
            width=3.175, height=13.208, center_x=5.2959),
        ref_offset_y=-9.144),
    "XAL1580": InductorSpecs(
        body_dimensions=BodyDimensions(width=15.748, height=16.764),
        pad_dimensions=PadDimensions(
            width=3.175, height=13.208, center_x=5.2959),
        ref_offset_y=-9.144),
    "XAL4020": InductorSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652, height=3.4036, center_x=1.1811),
        ref_offset_y=-3.048),
    "XAL4030": InductorSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652, height=3.4036, center_x=1.1811),
        ref_offset_y=-3.048),
    "XAL4040": InductorSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652, height=3.4036, center_x=1.1811),
        ref_offset_y=-3.048),
    "XAL5020": InductorSpecs(
        body_dimensions=BodyDimensions(width=5.6896, height=5.9436),
        pad_dimensions=PadDimensions(
            width=1.1684, height=4.699, center_x=1.651),
        ref_offset_y=-3.81),
    "XAL5030": InductorSpecs(
        body_dimensions=BodyDimensions(width=5.6896, height=5.9436),
        pad_dimensions=PadDimensions(
            width=1.1684, height=4.699, center_x=1.651),
        ref_offset_y=-3.81),
    "XAL5050": InductorSpecs(
        body_dimensions=BodyDimensions(width=5.6896, height=5.9436),
        pad_dimensions=PadDimensions(
            width=1.1684, height=4.699, center_x=1.651),
        ref_offset_y=-3.81),
    "XAL6020": InductorSpecs(
        body_dimensions=BodyDimensions(width=6.858, height=7.112),
        pad_dimensions=PadDimensions(
            width=1.4224, height=5.4864, center_x=2.0193),
        ref_offset_y=-4.572),
    "XAL6030": InductorSpecs(
        body_dimensions=BodyDimensions(width=6.858, height=7.112),
        pad_dimensions=PadDimensions(
            width=1.4224, height=5.4864, center_x=2.0193),
        ref_offset_y=-4.572),
    "XAL6060": InductorSpecs(
        body_dimensions=BodyDimensions(width=6.858, height=7.112),
        pad_dimensions=PadDimensions(
            width=1.4224, height=5.4864, center_x=2.0193),
        ref_offset_y=-4.572),
    "XAL7020": InductorSpecs(
        body_dimensions=BodyDimensions(width=8.382, height=8.382),
        pad_dimensions=PadDimensions(
            width=1.778, height=6.5024, center_x=2.3622),
        ref_offset_y=-5.08),
    "XAL7030": InductorSpecs(
        body_dimensions=BodyDimensions(width=8.382, height=8.382),
        pad_dimensions=PadDimensions(
            width=1.778, height=6.5024, center_x=2.3622),
        ref_offset_y=-5.08),
    "XAL7050": InductorSpecs(
        body_dimensions=BodyDimensions(width=8.382, height=8.382),
        pad_dimensions=PadDimensions(
            width=1.778, height=6.5024, center_x=2.3622),
        ref_offset_y=-5.08),
    "XAL7070": InductorSpecs(
        body_dimensions=BodyDimensions(width=8.0264, height=8.382),
        pad_dimensions=PadDimensions(
            width=1.9304, height=6.5024, center_x=2.413),
        ref_offset_y=-5.08),
    "XAL8050": InductorSpecs(
        body_dimensions=BodyDimensions(width=8.636, height=9.144),
        pad_dimensions=PadDimensions(
            width=1.778, height=7.0104, center_x=2.5781),
        ref_offset_y=-5.588),
    "XAL8080": InductorSpecs(
        body_dimensions=BodyDimensions(width=8.636, height=9.144),
        pad_dimensions=PadDimensions(
            width=1.778, height=7.0104, center_x=2.5781),
        ref_offset_y=-5.588),
    "XFL2005": InductorSpecs(
        body_dimensions=BodyDimensions(width=2.6924, height=2.3876),
        pad_dimensions=PadDimensions(
            width=1.0414, height=2.2098, center_x=0.7239),
        ref_offset_y=-2.032),
    "XFL2006": InductorSpecs(
        body_dimensions=BodyDimensions(width=2.286, height=2.3876),
        pad_dimensions=PadDimensions(
            width=0.6096, height=1.8034, center_x=0.6731),
        ref_offset_y=-2.032),
    "XFL2010": InductorSpecs(
        body_dimensions=BodyDimensions(width=2.286, height=2.3876),
        pad_dimensions=PadDimensions(
            width=0.6096, height=1.8034, center_x=0.6731),
        ref_offset_y=-2.032),
    "XFL3010": InductorSpecs(
        body_dimensions=BodyDimensions(width=3.3528, height=3.3528),
        pad_dimensions=PadDimensions(
            width=0.9906, height=2.8956, center_x=1.016),
        ref_offset_y=-2.54),
    "XFL3012": InductorSpecs(
        body_dimensions=BodyDimensions(width=3.3528, height=3.3528),
        pad_dimensions=PadDimensions(
            width=0.9906, height=2.8956, center_x=1.016),
        ref_offset_y=-2.54),
    "XFL4012": InductorSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652, height=3.4036, center_x=1.1811),
        ref_offset_y=-3.048),
    "XFL4015": InductorSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652, height=3.4036, center_x=1.1811),
        ref_offset_y=-3.048),
    "XFL4020": InductorSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652, height=3.4036, center_x=1.1811),
        ref_offset_y=-3.048),
    "XFL4030": InductorSpecs(
        body_dimensions=BodyDimensions(width=4.4704, height=4.4704),
        pad_dimensions=PadDimensions(
            width=0.9652, height=3.4036, center_x=1.1811),
        ref_offset_y=-3.048),
    "XFL5015": InductorSpecs(
        body_dimensions=BodyDimensions(width=5.6896, height=5.9436),
        pad_dimensions=PadDimensions(
            width=1.1684, height=4.699, center_x=1.651),
        ref_offset_y=-3.81),
    "XFL5018": InductorSpecs(
        body_dimensions=BodyDimensions(width=5.6896, height=5.9436),
        pad_dimensions=PadDimensions(
            width=1.1684, height=4.699, center_x=1.651),
        ref_offset_y=-3.81),
    "XFL5030": InductorSpecs(
        body_dimensions=BodyDimensions(width=5.6896, height=5.9436),
        pad_dimensions=PadDimensions(
            width=1.1684, height=4.699, center_x=1.651),
        ref_offset_y=-3.81),
    "XFL6012": InductorSpecs(
        body_dimensions=BodyDimensions(width=6.858, height=7.112),
        pad_dimensions=PadDimensions(
            width=1.4224, height=5.4864, center_x=2.0193),
        ref_offset_y=-4.572),
    "XFL6060": InductorSpecs(
        body_dimensions=BodyDimensions(width=6.858, height=7.112),
        pad_dimensions=PadDimensions(
            width=1.4224, height=5.4864, center_x=2.0193),
        ref_offset_y=-4.572),
    "XFL7015": InductorSpecs(
        body_dimensions=BodyDimensions(width=8.382, height=8.382),
        pad_dimensions=PadDimensions(
            width=1.778, height=6.223, center_x=2.286),
        ref_offset_y=-5.08),
}
