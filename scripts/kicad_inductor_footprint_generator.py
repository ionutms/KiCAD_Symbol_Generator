"""
KiCad Footprint Generator for Power Inductors

Generates standardized KiCad footprint files (.kicad_mod) for power inductors.
Uses manufacturer specifications to create accurate footprints with appropriate
pad dimensions and clearances.
"""

from typing import Dict, NamedTuple
from uuid import uuid4


class PadDimensions(NamedTuple):
    """
    Defines SMD pad dimensions and positioning.

    All measurements in millimeters.
    """
    width: float      # Width of each pad
    height: float     # Height of each pad
    center_x: float   # Distance from origin to pad center


class BodyDimensions(NamedTuple):
    "TODO"
    width: float
    height: float


class TextOffsetY(NamedTuple):
    "TODO"
    ref: float
    value: float
    fab: float


class InductorSpecs(NamedTuple):
    """
    Complete specifications for generating an inductor footprint.

    Combines physical dimensions with series-specific properties for
    generating accurate KiCad footprints.
    """
    series_name: str          # Inductor series name
    body_dims: BodyDimensions
    pad_dims: PadDimensions  # Pad specifications
    silk_line_y: float       # Y-coordinate of silkscreen lines
    text_offset_y: TextOffsetY


# Mapping of inductor series to physical dimensions
INDUCTOR_SPECS: Dict[str, Dict[str, float]] = {
    "XAL1010": {
        "body": {"width": 10.922, "height": 12.192},
        "pad": {"width": 2.3876, "height": 8.9916, "center_x": 3.3274},
        "silk_line_y": 6.096,
        "text_offset_y": {"ref": -6.858, "value": 8.128, "fab": 6.858},
    },
    "XAL1030": {
        "body": {"width": 10.922, "height": 12.192},
        "pad": {"width": 2.3876, "height": 8.9916, "center_x": 3.3274},
        "silk_line_y": 6.096,
        "text_offset_y": {"ref": -6.858, "value": 8.128, "fab": 6.858},
    },
    "XAL1060": {
        "body": {"width": 10.922, "height": 12.192},
        "pad": {"width": 2.3876, "height": 8.9916, "center_x": 3.3274},
        "silk_line_y": 6.096,
        "text_offset_y": {"ref": -6.858, "value": 8.128, "fab": 6.858},
    },
    "XAL1080": {
        "body": {"width": 10.922, "height": 12.192},
        "pad": {"width": 2.3876, "height": 8.9916, "center_x": 3.3274},
        "silk_line_y": 6.096,
        "text_offset_y": {"ref": -6.858, "value": 8.128, "fab": 6.858},
    },
    "XAL1350": {
        "body": {"width": 13.716, "height": 14.732},
        "pad": {"width": 2.9718, "height": 11.9888, "center_x": 4.3053},
        "silk_line_y": 7.366,
        "text_offset_y": {"ref": -8.128, "value": 8.128, "fab": 9.398},
    },
    "XAL1510": {
        "body": {"width": 15.748, "height": 16.764},
        "pad": {"width": 3.175, "height": 13.208, "center_x": 5.2959},
        "silk_line_y": 8.382,
        "text_offset_y": {"ref": -9.144, "value": 9.144, "fab": 10.414},
    },
    "XAL1513": {
        "body": {"width": 15.748, "height": 16.764},
        "pad": {"width": 3.175, "height": 13.208, "center_x": 5.2959},
        "silk_line_y": 8.382,
        "text_offset_y": {"ref": -9.144, "value": 9.144, "fab": 10.414},
    },
    "XAL1580": {
        "body": {"width": 15.748, "height": 16.764},
        "pad": {"width": 3.175, "height": 13.208, "center_x": 5.2959},
        "silk_line_y": 8.382,
        "text_offset_y": {"ref": -9.144, "value": 9.144, "fab": 10.414},
    },
    "XAL4020": {
        "body": {"width": 4.4704, "height": 4.4704},
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
        "silk_line_y": 2.2352,
        "text_offset_y": {"ref": -3.048, "value": 3.048, "fab": 4.318},
    },
    "XAL4030": {
        "body": {"width": 4.4704, "height": 4.4704},
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
        "silk_line_y": 2.2352,
        "text_offset_y": {"ref": -3.048, "value": 3.048, "fab": 4.318},
    },
    "XAL4040": {
        "body": {"width": 4.4704, "height": 4.4704},
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
        "silk_line_y": 2.2352,
        "text_offset_y": {"ref": -3.048, "value": 3.048, "fab": 4.318},
    },
    "XAL5020": {
        "body": {"width": 5.6896, "height": 5.9436},
        "pad": {"width": 1.1684, "height": 4.699, "center_x": 1.651},
        "silk_line_y": 2.9718,
        "text_offset_y": {"ref": -3.81, "value": 3.81, "fab": 5.08},
    },
    "XAL5030": {
        "body": {"width": 5.6896, "height": 5.9436},
        "pad": {"width": 1.1684, "height": 4.699, "center_x": 1.651},
        "silk_line_y": 2.9718,
        "text_offset_y": {"ref": -3.81, "value": 3.81, "fab": 5.08},
    },
    "XAL5050": {
        "body": {"width": 5.6896, "height": 5.9436},
        "pad": {"width": 1.1684, "height": 4.699, "center_x": 1.651},
        "silk_line_y": 2.9718,
        "text_offset_y": {"ref": -3.81, "value": 3.81, "fab": 5.08},
    },
    "XAL6020": {
        "body": {"width": 6.858, "height": 7.112},
        "pad": {"width": 1.4224, "height": 5.4864, "center_x": 2.0193},
        "silk_line_y": 3.556,
        "text_offset_y": {"ref": -4.572, "value": 4.572, "fab": 5.842},
    },
    "XAL6030": {
        "body": {"width": 6.858, "height": 7.112},
        "pad": {"width": 1.4224, "height": 5.4864, "center_x": 2.0193},
        "silk_line_y": 3.556,
        "text_offset_y": {"ref": -4.572, "value": 4.572, "fab": 5.842},
    },
    "XAL6060": {
        "body": {"width": 6.858, "height": 7.112},
        "pad": {"width": 1.4224, "height": 5.4864, "center_x": 2.0193},
        "silk_line_y": 3.556,
        "text_offset_y": {"ref": -4.572, "value": 4.572, "fab": 5.842},
    },
    "XAL7020": {
        "body": {"width": 8.382, "height": 8.382},
        "pad": {"width": 1.778, "height": 6.5024, "center_x": 2.3622},
        "silk_line_y": 4.191,
        "text_offset_y": {"ref": -5.08, "value": 5.08, "fab": 6.35},
    },
    "XAL7030": {
        "body": {"width": 8.382, "height": 8.382},
        "pad": {"width": 1.778, "height": 6.5024, "center_x": 2.3622},
        "silk_line_y": 4.191,
        "text_offset_y": {"ref": -5.08, "value": 5.08, "fab": 6.35},
    },
    "XAL7050": {
        "body": {"width": 8.382, "height": 8.382},
        "pad": {"width": 1.778, "height": 6.5024, "center_x": 2.3622},
        "silk_line_y": 4.191,
        "text_offset_y": {"ref": -5.08, "value": 5.08, "fab": 6.35},
    },
    "XAL7070": {
        "body": {"width": 8.0264, "height": 8.382},
        "pad": {"width": 1.9304, "height": 6.5024, "center_x": 2.413},
        "silk_line_y": 4.191,
        "text_offset_y": {"ref": -5.08, "value": 5.08, "fab": 6.35},
    },
    "XAL8050": {
        "body": {"width": 8.636, "height": 9.144},
        "pad": {"width": 1.778, "height": 7.0104, "center_x": 2.5781},
        "silk_line_y": 4.572,
        "text_offset_y": {"ref": -5.588, "value": 5.588, "fab": 6.858},
    },
    "XAL8080": {
        "body": {"width": 8.636, "height": 9.144},
        "pad": {"width": 1.778, "height": 7.0104, "center_x": 2.5781},
        "silk_line_y": 4.572,
        "text_offset_y": {"ref": -5.588, "value": 5.588, "fab": 6.858},
    },
    "XFL2005": {
        "body": {"width": 2.6924, "height": 2.3876},
        "pad": {"width": 1.0414, "height": 2.2098, "center_x": 0.7239},
        "silk_line_y": 1.1938,
        "text_offset_y": {"ref": -2.032, "value": 2.032, "fab": 3.302},
    },
    "XFL2006": {
        "body": {"width": 2.286, "height": 2.3876},
        "pad": {"width": 0.6096, "height": 1.8034, "center_x": 0.6731},
        "silk_line_y": 1.1938,
        "text_offset_y": {"ref": -2.032, "value": 2.032, "fab": 3.302},
    },
    "XFL2010": {
        "body": {"width": 2.286, "height": 2.3876},
        "pad": {"width": 0.6096, "height": 1.8034, "center_x": 0.6731},
        "silk_line_y": 1.1938,
        "text_offset_y": {"ref": -2.032, "value": 2.032, "fab": 3.302},
    },
    "XFL3010": {
        "body": {"width": 3.3528, "height": 3.3528},
        "pad": {"width": 0.9906, "height": 2.8956, "center_x": 1.016},
        "silk_line_y": 1.6764,
        "text_offset_y": {"ref": -2.54, "value": 2.54, "fab": 3.81},
    },
    "XFL3012": {
        "body": {"width": 3.3528, "height": 3.3528},
        "pad": {"width": 0.9906, "height": 2.8956, "center_x": 1.016},
        "silk_line_y": 1.6764,
        "text_offset_y": {"ref": -2.54, "value": 2.54, "fab": 3.81},
    },
    "XFL4012": {
        "body": {"width": 4.4704, "height": 4.4704},
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
        "silk_line_y": 2.2352,
        "text_offset_y": {"ref": -3.048, "value": 3.048, "fab": 4.318},
    },
    "XFL4015": {
        "body": {"width": 4.4704, "height": 4.4704},
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
        "silk_line_y": 2.2352,
        "text_offset_y": {"ref": -3.048, "value": 3.048, "fab": 4.318},
    },
    "XFL4020": {
        "body": {"width": 4.4704, "height": 4.4704},
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
        "silk_line_y": 2.2352,
        "text_offset_y": {"ref": -3.048, "value": 3.048, "fab": 4.318},
    },
    "XFL4030": {
        "body": {"width": 4.4704, "height": 4.4704},
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
        "silk_line_y": 2.2352,
        "text_offset_y": {"ref": -3.048, "value": 3.048, "fab": 4.318},
    },
    "XFL5015": {
        "body": {"width": 5.6896, "height": 5.9436},
        "pad": {"width": 1.1684, "height": 4.699, "center_x": 1.651},
        "silk_line_y": 2.9718,
        "text_offset_y": {"ref": -3.81, "value": 3.81, "fab": 5.08},
    },
    "XFL5018": {
        "body": {"width": 5.6896, "height": 5.9436},
        "pad": {"width": 1.1684, "height": 4.699, "center_x": 1.651},
        "silk_line_y": 2.9718,
        "text_offset_y": {"ref": -3.81, "value": 3.81, "fab": 5.08},
    },
    "XFL5030": {
        "body": {"width": 5.6896, "height": 5.9436},
        "pad": {"width": 1.1684, "height": 4.699, "center_x": 1.651},
        "silk_line_y": 2.9718,
        "text_offset_y": {"ref": -3.81, "value": 3.81, "fab": 5.08},
    },
}


