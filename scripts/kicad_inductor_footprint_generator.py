"""
KiCad Footprint Generator for Power Inductors

Generates standardized KiCad footprint files (.kicad_mod) for power inductors.
Uses manufacturer specifications to create accurate footprints with appropriate
pad dimensions and clearances.
"""

from typing import Dict, NamedTuple
from uuid import uuid4
import series_specs_inductors as ssi


class PadDimensions(NamedTuple):
    """
    Defines SMD pad dimensions and positioning.

    All measurements in millimeters.
    """
    width: float      # Width of each pad
    height: float     # Height of each pad
    center_x: float   # Distance from origin to pad center


class BodyDimensions(NamedTuple):
    """
    Defines part body dimensions.

    All measurements in millimeters.
    """
    width: float
    height: float


class InductorSpecs(NamedTuple):
    """
    Complete specifications for generating an inductor footprint.

    Combines physical dimensions with series-specific properties for
    generating accurate KiCad footprints.
    """
    series_name: str          # Inductor series name
    body_dims: BodyDimensions
    pad_dims: PadDimensions  # Pad specifications
    ref_offset_y: float


# Mapping of inductor series to physical dimensions
INDUCTOR_SPECS: Dict[str, Dict[str, float]] = {
    "XAL1010": {
        "body": {"width": 10.922, "height": 12.192}, "ref_offset_y": -6.858,
        "pad": {"width": 2.3876, "height": 8.9916, "center_x": 3.3274},
    },
    "XAL1030": {
        "body": {"width": 10.922, "height": 12.192}, "ref_offset_y": -6.858,
        "pad": {"width": 2.3876, "height": 8.9916, "center_x": 3.3274},
    },
    "XAL1060": {
        "body": {"width": 10.922, "height": 12.192}, "ref_offset_y": -6.858,
        "pad": {"width": 2.3876, "height": 8.9916, "center_x": 3.3274},
    },
    "XAL1080": {
        "body": {"width": 10.922, "height": 12.192}, "ref_offset_y": -6.858,
        "pad": {"width": 2.3876, "height": 8.9916, "center_x": 3.3274},
    },
    "XAL1350": {
        "body": {"width": 13.716, "height": 14.732}, "ref_offset_y": -8.128,
        "pad": {"width": 2.9718, "height": 11.9888, "center_x": 4.3053},
    },
    "XAL1510": {
        "body": {"width": 15.748, "height": 16.764}, "ref_offset_y": -9.144,
        "pad": {"width": 3.175, "height": 13.208, "center_x": 5.2959},
    },
    "XAL1513": {
        "body": {"width": 15.748, "height": 16.764}, "ref_offset_y": -9.144,
        "pad": {"width": 3.175, "height": 13.208, "center_x": 5.2959},
    },
    "XAL1580": {
        "body": {"width": 15.748, "height": 16.764}, "ref_offset_y": -9.144,
        "pad": {"width": 3.175, "height": 13.208, "center_x": 5.2959},
    },
    "XAL4020": {
        "body": {"width": 4.4704, "height": 4.4704}, "ref_offset_y": -3.048,
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
    },
    "XAL4030": {
        "body": {"width": 4.4704, "height": 4.4704}, "ref_offset_y": -3.048,
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
    },
    "XAL4040": {
        "body": {"width": 4.4704, "height": 4.4704}, "ref_offset_y": -3.048,
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
    },
    "XAL5020": {
        "body": {"width": 5.6896, "height": 5.9436}, "ref_offset_y": -3.81,
        "pad": {"width": 1.1684, "height": 4.699, "center_x": 1.651},
    },
    "XAL5030": {
        "body": {"width": 5.6896, "height": 5.9436}, "ref_offset_y": -3.81,
        "pad": {"width": 1.1684, "height": 4.699, "center_x": 1.651},
    },
    "XAL5050": {
        "body": {"width": 5.6896, "height": 5.9436}, "ref_offset_y": -3.81,
        "pad": {"width": 1.1684, "height": 4.699, "center_x": 1.651},
    },
    "XAL6020": {
        "body": {"width": 6.858, "height": 7.112}, "ref_offset_y": -4.572,
        "pad": {"width": 1.4224, "height": 5.4864, "center_x": 2.0193},
    },
    "XAL6030": {
        "body": {"width": 6.858, "height": 7.112}, "ref_offset_y": -4.572,
        "pad": {"width": 1.4224, "height": 5.4864, "center_x": 2.0193},
    },
    "XAL6060": {
        "body": {"width": 6.858, "height": 7.112}, "ref_offset_y": -4.572,
        "pad": {"width": 1.4224, "height": 5.4864, "center_x": 2.0193},
    },
    "XAL7020": {
        "body": {"width": 8.382, "height": 8.382}, "ref_offset_y": -5.08,
        "pad": {"width": 1.778, "height": 6.5024, "center_x": 2.3622},
    },
    "XAL7030": {
        "body": {"width": 8.382, "height": 8.382}, "ref_offset_y": -5.08,
        "pad": {"width": 1.778, "height": 6.5024, "center_x": 2.3622},
    },
    "XAL7050": {
        "body": {"width": 8.382, "height": 8.382}, "ref_offset_y": -5.08,
        "pad": {"width": 1.778, "height": 6.5024, "center_x": 2.3622},
    },
    "XAL7070": {
        "body": {"width": 8.0264, "height": 8.382}, "ref_offset_y": -5.08,
        "pad": {"width": 1.9304, "height": 6.5024, "center_x": 2.413},
    },
    "XAL8050": {
        "body": {"width": 8.636, "height": 9.144}, "ref_offset_y": -5.588,
        "pad": {"width": 1.778, "height": 7.0104, "center_x": 2.5781},
    },
    "XAL8080": {
        "body": {"width": 8.636, "height": 9.144}, "ref_offset_y": -5.588,
        "pad": {"width": 1.778, "height": 7.0104, "center_x": 2.5781},
    },
    "XFL2005": {
        "body": {"width": 2.6924, "height": 2.3876}, "ref_offset_y": -2.032,
        "pad": {"width": 1.0414, "height": 2.2098, "center_x": 0.7239},
    },
    "XFL2006": {
        "body": {"width": 2.286, "height": 2.3876}, "ref_offset_y": -2.032,
        "pad": {"width": 0.6096, "height": 1.8034, "center_x": 0.6731},
    },
    "XFL2010": {
        "body": {"width": 2.286, "height": 2.3876}, "ref_offset_y": -2.032,
        "pad": {"width": 0.6096, "height": 1.8034, "center_x": 0.6731},
    },
    "XFL3010": {
        "body": {"width": 3.3528, "height": 3.3528}, "ref_offset_y": -2.54,
        "pad": {"width": 0.9906, "height": 2.8956, "center_x": 1.016},
    },
    "XFL3012": {
        "body": {"width": 3.3528, "height": 3.3528}, "ref_offset_y": -2.54,
        "pad": {"width": 0.9906, "height": 2.8956, "center_x": 1.016},
    },
    "XFL4012": {
        "body": {"width": 4.4704, "height": 4.4704}, "ref_offset_y": -3.048,
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
    },
    "XFL4015": {
        "body": {"width": 4.4704, "height": 4.4704}, "ref_offset_y": -3.048,
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
    },
    "XFL4020": {
        "body": {"width": 4.4704, "height": 4.4704}, "ref_offset_y": -3.048,
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
    },
    "XFL4030": {
        "body": {"width": 4.4704, "height": 4.4704}, "ref_offset_y": -3.048,
        "pad": {"width": 0.9652, "height": 3.4036, "center_x": 1.1811},
    },
    "XFL5015": {
        "body": {"width": 5.6896, "height": 5.9436}, "ref_offset_y": -3.81,
        "pad": {"width": 1.1684, "height": 4.699, "center_x": 1.651},
    },
    "XFL5018": {
        "body": {"width": 5.6896, "height": 5.9436}, "ref_offset_y": -3.81,
        "pad": {"width": 1.1684, "height": 4.699, "center_x": 1.651},
    },
    "XFL5030": {
        "body": {"width": 5.6896, "height": 5.9436}, "ref_offset_y": -3.81,
        "pad": {"width": 1.1684, "height": 4.699, "center_x": 1.651},
    },
    "XFL6012": {
        "body": {"width": 6.858, "height": 7.112}, "ref_offset_y": -4.572,
        "pad": {"width": 1.4224, "height": 5.4864, "center_x": 2.0193},
    },
    "XFL6060": {
        "body": {"width": 6.858, "height": 7.112}, "ref_offset_y": -4.572,
        "pad": {"width": 1.4224, "height": 5.4864, "center_x": 2.0193},
    },
    "XFL7015": {
        "body": {"width": 8.382, "height": 8.382}, "ref_offset_y": -5.08,
        "pad": {"width": 1.778, "height": 6.223, "center_x": 2.286},
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
        ref_offset_y=dims["ref_offset_y"]
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
        f'        (at 0 {specs.ref_offset_y} 0)\n'
        '        (unlocked yes)\n'
        '        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        '    )\n'
        f'    (property "Value" "{specs.series_name}"\n'
        f'        (at 0 {-1 * specs.ref_offset_y} 0)\n'
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
            '        (start '
            f'{silkscreen_x} '
            f'{symbol}{specs.body_dims["height"]/2})\n'
            '        (end '
            f'-{silkscreen_x} '
            f'{symbol}{specs.body_dims["height"]/2})\n'
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
        f'        (at 0 {-1 * specs.ref_offset_y + 1.27} 0)\n'
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
        '        (offset (xyz 0 0 0))\n'
        '        (scale (xyz 1 1 1))\n'
        '        (rotate (xyz 0 0 0))\n'
        '    )'
    )


def generate_footprint_file(
        part_info: ssi.PartInfo,
        output_dir: str) -> None:
    """
    Generate and save a complete .kicad_mod file for an inductor.

    Creates a KiCad footprint file in the specified directory using the
    provided PartInfo object containing series information.

    Args:
        part_info: PartInfo object containing the inductor series name
        output_dir:
            Directory path where the generated footprint file will be saved

    Raises:
        ValueError: If the specified series is not found in INDUCTOR_SPECS
        IOError: If there are problems writing the output file
    """
    if part_info.series not in INDUCTOR_SPECS:
        raise ValueError(f"Unknown series: {part_info.series}")

    filename = part_info.series

    inductor_specs = create_inductor_specs(filename)
    footprint_content = generate_footprint(inductor_specs)

    filename = f"{output_dir}/{filename}.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as file_handle:
        file_handle.write(footprint_content)
