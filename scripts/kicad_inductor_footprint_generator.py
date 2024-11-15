"""
KiCad Footprint Generator for Inductors

Generates standardized KiCad footprint files (.kicad_mod) for various inductor
series. Uses manufacturer specifications to create accurate footprints with
appropriate pad dimensions and clearances.
"""

from typing import Dict, NamedTuple
from uuid import uuid4
from series_specs_inductors import PartInfo


class PadDimensions(NamedTuple):
    """
    Defines SMD pad dimensions and positioning.

    All measurements are in millimeters.
    """
    width: float      # Width of each pad
    height: float     # Height of each pad
    center_x: float   # Distance from origin to pad center


class InductorSpecs(NamedTuple):
    """
    Complete specifications for generating an inductor footprint.

    Combines physical dimensions with series-specific properties.
    """
    body_width: float         # Width of inductor body
    body_height: float        # Height of inductor body
    pad_dims: PadDimensions  # Pad specifications
    silk_y: float            # Y-coordinate of silkscreen lines
    silk_extension: float    # X-extension of silkscreen lines
    silk_inset: float        # Distance silk extends from body
    courtyard_margin: float  # Courtyard margin beyond body
    ref_y: float            # Y position for reference designator
    value_y: float          # Y position for value text
    fab_reference_y: float  # Y position for fab layer reference


# Default specifications for different inductor series
INDUCTOR_SPECS: Dict[str, Dict[str, float]] = {
    "XFL4020": {
        "body_width": 4.0,
        "body_height": 4.0,
        "pad_width": 0.9652,
        "pad_height": 3.4036,
        "pad_center_x": 1.1811,
        "silk_y": 1.6256,
        "silk_extension": 0.6096,
        "silk_inset": 0.2,
        "courtyard_margin": 0.25,
        "ref_y": -3.048,
        "value_y": 4.318,
        "fab_reference_y": 3.048
    },
    "XFL4015": {
        "body_width": 4.0,
        "body_height": 4.0,
        "pad_width": 0.9652,
        "pad_height": 3.4036,
        "pad_center_x": 1.1811,
        "silk_y": 2.2352,
        "silk_extension": 0.6096,
        "silk_inset": 0.2,
        "courtyard_margin": 0.25,
        "ref_y": -3.048,
        "value_y": 4.318,
        "fab_reference_y": 3.048
    }
}


def create_inductor_specs(series_name: str) -> InductorSpecs:
    """
    Create complete inductor specifications from series name.

    Args:
        series_name: Name of the inductor series (e.g., "XFL4020")

    Returns:
        InductorSpecs object with complete physical dimensions

    Raises:
        KeyError: If series_name is not found in INDUCTOR_SPECS
    """
    specs = INDUCTOR_SPECS[series_name]

    return InductorSpecs(
        body_width=specs["body_width"],
        body_height=specs["body_height"],
        pad_dims=PadDimensions(
            width=specs["pad_width"],
            height=specs["pad_height"],
            center_x=specs["pad_center_x"]
        ),
        silk_y=specs["silk_y"],
        silk_extension=specs["silk_extension"],
        silk_inset=specs["silk_inset"],
        courtyard_margin=specs["courtyard_margin"],
        ref_y=specs["ref_y"],
        value_y=specs["value_y"],
        fab_reference_y=specs["fab_reference_y"]
    )


def generate_footprint(specs: InductorSpecs, part_info: PartInfo) -> str:
    """
    Generate complete KiCad footprint file content for an inductor.

    Args:
        specs: Physical specifications for the inductor
        part_info: Part information from series specifications

    Returns:
        Complete .kicad_mod file content as formatted string
    """
    sections = [
        generate_header(part_info.series),
        generate_properties(part_info.series, specs),
        generate_silkscreen(specs),
        generate_courtyard(specs),
        generate_fab_layer(specs),
        generate_pads(specs),
        generate_3d_model(part_info.series),
        ")"  # Close the footprint
    ]
    return "\n".join(sections)


def generate_header(series_name: str) -> str:
    """Generate the footprint header section."""
    return (
        f'(footprint "{series_name}"\n'
        f'    (version 20240108)\n'
        f'    (generator "pcbnew")\n'
        f'    (generator_version "8.0")\n'
        f'    (layer "F.Cu")'
    )


def generate_properties(series_name: str, specs: InductorSpecs) -> str:
    """Generate properties section."""
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
        f'    (property "Reference" "REF**"\n'
        f'        (at 0 {specs.ref_y} 0)\n'
        f'        (unlocked yes)\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        f'    )\n'
        f'    (property "Value" "{series_name}"\n'
        f'        (at 0 {specs.value_y} 0)\n'
        f'        (unlocked yes)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        f'    )\n'
        f'    (property "Footprint" ""\n'
        f'        (at 0 0 0)\n'
        f'        (layer "F.Fab")\n'
        f'        (hide yes)\n'
        f'        (uuid "{uuid4()}")\n'
        f'{font_props}\n'
        f'    )'
    )