def create_inductor_specs(series_name: str) -> InductorSpecs:
    """
    Create complete inductor specifications from series name.

    Args:
        series_name: Name of the inductor series (e.g., "XAL1010")

    Returns:
        InductorSpecs object with complete physical dimensions

    Raises:
        KeyError: If series name is not found in INDUCTOR_DIMENSIONS
    """
    dims = INDUCTOR_SPECS[series_name]

    return InductorSpecs(
        series_name=series_name,
        body_dims=dims["body"],
        pad_dims=dims["pad"],
        silk_line_y=dims["silk_line_y"],
        text_offset_y=dims["text_offset_y"]
    )


def generate_footprint(specs: InductorSpecs) -> str:
    """
    Generate complete KiCad footprint file content for an inductor.

    Args:
        specs: Physical specifications for the inductor

    Returns:
        Complete .kicad_mod file content as formatted string
    """
    sections = [
        generate_header(specs),
        generate_properties(specs),
        generate_silkscreen(specs),
        generate_courtyard(specs),
        generate_fab_layer(specs),
        generate_pads(specs),
        generate_3d_model(specs),
        ")"  # Close the footprint
    ]
    return "\n".join(sections)


def generate_header(specs: InductorSpecs) -> str:
    """Generate the footprint header section."""
    return (
        f'(footprint "{specs.series_name}"\n'
        '    (version 20240108)\n'
        '    (generator "pcbnew")\n'
        '    (generator_version "8.0")\n'
        '    (layer "F.Cu")\n'
        '    (descr "")\n'
        '    (tags "")\n'
        '    (attr smd)'
    )


