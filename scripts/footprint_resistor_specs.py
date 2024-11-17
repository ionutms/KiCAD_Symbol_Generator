"""Resistor footprint specifications using structured data types."""

from typing import Dict, NamedTuple


class BodyDimensions(NamedTuple):
    """
    Defines rectangular dimensions for component footprint body.

    All measurements are in millimeters.
    """
    width: float    # Total width of the component body
    height: float   # Total height of the component body


class PadDimensions(NamedTuple):
    """
    Defines dimensions for component pads.

    All measurements are in millimeters.
    """
    width: float     # Width of each pad
    height: float    # Height of each pad
    center_x: float  # Distance from origin to pad center
    roundrect_ratio: float = 0.25  # Constant value for pad corner rounding


class SilkscreenParams(NamedTuple):
    """
    Defines parameters for silkscreen layout.

    All measurements are in millimeters.
    """
    y_position: float      # Y coordinate for silkscreen line
    extension: float       # Extension beyond body outline
    inset: float          # Inset from body edge


class TextPositions(NamedTuple):
    """
    Defines Y-axis positions for various text elements.

    All measurements are in millimeters.
    """
    reference: float       # Reference designator position
    value: float          # Component value position
    fab_reference: float  # Fabrication layer reference position


class ResistorSpecs(NamedTuple):
    """
    Complete specifications for generating a resistor footprint.

    Defines all physical dimensions, pad properties, and text positions
    needed to generate a complete KiCad footprint file.
    """
    body_dimensions: BodyDimensions
    pad_dimensions: PadDimensions
    silkscreen: SilkscreenParams
    text_positions: TextPositions
    courtyard_margin: float


RESISTOR_SPECS: Dict[str, ResistorSpecs] = {
    "0402": ResistorSpecs(
        body_dimensions=BodyDimensions(
            width=1.0,
            height=0.5
        ),
        pad_dimensions=PadDimensions(
            width=0.54,
            height=0.64,
            center_x=0.51
        ),
        silkscreen=SilkscreenParams(
            y_position=0.38,
            extension=0.153641,
            inset=0.15
        ),
        text_positions=TextPositions(
            reference=-1.27,
            value=1.27,
            fab_reference=2.54
        ),
        courtyard_margin=0.91
    ),
    "0603": ResistorSpecs(
        body_dimensions=BodyDimensions(
            width=1.6,
            height=0.8
        ),
        pad_dimensions=PadDimensions(
            width=0.8,
            height=0.95,
            center_x=0.825
        ),
        silkscreen=SilkscreenParams(
            y_position=0.5225,
            extension=0.237258,
            inset=0.24
        ),
        text_positions=TextPositions(
            reference=-1.524,
            value=1.524,
            fab_reference=2.794
        ),
        courtyard_margin=1.48
    ),
    "0805": ResistorSpecs(
        body_dimensions=BodyDimensions(
            width=2.0,
            height=1.25
        ),
        pad_dimensions=PadDimensions(
            width=1.025,
            height=1.4,
            center_x=0.9125
        ),
        silkscreen=SilkscreenParams(
            y_position=0.735,
            extension=0.227064,
            inset=0.23
        ),
        text_positions=TextPositions(
            reference=-1.778,
            value=1.778,
            fab_reference=3.048
        ),
        courtyard_margin=1.68
    ),
    "1206": ResistorSpecs(
        body_dimensions=BodyDimensions(
            width=3.2,
            height=1.6
        ),
        pad_dimensions=PadDimensions(
            width=1.125,
            height=1.75,
            center_x=1.4625
        ),
        silkscreen=SilkscreenParams(
            y_position=0.91,
            extension=0.727064,
            inset=0.25
        ),
        text_positions=TextPositions(
            reference=-2.032,
            value=2.032,
            fab_reference=3.302
        ),
        courtyard_margin=2.28
    )
}