def generate_silkscreen(specs: InductorSpecs) -> str:
    """Generate silkscreen elements."""
    return (
        f'    (attr smd)\n'
        f'    (fp_line\n'
        f'        (start -{specs.silk_extension} {specs.silk_y})\n'
        f'        (end {specs.silk_extension} {specs.silk_y})\n'
        f'        (stroke\n'
        f'            (width 0.1524)\n'
        f'            (type solid)\n'
        f'        )\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )\n'
        f'    (fp_line\n'
        f'        (start {specs.silk_extension} -{specs.silk_y})\n'
        f'        (end -{specs.silk_extension} -{specs.silk_y})\n'
        f'        (stroke\n'
        f'            (width 0.1524)\n'
        f'            (type solid)\n'
        f'        )\n'
        f'        (layer "F.SilkS")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )


def generate_courtyard(specs: InductorSpecs) -> str:
    """Generate courtyard outline."""
    half_width = specs.body_width/2 + specs.courtyard_margin
    half_height = specs.body_height/2 + specs.courtyard_margin

    return (
        f'    (fp_rect\n'
        f'        (start -{half_width} -{half_height})\n'
        f'        (end {half_width} {half_height})\n'
        f'        (stroke\n'
        f'            (width 0.00635)\n'
        f'            (type default)\n'
        f'        )\n'
        f'        (fill none)\n'
        f'        (layer "F.CrtYd")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )


def generate_fab_layer(specs: InductorSpecs) -> str:
    """Generate fabrication layer."""
    half_width = specs.body_width/2
    half_height = specs.body_height/2

    return (
        f'    (fp_rect\n'
        f'        (start -{half_width} -{half_height})\n'
        f'        (end {half_width} {half_height})\n'
        f'        (stroke\n'
        f'            (width 0.0254)\n'
        f'            (type default)\n'
        f'        )\n'
        f'        (fill none)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )\n'
        f'    (fp_circle\n'
        f'        (center -{specs.pad_dims.center_x} 0)\n'
        f'        (end {-specs.pad_dims.center_x + 0.0762} 0)\n'
        f'        (stroke\n'
        f'            (width 0.0254)\n'
        f'            (type solid)\n'
        f'        )\n'
        f'        (fill none)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )\n'
        f'    (fp_text user "${{REFERENCE}}"\n'
        f'        (at 0 {specs.fab_reference_y} 0)\n'
        f'        (layer "F.Fab")\n'
        f'        (uuid "{uuid4()}")\n'
        f'        (effects\n'
        f'            (font\n'
        f'                (size 0.762 0.762)\n'
        f'                (thickness 0.1524)\n'
        f'            )\n'
        f'            (justify left)\n'
        f'        )\n'
        f'    )'
    )


def generate_pads(specs: InductorSpecs) -> str:
    """Generate SMD pads."""
    pads = []

    # Left pad (1)
    pads.append(
        f'    (pad "1" smd rect\n'
        f'        (at -{specs.pad_dims.center_x} 0)\n'
        f'        (size {specs.pad_dims.width} {specs.pad_dims.height})\n'
        f'        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    # Right pad (2)
    pads.append(
        f'    (pad "2" smd rect\n'
        f'        (at {specs.pad_dims.center_x} 0)\n'
        f'        (size {specs.pad_dims.width} {specs.pad_dims.height})\n'
        f'        (layers "F.Cu" "F.Paste" "F.Mask")\n'
        f'        (uuid "{uuid4()}")\n'
        f'    )'
    )

    return "\n".join(pads)


def generate_3d_model(series_name: str) -> str:
    """Generate 3D model reference."""
    return (
        f'    (model "${{KIPRJMOD}}/KiCAD_Symbol_Generator/3D_models/'
        f'{series_name}.step"\n'
        f'        (offset (xyz 0 0 0.1016))\n'
        f'        (scale (xyz 1 1 1))\n'
        f'        (rotate (xyz -90 0 0))\n'
        f'    )'
    )


def generate_footprint_file(part_info: PartInfo, output_dir: str) -> None:
    """
    Generate and save a complete .kicad_mod file for an inductor.

    Args:
        part_info: Part information from series specifications
        output_dir: Directory to save the generated footprint file

    Raises:
        KeyError: If series_name is not found in INDUCTOR_SPECS
        IOError: If there are problems writing the output file
    """
    inductor_specs = create_inductor_specs(part_info.series)
    footprint_content = generate_footprint(inductor_specs, part_info)

    filename = f"{output_dir}/{part_info.series}.kicad_mod"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(footprint_content)