def generate_properties(specs: InductorSpecs) -> str:
    """Generate properties section with inductor-specific information."""
    font_props = (
        '        (effects\n'
        '            (font\n'
        '                (size 0.762 0.762)\n'
        '                (thickness 0.1524)\n'
        '            )\n'
        '            (justify left)\n'
        '        )'
    )

    return (
        '    (property "Reference" "REF**"\n'
        f'        (at 0 {specs.text_offset_y["ref"]} 0)\n'
        '        (unlocked yes)\n'
        '        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        '    )\n'
        f'    (property "Value" "{specs.series_name}"\n'
        f'        (at 0 {specs.text_offset_y["value"]} 0)\n'
        '        (unlocked yes)\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        '    )\n'
        '    (property "Footprint" ""\n'
        '        (at 0 0 0)\n'
        '        (layer "F.Fab")\n'
        '        (hide yes)\n'
        f'        (uuid "{uuid4()}")\n'
        '        (effects\n'
        '            (font\n'
        '                (size 1.27 1.27)\n'
        '                (thickness 0.15)\n'
        '            )\n'
        '        )\n'
        '    )'
    )


def generate_silkscreen(specs: InductorSpecs) -> str:
    """Generate silkscreen elements with inductor-specific clearances."""
    silkscreen_x = specs.pad_dims["center_x"] - specs.pad_dims["width"] / 2

    silkscreen = []

    for symbol in ['-', '']:
        silkscreen.append(
            '    (fp_line\n'
            f'        (start {silkscreen_x} {symbol}{specs.silk_line_y})\n'
            f'        (end -{silkscreen_x} {symbol}{specs.silk_line_y})\n'
            '        (stroke\n'
            '            (width 0.1524)\n'
            '            (type solid)\n'
            '        )\n'
            '        (layer "F.SilkS")\n'
            f'        (uuid "{uuid4()}")\n'
            '    )'
        )

    return "\n".join(silkscreen)


def generate_courtyard(specs: InductorSpecs) -> str:
    """Generate courtyard outline with inductor-specific clearances."""
    half_width = specs.body_dims["width"] / 2
    half_height = specs.body_dims["height"] / 2

    return (
        '    (fp_rect\n'
        f'        (start -{half_width} -{half_height})\n'
        f'        (end {half_width} {half_height})\n'
        '        (stroke\n'
        '            (width 0.00635)\n'
        '            (type default)\n'
        '        )\n'
        '        (fill none)\n'
        '        (layer "F.CrtYd")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )


def generate_fab_layer(specs: InductorSpecs) -> str:
    """Generate fabrication layer with inductor-specific markings."""
    half_width = specs.body_dims["width"] / 2
    half_height = specs.body_dims["height"] / 2

    fab_elements = []

    # Main body outline
    fab_elements.append(
        '    (fp_rect\n'
        f'        (start -{half_width} -{half_height})\n'
        f'        (end {half_width} {half_height})\n'
        '        (stroke\n'
        '            (width 0.0254)\n'
        '            (type default)\n'
        '        )\n'
        '        (fill none)\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )

    # Polarity marker
    fab_elements.append(
        '    (fp_circle\n'
        f'        (center -{specs.pad_dims["center_x"]} 0)\n'
        f'        (end -{specs.pad_dims["center_x"] - 0.0762} 0)\n'
        '        (stroke\n'
        '            (width 0.0254)\n'
        '            (type solid)\n'
        '        )\n'
        '        (fill none)\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        '    )'
    )

    # Reference on fab layer
    fab_elements.append(
        f'    (fp_text user "${{REFERENCE}}"\n'
        f'        (at 0 {specs.text_offset_y["fab"]} 0)\n'
        '        (unlocked yes)\n'
        '        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        '        (effects\n'
        '            (font\n'
        '                (size 0.762 0.762)\n'
        '                (thickness 0.1524)\n'
        '            )\n'
        '            (justify left)\n'
        '        )\n'
        '    )'
    )

    return "\n".join(fab_elements)


def generate_pads(specs: InductorSpecs) -> str:
    """Generate SMD pads with inductor-specific dimensions."""
    pads = []

    for pad_number, symbol in enumerate(['-', ''], start=1):
        pads.append(
            f'    (pad "{pad_number}" smd rect\n'
            f'        (at {symbol}{specs.pad_dims["center_x"]} 0)\n'
            '        (size '
            f'{specs.pad_dims["width"]} '
            f'{specs.pad_dims["height"]})\n'
            '        (layers "F.Cu" "F.Paste" "F.Mask")\n'
            f'        (uuid "{uuid4()}")\n'
            '    )'
        )

    return "\n".join(pads)


def generate_3d_model(specs: InductorSpecs) -> str:
    """Generate 3D model reference for the inductor."""
    return (
        f'    (model "${{KIPRJMOD}}/KiCAD_Symbol_Generator/3D_models/'
        f'{specs.series_name}.step"\n'
        '        (offset\n'
        '            (xyz 0 0 0)\n'
        '        )\n'
        '        (scale\n'
        '            (xyz 1 1 1)\n'
        '        )\n'
        '        (rotate\n'
        '            (xyz 0 0 0)\n'
        '        )\n'
        '    )'
    )


def generate_footprint_file(
        part_info,  # Can be str or PartInfo
        output_dir: str) -> None:
    """
    Generate and save a complete .kicad_mod file for an inductor.

    Args:
        part_info:
            Either series name string (e.g., "XAL1010") or PartInfo object
        output_dir: Directory to save the generated footprint file

    Raises:
        KeyError: If series_name is not found in INDUCTOR_DIMENSIONS
        IOError: If there are problems writing the output file
    """

    if part_info.series not in INDUCTOR_SPECS:
        raise ValueError(f"Unknown series: {part_info.series}")
    # Extract series name if PartInfo object is provided
    series_name = \
        part_info.series if hasattr(part_info, 'series') else part_info

    inductor_specs = create_inductor_specs(series_name)
    footprint_content = generate_footprint(inductor_specs)

    filename = f"{output_dir}/{series_name}.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(footprint_content)
